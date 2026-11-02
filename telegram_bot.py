"""
NyayaMitra AI - Telegram Legal Assistant Bot
Civic Legal Guidance for Indian Citizens via Telegram
Supports text inquiries, photo receipt/fraud SMS OCR, and 6 Indian languages with Audio Voice Notes (gTTS).
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

# Try importing gTTS for voice note synthesis
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# Ensure database tables exist
database.init_db()

# User preferences stored in memory
user_languages = {}
user_voice_enabled = {}  # chat_id -> bool (default: True)

LANG_CODE_MAP = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "mr": "Marathi"
}

LANG_TO_GTTS = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Bengali": "bn",
    "Marathi": "mr"
}


def generate_audio_summary(res: dict, language: str = "English") -> io.BytesIO:
    """
    Synthesizes a short, punchy 2-3 sentence audio summary of the legal guidance
    in the citizen's preferred language using gTTS, formatted for Telegram voice notes.
    """
    if not GTTS_AVAILABLE:
        return None

    lang_code = LANG_TO_GTTS.get(language, "en")
    category = res.get("category", "Legal Guidance")
    explanation = res.get("explanation", "").strip()
    actions = res.get("actions", [])
    resources = res.get("official_resources", [])

    first_action = actions[0] if actions else ""
    first_res = resources[0] if resources else {}
    helpline = f"{first_res.get('name', 'Helpline')} ({first_res.get('contact', '')})" if first_res else ""

    # Concise spoken scripts tailored by language
    if lang_code == "hi":
        spoken_text = f"न्यायमित्र विधिक मार्गदर्शन। विषय: {category}। "
        if explanation:
            spoken_text += f"{explanation[:150]}। "
        if first_action:
            spoken_text += f"तुरंत कदम: {first_action}। "
        if helpline:
            spoken_text += f"संपर्क करें: {helpline}। "
        spoken_text += "मुफ्त वकील सहायता हेतु नालसा हेल्पलाइन 15100 पर कॉल करें।"
    elif lang_code == "ta":
        spoken_text = f"நியாயமித்ரா சட்ட வழிகாட்டுதல். பிரிவு: {category}. "
        if first_action:
            spoken_text += f"உடனடி நடவடிக்கை: {first_action}. "
        if helpline:
            spoken_text += f"உதவி எண்: {helpline}. "
        spoken_text += "இலவச சட்ட உதவிக்கு NALSA 15100 எண்ணை அழைக்கவும்."
    elif lang_code == "te":
        spoken_text = f"న్యాయమిత్ర చట్ట మార్గదర్శకత్వం. విభాగం: {category}. "
        if first_action:
            spoken_text += f"తక్షణ చర్య: {first_action}. "
        if helpline:
            spoken_text += f"హెల్ప్‌లైన్: {helpline}. "
        spoken_text += "ఉచిత న్యాయ సహాయం కోసం నల్సా 15100 కు కాల్ చేయండి."
    elif lang_code == "bn":
        spoken_text = f"ন্যায়মিত্র আইনি নির্দেশিকা। বিষয়: {category}। "
        if first_action:
            spoken_text += f"তাৎক্ষণিক পদক্ষেপ: {first_action}। "
        if helpline:
            spoken_text += f"হেল্পলাইন: {helpline}। "
        spoken_text += "বিনামূল্যে আইনি সহায়তার জন্য নালসা ১৫১০০ এ যোগাযোগ করুন।"
    elif lang_code == "mr":
        spoken_text = f"न्यायमित्र कायदेशीर मार्गदर्शन. विषय: {category}. "
        if first_action:
            spoken_text += f"तात्काळ पाऊल: {first_action}. "
        if helpline:
            spoken_text += f"हेल्पलाइन: {helpline}. "
        spoken_text += "मोफत कायदेशीर मदतीसाठी नालसा 15100 वर संपर्क साधा."
    else:
        # Default English
        spoken_text = f"NyayaMitra legal guidance for {category}. "
        if explanation:
            spoken_text += f"{explanation[:150]}. "
        if first_action:
            spoken_text += f"Immediate action: {first_action}. "
        if helpline:
            spoken_text += f"Key helpline: {helpline}. "
        spoken_text += "For free legal aid, call NALSA Helpline 15100."

    try:
        buf = io.BytesIO()
        buf.name = "guidance.ogg"
        tts = gTTS(text=spoken_text, lang=lang_code)
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except Exception as e:
        logger.warning(f"Voice generation failed: {e}")
        return None


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
        "2. 🎙️ *Audio Voice Notes:* I send playable voice advice for every query!\n"
        "3. 📸 *Send a photo or screenshot* of a UPI receipt, bank SMS, or dispute notice for instant OCR\n"
        "4. 🌐 *Change language:* Use /language (`en`, `hi`, `ta`, `te`, `bn`, `mr`)\n"
        "5. 🔇 *Toggle Voice:* Use /voice to turn voice notes on/off\n\n"
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
        "/voice [on/off] - Toggle voice note replies\n"
        "/help - Emergency numbers & tips\n\n"
        "*Tip:* You can type or send voice notes in *Hindi, Tamil, Telugu, Bengali, Marathi, or Hinglish*!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def voice_command(update, context):
    """Toggles voice note audio responses on or off."""
    chat_id = update.effective_chat.id
    args = context.args

    if not args:
        current = "ON" if user_voice_enabled.get(chat_id, True) else "OFF"
        await update.message.reply_text(
            f"🎙️ Voice note replies are currently: *{current}*\n\n"
            "To change, use:\n"
            "• `/voice on` — Enable audio notes\n"
            "• `/voice off` — Text only",
            parse_mode="Markdown"
        )
        return

    sub = args[0].lower().strip()
    if sub in ("on", "enable", "yes", "true", "1"):
        user_voice_enabled[chat_id] = True
        await update.message.reply_text("✅ Voice note audio replies are now *ENABLED*.", parse_mode="Markdown")
    elif sub in ("off", "disable", "no", "false", "0"):
        user_voice_enabled[chat_id] = False
        await update.message.reply_text("🔇 Voice note audio replies are now *DISABLED*.", parse_mode="Markdown")
    else:
        await update.message.reply_text("Usage: `/voice on` or `/voice off`", parse_mode="Markdown")


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
            f"✅ Language set to *{LANG_CODE_MAP[code]}*. Future guidance and voice notes will be in this language.",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "Unknown code. Supported: `en`, `hi`, `ta`, `te`, `bn`, `mr`",
            parse_mode="Markdown"
        )


async def send_guidance_with_voice(update, res: dict, user_lang: str, chat_id: int):
    """Helper to send the formatted text response and accompanying voice note."""
    reply = format_telegram_response(res)
    await update.message.reply_text(reply, parse_mode="Markdown")

    # Send voice note if enabled
    if user_voice_enabled.get(chat_id, True) and GTTS_AVAILABLE:
        try:
            await update.message.chat.send_action("record_voice")
            loop = asyncio.get_event_loop()
            voice_fp = await loop.run_in_executor(None, generate_audio_summary, res, user_lang)
            if voice_fp:
                cat_name = res.get("category", "Legal Guidance")
                await update.message.reply_voice(
                    voice=voice_fp,
                    caption=f"🎙️ *{cat_name} Audio Guidance* ({user_lang})"
                )
        except Exception as ve:
            logger.warning(f"Failed to deliver voice note: {ve}")


async def handle_text_message(update, context):
    """Processes incoming citizen legal questions."""
    user_query = update.message.text.strip()
    chat_id = update.effective_chat.id
    user_lang = user_languages.get(chat_id, "English")

    if len(user_query) < 5:
        await update.message.reply_text("Please provide a little more detail about what happened.")
        return

    await update.message.chat.send_action("typing")

    try:
        detected_category = legal_retriever.detect_category(user_query)
        verified_ctx = legal_retriever.get_verified_context(detected_category, user_lang)
        res = ai_service.generate_legal_response(
            category=detected_category,
            question=user_query,
            verified_ctx=verified_ctx,
            language=user_lang
        )

        await send_guidance_with_voice(update, res, user_lang, chat_id)

    except Exception as e:
        logger.error(f"Error handling text query: {e}")
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
        photo = update.message.photo[-1]
        photo_file = await photo.get_file()
        file_bytes = await photo_file.download_as_bytearray()

        caption = update.message.caption or ""

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

        info_header = "📄 *Document OCR Extracted Details:*\n"
        if amount:
            info_header += f"• Amount: *₹{amount}*\n"
        if utr:
            info_header += f"• Reference / UTR: *{utr}*\n"
        info_header += f"• Detected Category: *{cat}*\n\n"

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

        # Also send voice note
        if user_voice_enabled.get(chat_id, True) and GTTS_AVAILABLE:
            try:
                loop = asyncio.get_event_loop()
                voice_fp = await loop.run_in_executor(None, generate_audio_summary, res, user_lang)
                if voice_fp:
                    await update.message.reply_voice(
                        voice=voice_fp,
                        caption=f"🎙️ *{cat} Audio Summary*"
                    )
            except Exception as ve:
                logger.warning(f"Voice generation for photo failed: {ve}")

    except Exception as e:
        logger.error(f"Error handling photo upload: {e}")
        await update.message.reply_text(
            "Could not parse image text completely. Please type your legal problem in text.",
            parse_mode="Markdown"
        )


async def handle_voice_message(update, context):
    """Acknowledges voice notes sent by citizens and guides them."""
    chat_id = update.effective_chat.id
    user_lang = user_languages.get(chat_id, "English")

    guide_msg = (
        "🎙️ *Voice Message Received!*\n\n"
        "NyayaMitra is listening. For highest procedural accuracy, you can also type "
        "a 1-sentence summary of your issue (e.g., _'₹15,000 debited from SBI without OTP'_).\n\n"
        "Emergency Contacts:\n"
        "• Cyber Fraud: **1930**\n"
        "• Consumer Complaints: **1915**\n"
        "• Free Legal Aid (NALSA): **15100**"
    )
    await update.message.reply_text(guide_msg, parse_mode="Markdown")


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

    print("[*] Starting NyayaMitra AI Telegram Bot with Audio Voice Note Support...")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("language", language_command))
    app.add_handler(CommandHandler("voice", voice_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice_message))

    print("[+] NyayaMitra Telegram Bot is active and listening for messages & voice notes!")
    app.run_polling()


if __name__ == "__main__":
    main()
