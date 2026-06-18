import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import random
import glob
import os.path
import datetime

# 从 Railway / 环境变量读取 Token（不要写死）
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 你的真实交易 / WebApp 地址
TRADE_URL = "https://www.appyourplatform.info/trade"

# 客服账号（或群）
SUPPORT_CONTACT = "@xwallettonlineservice"
# ===== Ad Content Config (Editable) =====
AD_TEXT = os.getenv(
    "AD_TEXT",
    "🚀 *X-WALLET*\n\n"
    "🔐 Secure, non-custodial crypto wallet\n"
    "📊 Real-time market data & analytics\n"
    "⚡ Fast, reliable infrastructure\n\n"
    "👇 Tap below to continue"
)

# ===== Channel Ads Config =====
CHANNEL_ID = -1003521365611  # ⚠️ 换成你的频道ID
IMAGE_DIR = "images"  # 本地图片文件夹，每次随机选一张

# ===== 广告图文配对（17张图 × 17段文案，按天轮换）=====
AD_PAIRS = [
    # 1. Cyberpunk Night X-WALLET
    (
        "Gemini_Generated_Image_2xj9tz2xj9tz2xj9.png",
        "🌃 *X-WALLET — Non-Custodial Crypto Suite*\n\nMulti-chain wallet supporting BTC, ETH, BNB\nInstitutional-grade security architecture\n24/7 dedicated support team standing by\n\n👇 Join Now"
    ),
    # 2. Security Guardian
    (
        "Gemini_Generated_Image_bhpvugbhpvugbhpv.png",
        "🔐 *X-WALLET — Enterprise Security Standard*\n\nAES-256 encryption · Multi-Party Computation\nCold storage with real-time risk monitoring\nYour private keys, exclusively yours\n\n👇 Trade Securely"
    ),
    # 3. Multi-Chain Treasure
    (
        "Gemini_Generated_Image_bzsrg3bzsrg3bzsr.png",
        "💎 *X-WALLET — Cross-Chain Asset Hub*\n\nBTC · ETH · BNB · USDT unified management\nReal-time price feeds across 50+ exchanges\nInstant cross-chain swaps at optimal rates\n\n👇 Start Trading"
    ),
    # 4. ETH Smart Contract Interaction
    (
        "Gemini_Generated_Image_c6k61dc6k61dc6k6.png",
        "📈 *X-WALLET — DeFi & Smart Contracts*\n\nNative Web3 dApp browser built in\nSeamless DeFi yield farming integration\nGas optimization for every transaction\n\n👇 Connect dApp"
    ),
    # 5. Trading Is Live
    (
        "Gemini_Generated_Image_cfwethcfwethcfwe.png",
        "🏄 *X-WALLET — Spot & Derivatives Trading*\n\nBTC/USDT · ETH/USDT · BNB/USDT live\nDeep liquidity pools, minimal slippage\nLightning-fast order execution engine\n\n👇 Trade Now"
    ),
    # 6. Crypto Vault
    (
        "Gemini_Generated_Image_cg6wfvcg6wfvcg6w.png",
        "🛡️ *X-WALLET — Secured Asset Custody*\n\nMulti-signature authorization protocol\nAnti-phishing protection layer activated\nSOC 2 Type II certified infrastructure\n\n👇 Deposit With Confidence"
    ),
    # 7. Stablecoin Hub
    (
        "Gemini_Generated_Image_e8py8ie8py8ie8py.png",
        "💰 *X-WALLET — Stablecoin Gateway*\n\nUSDT / USDC deposits credited instantly\nFiat on-ramp via 40+ payment methods\nZero confirmation wait for verified users\n\n👇 Deposit USDT"
    ),
    # 8. Web3 Explorer
    (
        "Gemini_Generated_Image_ex6mugex6mugex6m.png",
        "🎮 *X-WALLET — NFT & GameFi Ecosystem*\n\nConnect MetaMask · Trust Wallet · Ledger\nNFT gallery with rarity ranking engine\nGameFi staking rewards up to 45% APY\n\n👇 Enter Web3"
    ),
    # 9. System Update Portal
    (
        "Gemini_Generated_Image_f8gxatf8gxatf8gx.png",
        "⚡ *X-WALLET — v3.2 System Upgrade*\n\nNew: BNB Smart Chain full integration\nEnhanced: KYT anti-money laundering module\nOptimized: Node response time reduced 62%\n\n👇 Read Changelog"
    ),
    # 10. Maximum Security
    (
        "Gemini_Generated_Image_izctmbizctmbizct.png",
        "🔒 *X-WALLET — Zero-Trust Security Model*\n\nHardware Security Module (HSM) certified\nBiometric authentication + 2FA enforcement\nBug bounty program up to $500,000\n\n👇 Audit Report"
    ),
    # 11. Lightning Speed
    (
        "Gemini_Generated_Image_kjabs9kjabs9kjab.png",
        "🏁 *X-WALLET — High-Frequency Performance*\n\nSub-millisecond matching engine\n10,000 TPS throughput capacity\n99.99% uptime SLA commitment\n\n👇 Benchmark Results"
    ),
    # 12. Connect Any Wallet
    (
        "Gemini_Generated_Image_onaydionaydionay.png",
        "🌐 *X-WALLET — Universal Wallet Aggregator*\n\nWalletConnect v2.0 protocol supported\nImport 100+ wallets via seed phrase\nUnified balance dashboard across chains\n\n👇 Connect Wallet"
    ),
    # 13. Leaderboard
    (
        "Gemini_Generated_Image_qtlt6hqtlt6hqtlt.png",
        "🏆 *X-WALLET — Professional Trading Terminal*\n\nBTC $XX,XXX | ETH $X,XXX | BNB $XXX\nAdvanced charting: TradingView integration\nAPI access for algorithmic trading bots\n\n👇 Open Terminal"
    ),
    # 14. Mobile Trading
    (
        "Gemini_Generated_Image_xoze34xoze34xoze.png",
        "📱 *X-WALLET — iOS & Android App*\n\nFull trading functionality on mobile\nFace ID / fingerprint biometric unlock\nPush alerts for price targets & whale moves\n\n👇 Download App"
    ),
    # 15. Live Market Data
    (
        "Gemini_Generated_Image_yy238xyy238xyy23.png",
        "📊 *X-WALLET — Market Intelligence Suite*\n\nBTC/ETH/BNB real-time order book depth\nOn-chain whale alert & large transfer tracker\nVIX-style volatility index for crypto\n\n👇 View Dashboard"
    ),
    # 16. 24/7 Support
    (
        "Gemini_Generated_Image_z4neepz4neepz4ne.png",
        "🛎️ *X-WALLET — 24/7 Concierge Support*\n\nAverage response time: under 90 seconds\nDedicated account manager for VIP tier\nMulti-language support: EN · 中文 · 日本語\n\n👇 Contact Support"
    ),
    # 17. Bitcoin Power Core
    (
        "Gemini_Generated_Image_z9a2ipz9a2ipz9a2.png",
        "💫 *X-WALLET — BTC Native Experience*\n\nFull node validation, trust minimized\nTaproot & Lightning Network ready\nSegWit addresses for lowest fees\n\n👇 Buy BTC Instantly"
    ),
]


# /start：自动发送欢迎 + 底部键盘
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            KeyboardButton("🚀 TRADE NOW"),
            KeyboardButton("🆘 SUPPORT"),
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Choose an option"
    )

    await update.message.reply_text(
        "👋 Welcome to *X-Wallet*\n\n"
        "🔐 Secure non-custodial crypto wallet\n"
        "📊 Real-time market data & tools\n"
        "⚡ Fast, reliable, and safe\n\n"
        "👇 Choose an option below:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


# 处理按钮点击
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 有些 update 没有 message（例如按钮点击 / 系统事件）
    if not update.message:
        return

    text = update.message.text


    if text == "🚀 TRADE NOW":
        await update.message.reply_text(
            f"🚀 Opening X-Wallet:\n{TRADE_URL}"
        )

    elif text == "🆘 SUPPORT":
        await update.message.reply_text(
            f"🆘 Support contact:\n{SUPPORT_CONTACT}"
        )

    else:
        await update.message.reply_text(
            "Please use the buttons below 👇"
        )

async def send_daily_channel_ad(context: ContextTypes.DEFAULT_TYPE):
    # 按日期轮换图文配对（每天换一张，17天一轮）
    pair = AD_PAIRS[datetime.date.today().toordinal() % len(AD_PAIRS)]
    img_filename, caption = pair

    keyboard = [
        [
            InlineKeyboardButton("🔥 DEPOSIT", url="https://www.appyourplatform.info/deposit"),
            InlineKeyboardButton("📊 MARKET", url="https://www.appyourplatform.info/market"),
        ],
        [
            InlineKeyboardButton("⚖️ PLAN", url="https://www.appyourplatform.info/plan"),
            InlineKeyboardButton("🤖 AI BOT", url="https://t.me/nexbitsafebot"),
        ],
        [
            InlineKeyboardButton("🚀 TRADE", url=TRADE_URL),
            InlineKeyboardButton(
                "🆘 SUPPORT",
                url=f"https://t.me/{SUPPORT_CONTACT.lstrip('@')}"
            )
        ]
    ]

    img_path = os.path.join(IMAGE_DIR, img_filename)
    with open(img_path, "rb") as img:
        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=img,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    # ===== Daily Channel Ad (Once Per Day) =====
    app.job_queue.run_repeating(
    send_daily_channel_ad,
    interval=7 * 24 * 60 * 60,  # ✅ 7 天（一个星期）一次
    first=10
)



    print("🤖 X-Wallet Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
