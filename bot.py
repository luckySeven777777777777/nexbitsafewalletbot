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

# 从 Railway / 环境变量读取 Token（不要写死）
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 你的真实交易 / WebApp 地址
TRADE_URL = "https://www.nexbitsafe.com/trade"

# 客服账号（或群）
SUPPORT_CONTACT = "@nexbitonlineservice"
# ===== Ad Content Config (Editable) =====
AD_TEXT = os.getenv(
    "AD_TEXT",
    "🚀 *NEXBIT-SAFE WALLET*\n\n"
    "🔐 Secure, non-custodial crypto wallet\n"
    "📊 Real-time market data & analytics\n"
    "⚡ Fast, reliable infrastructure\n\n"
    "👇 Tap below to continue"
)

# ===== Channel Ads Config =====
CHANNEL_ID = -1003521365611  # ⚠️ 换成你的频道ID
AD_IMAGE_URL = "https://custom-images.strikinglycdn.com/res/hrscywv4p/image/upload/c_limit,fl_lossy,h_9000,w_1200,f_auto,q_auto/13252794/770448_524050.png"  # 广告图片（必须是公网 https）


# /start：自动发送欢迎 + 底部键盘
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🔥 DEPOSIT", url="https://www.nexbitsafe.com/deposit"),
            InlineKeyboardButton("📊 MARKET", url="https://www.nexbitsafe.com/market"),
        ],
        [
            InlineKeyboardButton("⚖️ PLAN", url="https://www.nexbitsafe.com/arbitrage-products"),
            InlineKeyboardButton("🤖 AI BOT", url="https://t.me/nexbitsafebot"),
        ],
        [
            InlineKeyboardButton("🚀 TRADE", url=TRADE_URL),
            InlineKeyboardButton(
                "🆘 SUPPORT",
                url=f"https://t.me/{SUPPORT_CONTACT.lstrip('@')}",
            ),
        ],
    ]

    await update.message.reply_text(
        "👋 Welcome to *NEXBIT-SAFE Wallet*\n\n"
        "🔐 Secure non-custodial crypto wallet\n"
        "📊 Real-time market data & tools\n"
        "⚡ Fast, reliable, and safe\n\n"
        "👇 Choose an option below:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN,
    )



# 处理按钮点击
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🚀 TRADE NOW":
        await update.message.reply_text(
            f"🚀 Opening NEXBIT-SAFE Wallet:\n{TRADE_URL}"
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
    caption = AD_TEXT

    keyboard = [
        [
            InlineKeyboardButton("🚀 TRADE", url=TRADE_URL),
            InlineKeyboardButton(
                "🆘 SUPPORT",
                url=f"https://t.me/{SUPPORT_CONTACT.lstrip('@')}"
            )
        ]
    ]

    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=AD_IMAGE_URL,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # ===== Daily Channel Ad (Once Per Day) =====
    app.job_queue.run_repeating(
    send_daily_channel_ad,
    interval=3 * 24 * 60 * 60,  # ✅ 3 天一次
    first=10
)


    print("🤖 NEXBIT-SAFE Wallet Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
