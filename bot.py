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
AD_IMAGE_URL = "https://t3.ftcdn.net/jpg/16/55/10/30/360_F_1655103052_0PkAG5DGDHUQDxVEfMBCbtVS4yYrm7dL.jpg"  # 广告图片（必须是公网 https）


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
        "👋 Welcome to *NEXBIT-SAFE Wallet*\n\n"
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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    # ===== Daily Channel Ad (Once Per Day) =====
    app.job_queue.run_repeating(
    send_daily_channel_ad,
    interval=7 * 24 * 60 * 60,  # ✅ 7 天（一个星期）一次
    first=10
)



    print("🤖 NEXBIT-SAFE Wallet Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
