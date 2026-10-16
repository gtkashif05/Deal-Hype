import urllib.request
import urllib.parse
import json
import html

class TelegramPoster:
    def __init__(self, bot_token: str, default_chat_id: str):
        self.bot_token = bot_token
        self.default_chat_id = default_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def _api_request(self, method: str, payload: dict):
        """Sends an API request to Telegram Bot API."""
        url = f"{self.base_url}/{method}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")
            print(f"[Telegram HTTP Error {e.code}] {error_body}")
            return {"ok": False, "description": error_body}
        except Exception as e:
            print(f"[Telegram Network Error] {e}")
            return {"ok": False, "description": str(e)}

    def verify_bot(self):
        """Tests if the provided bot token is valid."""
        res = self._api_request("getMe", {})
        if res.get("ok"):
            bot_info = res.get("result", {})
            return True, f"Connected as @{bot_info.get('username', 'Unknown')} ({bot_info.get('first_name', '')})"
        return False, res.get("description", "Invalid Bot Token")

    def format_deal_caption(self, deal: dict, config) -> str:
        """
        Creates a high-converting, professional HTML-formatted caption
        with emojis, bold headers, and discount highlights.
        """
        raw_title = deal.get("Title", "Hot Loot Deal")
        clean_title = html.escape(raw_title)
        
        price = deal.get("Price", "")
        orig_price = deal.get("OriginalPrice", "")
        discount = deal.get("Percentage", "")
        store = (deal.get("Publisher") or "Online Store").capitalize()
        ribbon = deal.get("Ribbon", "")
        
        # Build attractive message
        lines = [
            f"🔥 <b>LOOT DEAL ALERT!</b> 🔥",
            f"",
            f"📦 <b>{clean_title}</b>",
            f"",
            f"💰 <b>Deal Price:</b> ₹{price}  <s>₹{orig_price}</s>",
            f"📉 <b>Discount:</b> <b>{discount}% OFF</b>",
            f"🏷️ <b>Store:</b> {store}",
        ]
        
        if ribbon:
            lines.append(f"⚡ <b>Offer:</b> {html.escape(ribbon)}")
            
        lines.append("")
        lines.append(f"<i>{config.CHANNEL_SIGNATURE}</i>")
        
        if config.CHANNEL_NAME:
            lines.append(f"👉 <b>Join {html.escape(config.CHANNEL_NAME)}</b> for more loot deals!")
            
        return "\n".join(lines)

    def post_deal(self, deal: dict, buy_url: str, image_url: str, config, chat_id: str = None) -> bool:
        """
        Posts deal with image and inline keyboard button.
        Falls back to text message if image fails.
        """
        target_chat = chat_id or self.default_chat_id
        if not target_chat:
            print("[Telegram Error] No chat_id provided.")
            return False

        caption = self.format_deal_caption(deal, config)
        price = deal.get("Price", "")
        discount = deal.get("Percentage", "")
        
        btn_text = f"🔥 BUY NOW @ ₹{price} ({discount}% OFF)"
        share_text = urllib.parse.quote(f"Check this loot deal: {deal.get('Title')} @ ₹{price}!\n{buy_url}")
        share_url = f"https://t.me/share/url?url={urllib.parse.quote(buy_url)}&text={share_text}"
        
        reply_markup = {
            "inline_keyboard": [
                [{"text": btn_text, "url": buy_url}],
                [{"text": "📢 Share Deal With Friends", "url": share_url}]
            ]
        }

        # Try sending photo first
        if image_url:
            photo_payload = {
                "chat_id": target_chat,
                "photo": image_url,
                "caption": caption,
                "parse_mode": "HTML",
                "reply_markup": reply_markup
            }
            res = self._api_request("sendPhoto", photo_payload)
            if res.get("ok"):
                return True
            print(f"[Telegram Warning] Photo post failed, falling back to text. Reason: {res.get('description')}")

        # Fallback to plain message
        text_payload = {
            "chat_id": target_chat,
            "text": caption,
            "parse_mode": "HTML",
            "reply_markup": reply_markup,
            "disable_web_page_preview": False
        }
        res = self._api_request("sendMessage", text_payload)
        return bool(res.get("ok"))
