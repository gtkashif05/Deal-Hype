import sys
import os
import time
import json
import urllib.request
import urllib.parse
import re
import html
from datetime import datetime

from config import Config
from database import Database
from affiliate import build_affiliate_link
from telegram_poster import TelegramPoster

TRENDING_DEALS_API = "https://www.dealsmagnet.com/PublicUser/GetAllTrendingDeals"
DEAL_PAGE_PREFIX = "https://www.dealsmagnet.com/deal/"
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

class LootDealsBot:
    def __init__(self, config=Config):
        self.config = config
        self.db = Database()
        self.poster = TelegramPoster(
            bot_token=self.config.TELEGRAM_BOT_TOKEN,
            default_chat_id=self.config.TELEGRAM_CHANNEL
        )

    def fetch_trending_deals(self):
        """Fetches live deals from the API."""
        try:
            req = urllib.request.Request(
                TRENDING_DEALS_API,
                data=b"",
                headers={
                    "User-Agent": DEFAULT_USER_AGENT,
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                }
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                deals = data.get("Deals", [])
                return deals
        except Exception as e:
            print(f"[Fetch Error] Failed to fetch deals feed: {e}")
            return []

    def resolve_store_link(self, deal_url_slug: str) -> str:
        """
        Fetches the deal page, extracts the buy button data-code,
        and follows the redirect to get the true Amazon/Flipkart product URL.
        """
        full_deal_url = DEAL_PAGE_PREFIX + deal_url_slug
        try:
            req = urllib.request.Request(full_deal_url, headers={"User-Agent": DEFAULT_USER_AGENT})
            with urllib.request.urlopen(req, timeout=12) as resp:
                html_content = resp.read().decode("utf-8", errors="ignore")

            match = re.search(r'data-code="([^"]+)"', html_content)
            if not match:
                return full_deal_url

            data_code = match.group(1)
            buy_url = f"https://www.dealsmagnet.com/buy?{data_code}"

            # Track redirects to find final store link
            class RedirectTracker(urllib.request.HTTPRedirectHandler):
                def __init__(self):
                    self.links = []
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    self.links.append(newurl)
                    return super().redirect_request(req, fp, code, msg, headers, newurl)

            tracker = RedirectTracker()
            opener = urllib.request.build_opener(tracker)
            req2 = urllib.request.Request(buy_url, headers={"User-Agent": DEFAULT_USER_AGENT})
            with opener.open(req2, timeout=15) as buy_resp:
                final_url = buy_resp.geturl()

            # Check if any redirect had embedded store link (e.g., linksredirect or url=)
            all_urls = [buy_url] + tracker.links + [final_url]
            for u in all_urls:
                # Check for ?url= or &url=
                if "url=" in u:
                    parsed = urllib.parse.urlparse(u)
                    qs = urllib.parse.parse_qs(parsed.query)
                    if "url" in qs:
                        inner = qs["url"][0]
                        if "amazon" in inner or "flipkart" in inner or "myntra" in inner:
                            return inner
                if "amazon.in" in u or "flipkart.com" in u:
                    return u

            return final_url

        except Exception as e:
            print(f"[Resolve Warning] Could not resolve store redirect: {e}")
            return full_deal_url

    def construct_image_url(self, deal: dict) -> str:
        """
        Derives high-res product image URL from deal metadata.
        """
        url_slug = deal.get("Url", "")
        unique_key = deal.get("UniqueKey", "")
        if url_slug and unique_key:
            # Replace -{UniqueKey} with -o-{UniqueKey}.jpg
            slug_base = url_slug
            if slug_base.endswith(f"-{unique_key}"):
                slug_base = slug_base[:-len(f"-{unique_key}")]
            return f"https://www.dealsmagnet.com/images/{slug_base}-o-{unique_key}.jpg"
        return ""

    def process_and_post_deals(self, dry_run=False, max_posts=5):
        """
        Main deal processing cycle.
        """
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for latest loot deals...")
        deals = self.fetch_trending_deals()
        if not deals:
            print("No deals found or API unreachable.")
            return 0

        posted_count = 0
        min_discount = self.config.MIN_DISCOUNT_PERCENT

        for deal in deals:
            # Filter 1: Expired deals
            if str(deal.get("Expire", "0")) != "0":
                continue

            # Filter 2: Minimum discount percentage
            raw_percent = str(deal.get("Percentage", "0")).replace("%", "").strip()
            discount = int(raw_percent) if raw_percent.isdigit() else 0
            if discount < min_discount:
                continue

            unique_key = deal.get("UniqueKey") or deal.get("Id")
            if not unique_key:
                continue

            # Filter 3: Duplicate check in SQLite database
            if self.db.is_deal_posted(unique_key):
                continue

            raw_title = deal.get("Title", "Hot Deal")
            title = html.unescape(raw_title).strip()
            price = deal.get("Price", "0")
            orig_price = deal.get("OriginalPrice", "0")
            store = deal.get("Publisher") or "Online Store"
            image_url = self.construct_image_url(deal)

            print(f"\n[NEW DEAL FOUND] {title[:60]}...")
            print(f"  Price: Rs.{price} | MRP: Rs.{orig_price} | Discount: {discount}% | Store: {store}")

            # Resolve real store link
            raw_store_url = self.resolve_store_link(deal.get("Url", ""))
            
            # Attach User's Affiliate Tag
            affiliate_url = build_affiliate_link(store, raw_store_url, self.config)
            print(f"  Affiliate Link: {affiliate_url}")

            if dry_run:
                print("  [DRY RUN] Simulating post (not sending to Telegram).")
                posted_count += 1
            else:
                if not self.config.is_configured():
                    print("  [CONFIG WARNING] Telegram bot credentials not set in .env! Skipping live post.")
                    continue

                success = self.poster.post_deal(
                    deal=deal,
                    buy_url=affiliate_url,
                    image_url=image_url,
                    config=self.config
                )

                if success:
                    print("  [SUCCESS] Posted to Telegram channel!")
                    self.db.save_posted_deal(
                        unique_key=unique_key,
                        title=title,
                        price=price,
                        original_price=orig_price,
                        discount=discount,
                        store=store,
                        product_url=affiliate_url
                    )
                    posted_count += 1
                    # Small delay between posts to prevent Telegram rate-limiting
                    time.sleep(3)
                else:
                    print("  [FAILED] Could not post to Telegram.")

            if posted_count >= max_posts:
                break

        print(f"\nCycle complete. Total deals processed/posted: {posted_count}")
        return posted_count

    def run_daemon(self):
        """Runs the bot continuously in a loop."""
        interval = self.config.CHECK_INTERVAL_MINUTES * 60
        print("="*60)
        print("   AMAZON / FLIPKART AUTOMATED LOOT DEALS BOT STARTED")
        print("="*60)
        print(f"Target Channel : {self.config.TELEGRAM_CHANNEL or 'Not Configured'}")
        print(f"Min Discount   : {self.config.MIN_DISCOUNT_PERCENT}%")
        print(f"Check Interval : Every {self.config.CHECK_INTERVAL_MINUTES} minutes")
        print("Bot is now running in background. Press Ctrl+C to stop.\n")

        while True:
            try:
                self.process_and_post_deals(dry_run=False, max_posts=3)
                # Cleanup DB once a week
                self.db.cleanup_old_deals(days=14)
                print(f"Sleeping for {self.config.CHECK_INTERVAL_MINUTES} minutes until next check...")
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\n[STOPPED] Bot stopped by user.")
                break
            except Exception as e:
                print(f"[Daemon Error] {e}")
                time.sleep(60)

def main():
    bot = LootDealsBot()

    if "--test" in sys.argv:
        print("[TEST MODE] Fetching deals and testing affiliate conversion...")
        bot.process_and_post_deals(dry_run=True, max_posts=5)

    elif "--verify" in sys.argv:
        print("[VERIFY MODE] Checking Telegram Bot connection...")
        if not Config.TELEGRAM_BOT_TOKEN:
            print("ERROR: TELEGRAM_BOT_TOKEN is empty in .env!")
        else:
            ok, msg = bot.poster.verify_bot()
            if ok:
                print(f"SUCCESS: {msg}")
            else:
                print(f"FAILED: {msg}")

    elif "--once" in sys.argv:
        print("[RUN ONCE] Checking and posting new deals once...")
        bot.process_and_post_deals(dry_run=False, max_posts=5)

    else:
        # Default daemon mode
        bot.run_daemon()

if __name__ == "__main__":
    main()
