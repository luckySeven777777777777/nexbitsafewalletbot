import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ✅ 频道 username（不是名字）
CHANNEL_USERNAME = "@nexbitsafewallet"

# ✅ 钱包网站
WALLET_URL = "https://www.nexbitsafe.com/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 *NEXBIT-SAFE Wallet*\n\n"
        "Secure crypto wallet & market intelligence.\n\n"
        "🔐 Non-custodial Wallet\n"
        "📊 Real-time Market Tools\n"
        "⚡ Fast & Secure",
        parse_mode="Markdown"
    )


async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Open Wallet", url=WALLET_URL)]
    ])

    text = (
        "🚀 *NEXBIT-SAFE WALLET*\n\n"
        "Your secure non-custodial crypto wallet on Telegram.\n\n"
        "🔐 Non-custodial Security\n"
        "📊 Real-time Market Data\n"
        "⚡ Fast & Reliable\n\n"
        "Tap below to launch:"
    )

    await context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

    await update.message.reply_text("✅ Channel post sent successfully.")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post))

    app.run_polling()


if __name__ == "__main__":
    main()
