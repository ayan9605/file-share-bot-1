from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from supabase import create_client
import random, string
import config

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def gen_code(num=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=num))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to QuickShare Bot! Send a file to get a shareable code.")

async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.photo[-1] if update.message.photo else update.message.video
    code = gen_code()
    msg = await file.forward(chat_id=config.CHANNEL_ID)
    supabase.table("files").insert({
        "id": code,
        "file_type": file.mime_type if hasattr(file, "mime_type") else "unknown",
        "channel_msg_id": msg.message_id,
        "uploaded_by": str(update.message.from_user.id),
    }).execute()
    await update.message.reply_text(
        f"✅ Alright!\nDownload code: {code}\nUse /get {code} later", parse_mode="Markdown"
    )

async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usage: /get <code>")
        return
    code = context.args[0]
    res = supabase.table("files").select("*").eq("id", code).execute()
    if not res.data:
        await update.message.reply_text("❌ Invalid or expired code.")
        return
    msg_id = res.data[0]["channel_msg_id"]
    await context.bot.copy_message(
        chat_id=update.effective_chat.id,
        from_chat_id=config.CHANNEL_ID,
        message_id=msg_id
    )

# ✅ This is the correct syntax to start the bot
if name == "main":
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get", get_file))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.Photo.ALL | filters.Video.ALL, upload_file))
    app.run_polling()
