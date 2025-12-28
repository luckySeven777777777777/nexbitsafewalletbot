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

# 从 Railway / 环境变量读取 Token（不要写死）
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 你的真实交易 / WebApp 地址
TRADE_URL = "https://www.nexbitsafe.com/trade"

# 客服账号（或群）
SUPPORT_CONTACT = "@nexbitonlineservice"


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


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("🤖 NEXBIT-SAFE Wallet Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
