"""
NyayaMitra AI - Telegram Legal Assistant Bot
Civic Legal Guidance for Indian Citizens via Telegram
Supports text inquiries, photo receipt/fraud SMS OCR, and 6 Indian languages.
"""

import os
import io
import sys
import logging
import asyncio
from dotenv import load_dotenv

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("NyayaMitraBot")

# Import core NyayaMitra engine
import legal_retriever
import ai_service
import database

# Ensure database tables exist
database.init_db()

# User language preferences stored in memory (default: English)
user_languages = {}

LANG_CODE_MAP = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "mr": "Marathi"
}

def format_telegram_response(res: dict) -> str:
    """Formats the JSON legal guidance into a clean, readable Telegram message."""
    category = res.get("category", "Legal Guidance")
    explanation = res.get("explanation", "")
    actions = res.get("actions", [])
    evidence = res.get("evidence", [])
    laws = res.get("applicable_laws", [])
    resources = res.get("official_resources", [])
    disclaimer = res.get("disclaimer", "")

    lines = []
    lines.append(f"⚖️ *NyayaMitra Legal Guidance* | *{category}*")
    lines.append("────────────────────────")
    
    if laws:
        lines.append(f"🏛️ *Applicable Laws:* {', '.join(laws[:3])}")
        lines.append("")

    if explanation:
        lines.append(f"💡 *Summary:*\n{explanation}")
        lines.append("")

    if actions:
        lines.append("⚡ *Immediate Action Steps:*")
        for i, act in enumerate(actions[:4], 1):
            lines.append(f"  {i}. {act}")
        lines.append("")

    if evidence:
        lines.append("📋 *Key Documents & Evidence:*")
        for ev in evidence[:4]:
            lines.append(f"  • {ev}")
        lines.append("")

    if resources:
        lines.append("📞 *Official Helplines & Portals:*")
        for r in resources[:3]:
            contact = f" ({r.get('contact')})" if r.get("contact") else ""
            lines.append(f"  • *{r.get('name')}*{contact}")
        lines.append("")

    lines.append("⚠️ *Disclaimer:*")
    lines.append(disclaimer[:250] + ("..." if len(disclaimer) > 250 else ""))
    lines.append("\n_Need free lawyer aid? Dial NALSA Helpline 15100 or Tele-Law 14488._")

    return "\n".join(lines)


async def start_command(update, context):
    """Handles the /start command."""
    welcome_text = (
        "⚖️ *Namaste! Welcome to NyayaMitra AI — Your Indian Legal Information Assistant.*\n\n"
        "I provide instant, procedural legal guidance grounded in verified Indian laws "
        "(BNS 2023, CPA 2019, Model Tenancy Act, RTI Act 2005).\n\n"
        "*What you can do:*\n"
        "1. 📝 *Describe your problem* in plain words (e.g. _'Lost ₹15,000 in fake electricity bill SMS'_)\n"
        "2. 📸 *Send a photo or screenshot* of a UPI receipt, bank SMS, or dispute letter for instant OCR\n"
        "3. 🌐 *Change language:* Use /language (`en`, `hi`, `ta`, `te`, `bn`, `mr`)\n\n"
        "*Supported Categories:*\n"
        "• 💳 Cyber & Financial Fraud (1930)\n"
        "• 🛒 Consumer Complaints (1915)\n"
        "• 💼 Workplace & Salary Disputes\n"
        "• 🏠 Tenancy & Security Deposit\n"
        "• 📜 RTI (Right to Information)\n\n"
        "_Send your legal query or a receipt photo now to get started!_"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def help_command(update, context):
    """Handles the /help command with emergency contacts."""
    help_text = (
        "🆘 *NyayaMitra Emergency Helplines & Usage Guide*\n\n"
        "*Emergency Helplines (Pan-India):*\n"
        "• 🚨 *Cyber Crime Helpline:* 1930 (Dial within golden hour)\n"
        "• 🛒 *National Consumer Helpline:* 1915\n"
        "• ⚖️ *NALSA Free Legal Aid:* 15100\n"
        "• 📞 *Tele-Law Citizen Advice:* 14488\n\n"
        "*Commands:*\n"
        "/start - Welcome screen\n"
        "/language <code > - Set language (e.g. `/language hi` or `/language ta`)\n"
        "/help - Emergency numbers & tips\n\n"
        "*Tip:* You can also type in *Hindi, Tamil, Telugu, Bengali, Marathi, or Hinglish*!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def language_command(update, context):
    """Sets user preferred language."""
    chat_id = update.effective_chat.id
    args = context.args
    if not args:
        current = user_languages.get(chat_id, "English")
        await update.message.reply_text(
            f"Current language: *{current}*\n\n"
            "To change, send: `/language <code>`\n"
            "• `en` - English\n"
            "• `hi` - हिंदी (Hindi)\n"
            "• `ta` - தமிழ் (Tamil)\n"
            "• `te` - తెలుగు (Telugu)\n"
            "• `bn` - বাংলা (Bengali)\n"
            "• `mr` - मराठी (Marathi)",
            parse_mode="Markdown"
        )
        return

    code = args[0].lower().strip()
    if code in LANG_CODE_MAP:
        user_languages[chat_id] = LANG_CODE_MAP[code]
        await update.message.reply_text(
            f"✅ Language set to *{LANG_CODE_MAP[code]}*.",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "Unknown code. Supported: `en`, `hi`, `ta`, `te`, `bn`, `mr`",
            parse_mode="Markdown"
        )


async def handle_text_message(update, context):
    """Processes incoming citizen legal questions."""
    user_query = update.message.text.strip()
    chat_id = update.effective_chat.id
    user_lang = user_languages.get(chat_id, "English")

    if len(user_query) < 5:
        await update.message.reply_text("Please provide a little more detail about what happened.")
        return

    # Send typing action
    await update.message.chat.send_action("typing")

    try:
        # Detect category
        detected_category = legal_retriever.detect_category(user_query)
        # Retrieve verified context
        verified_ctx = legal_retriever.get_verified_context(detected_category, user_lang)
        # Generate legal response
        res = ai_service.generate_legal_response(
            category=detected_category,
            question=user_query,
            verified_ctx=verified_ctx,
            language=user_lang
        )

        reply = format_telegram_response(res)
        await update.message.reply_text(reply, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error handling text query: {e}")
        # Safe fallback
        fallback = (
            "⚖️ *NyayaMitra Guidance*\n\n"
            "We received your query. In case of immediate financial fraud, dial **1930** or visit **cybercrime.gov.in** immediately.\n"
            "For free legal aid, call **NALSA Helpline 15100**."
        )
        await update.message.reply_text(fallback, parse_mode="Markdown")


async def handle_photo_message(update, context):
    """Processes uploaded receipts/screenshots via multi-tiered OCR."""
    chat_id = update.effective_chat.id
    user_lang = user_languages.get(chat_id, "English")

    await update.message.reply_text("🔍 Analyzing receipt image with legal OCR parser...")
    await update.message.chat.send_action("typing")

    try:
        # Get highest resolution photo
        photo = update.message.photo[-1]
        photo_file = await photo.get_file()
        file_bytes = await photo_file.download_as_bytearray()

        caption = update.message.caption or ""

        # Run OCR parser
        parsed = ai_service.parse_document_or_receipt(
            file_bytes=bytes(file_bytes),
            filename="telegram_upload.jpg",
            mime_type="image/jpeg",
            text_context=caption,
            language=user_lang
        )

        amount = parsed.get("amount")
        utr = parsed.get("utr")
        cat = parsed.get("detected_category", "cyber_fraud")
        summary = parsed.get("summary") or "Receipt details parsed."

        info_header = "📄 *Document OCR Extracted Details:*\n"
        if amount:
            info_header += f"• Amount: *₹{amount}*\n"
        if utr:
            info_header += f"• Reference / UTR: *{utr}*\n"
        info_header += f"• Detected Category: *{cat}*\n\n"

        # Generate guidance for the parsed receipt
        prompt = ai_service.build_auto_fill_prompt(parsed, language=user_lang)
        verified_ctx = legal_retriever.get_verified_context(cat, user_lang)
        res = ai_service.generate_legal_response(
            category=cat,
            question=prompt,
            verified_ctx=verified_ctx,
            language=user_lang
        )

        reply = info_header + format_telegram_response(res)
        await update.message.reply_text(reply, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error handling photo upload: {e}")
        await update.message.reply_text(
            "Could not parse image text completely. Please type your legal problem in text.",
            parse_mode="Markdown"
        )


def main():
    """Starts the Telegram bot polling service."""
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token.strip() in ("your_telegram_bot_token_here", ""):
        print("\n" + "=" * 65)
        print("[!] TELEGRAM_BOT_TOKEN NOT CONFIGURED IN .env")
        print("=" * 65)
        print("To enable the NyayaMitra Telegram Bot:")
        print("1. Open Telegram and search for @BotFather")
        print("2. Send /newbot and follow instructions to name your bot")
        print("3. Copy the HTTP API token provided by BotFather")
        print("4. Add to your .env file: TELEGRAM_BOT_TOKEN=123456789:ABCDefgh...")
        print("5. Run: python telegram_bot.py")
        print("=" * 65 + "\n")
        return

    print("[*] Starting NyayaMitra AI Telegram Bot...")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("language", language_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo_message))

    print("[+] NyayaMitra Telegram Bot is active and listening for messages!")
    app.run_polling()


if __name__ == "__main__":
    main()
