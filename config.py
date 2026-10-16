import os
import re

def load_env_file(filepath=".env"):
    """
    Lightweight .env parser that works without external dependencies.
    """
    env_vars = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                env_vars[k] = v
                os.environ[k] = v
    return env_vars

# Load .env file
load_env_file()

class Config:
    # Telegram Settings
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL", "").strip()  # e.g., "@mydealchannel"
    
    # Affiliate Settings
    AMAZON_AFFILIATE_TAG = os.getenv("AMAZON_AFFILIATE_TAG", "").strip()  # e.g., "lootdeals-21"
    FLIPKART_AFFID = os.getenv("FLIPKART_AFFID", "").strip()              # e.g., "your_affid"
    EARNKARO_USER_ID = os.getenv("EARNKARO_USER_ID", "").strip()          # Optional: EarnKaro profit link ID
    
    # Filter Settings
    MIN_DISCOUNT_PERCENT = int(os.getenv("MIN_DISCOUNT_PERCENT", "50"))   # Only deals with >= 50% discount
    CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "15")) # Check every 15 minutes
    
    # Channel Branding / Footer
    CHANNEL_NAME = os.getenv("CHANNEL_NAME", "Loot Deals Alert").strip()
    CHANNEL_SIGNATURE = os.getenv("CHANNEL_SIGNATURE", "⚡ Fast loot! Price change hone se pehle book karein!").strip()
    
    @classmethod
    def is_configured(cls):
        """Check if basic Telegram credentials are provided."""
        return bool(cls.TELEGRAM_BOT_TOKEN and cls.TELEGRAM_CHANNEL)
