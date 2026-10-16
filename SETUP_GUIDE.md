# 🚀 Amazon & Flipkart Automated Loot Deals Bot - Complete Setup Guide

Yeh guide follow karke aap **5 se 10 minute ke andar** apna automated deals channel live kar sakte hain.

---

## 📋 Table of Contents
1. [Step 1: Telegram Bot Token Kaise Lein?](#step-1-telegram-bot-token-kaise-lein)
2. [Step 2: Telegram Channel Banayein & Bot Ko Admin Banayein](#step-2-telegram-channel-banayein--bot-ko-admin-banayein)
3. [Step 3: Affiliate Tag / Account Setup](#step-3-affiliate-tag--account-setup)
4. [Step 4: `.env` File Configure Karein](#step-4-env-file-configure-karein)
5. [Step 5: Bot Run Karein (1-Click)](#step-5-bot-run-karein-1-click)
6. [Step 6: Zero-Cost Fast Channel Growth Blueprint](#step-6-zero-cost-fast-channel-growth-blueprint)

---

## Step 1: Telegram Bot Token Kaise Lein?
1. Apne mobile ya PC par **Telegram** open karein.
2. Search bar mein search karein: `@BotFather` (verified blue tick wala bot).
3. BotFather ko `/start` bhejें.
4. Ab type karein: `/newbot`
5. BotFather aapse bot ka naam poochega (e.g., `Loot Deals Alert`).
6. Phir username poochega (yeh `bot` se end hona chahiye, e.g., `loot_deals_india_bot`).
7. BotFather aapko ek **HTTP API Token** dega.
   * Yeh token aisa dikhta hai: `7123456789:AAHk..._sample_token_xyz`
   * Ise copy karke rakh lein.

---

## Step 2: Telegram Channel Banayein & Bot Ko Admin Banayein
1. Telegram mein **New Channel** banayein:
   * Channel Name: `Daily Loot Deals & Discounts` (ya apni pasand ka koi bhi catchy naam).
   * Description: `Get 70% to 90% OFF on Amazon, Flipkart, Myntra deals daily!`
   * Channel Type: **Public** select karein aur ek clean username set karein (e.g., `@DailyLootOffersIndia`).
2. **Bot ko Admin banana zaroori hai:**
   * Channel ki **Settings > Administrators > Add Admin** par jayein.
   * Apne banaye hue bot ka username search karein.
   * **"Post Messages"** ki permission ON rakhein aur Save karein.

---

## Step 3: Affiliate Tag / Account Setup

Aapke paas do options hain:

### Option A: EarnKaro (Sabse Aasan & Recommended)
* [EarnKaro.com](https://earnkaro.com) par free account banayein (Instant approval, koi criteria nahi).
* Isme aapko ek referral/user ID milti hai (e.g., `1234567`).
* Iska fayda: Flipkart, Myntra, Ajio, Nykaa ke links automatically convert ho jaate hain.

### Option B: Amazon Associates (Direct)
* [affiliate-program.amazon.in](https://affiliate-program.amazon.in) par account banayein.
* Aapko ek **Store ID / Tracking ID** milegi (e.g., `mydeals-21`).
* Bot automatically har Amazon link mein aapka tag inject karega.

---

## Step 4: `.env` File Configure Karein

Aapke folder `c:\Users\user\Desktop\EARN` mein `.env` file ko open karein (Notepad ya VS Code mein):

```env
# 1. Telegram Details
TELEGRAM_BOT_TOKEN=7123456789:AAHk...AapkaBotTokenYahan
TELEGRAM_CHANNEL=@DailyLootOffersIndia

# 2. Affiliate Tag (Aapka Amazon tag ya EarnKaro ID)
AMAZON_AFFILIATE_TAG=yourdealstag-21
FLIPKART_AFFID=
EARNKARO_USER_ID=

# 3. Deal Settings
MIN_DISCOUNT_PERCENT=50
CHECK_INTERVAL_MINUTES=15

# 4. Branding
CHANNEL_NAME=Daily Loot Offers
CHANNEL_SIGNATURE=⚡ Fast loot! Price change hone se pehle book karein!
```
* File ko **Save** kar dein (`Ctrl + S`).

---

## Step 5: Bot Run Karein (1-Click Launchers)

Folder mein 3 ready-made batch files hain:

1. **`verify_telegram.bat`** (Pehle check karein):
   * Is par double-click karein. Yeh confirm karega ki aapka Telegram Bot token aur connection sahi hai ya nahi.
2. **`test_deals.bat`** (Preview karein):
   * Is par double-click karein. Yeh latest deals live fetch karega aur dikhayega ki affiliate link kaise generate hua hai.
3. **`start_bot.bat`** (24x7 Live Runner):
   * Double-click karein. Bot background mein start ho jayega aur har 15 minute mein automatically new deals Telegram channel par image aur buy button ke sath post karta rahega!

---

## Step 6: Zero-Cost Fast Channel Growth Blueprint

### 1. YouTube Shorts & Instagram Reels (Mass Traffic Hack)
* Jab bot kisi product par 80%–90% off post kare (e.g., Puma sneakers ₹699 mein):
  * Apne phone se 7–10 second ki short video banayein (screen record karein ya product image ke sath background music lagayein).
  * Video text: *"Amazon Glitch Deal! Puma Shoes 80% OFF! Link posted in Telegram (Bio mein link hai)"*.
  * Shopping deals reels bohot tezi se viral hoti hain. Ek reel se 500+ genuine buyers aate hain.

### 2. WhatsApp Groups Seeding
* Apne college, dosto aur family groups mein 2–3 crazy loot deals forward karein:
  * *"Bhai Amazon par glitch se ₹2000 ka headphone ₹399 mein mil raha hai, jaldi loot lo! Daily aisi deals ke liye yeh channel join kar lo."*
* Shuru ke 100 members yahan se instant aa jaate hain.

### 3. Consistency
* Bot ko chalu rakhein. Jab members dekhenge ki channel par daily active aur sasti deals aa rahi hain, to wo channel chhodkar nahi jaate aur notification ON rakhte hain.

---

## 🛠️ File Structure Reference
```
c:\Users\user\Desktop\EARN\
├── bot.py                  # Main automated engine (API, scraping, scheduler)
├── config.py               # Settings loader
├── database.py             # SQLite deduplication (deals_history.db)
├── affiliate.py            # Amazon / Flipkart / EarnKaro link engine
├── telegram_poster.py      # Rich image + inline button sender
├── .env                    # Aapki credentials file
├── test_deals.bat          # 1-Click test script
├── verify_telegram.bat     # 1-Click Telegram test
├── start_bot.bat           # 1-Click 24x7 background runner
└── SETUP_GUIDE.md          # Yeh documentation
```
