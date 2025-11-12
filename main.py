import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8535752721:AAGRxeom-zSe-3WPomLbwl33aCvH8ICPVHM"  # এখানে তোমার BotFather token বসাও

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"👋 Welcome, {user.first_name}!

"
        f"🆔 Your User ID: {user.id}
"
        f"🤖 Host & Run Python (.py) or ZIP (.zip) files.

"
        f"📩 Send your file to begin."
    )
    await update.message.reply_text(text)

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_name = update.message.document.file_name
    await file.download_to_drive(file_name)

    await update.message.reply_text(f"✅ File `{file_name}` uploaded successfully!")

    if file_name.endswith(".py"):
        try:
            result = subprocess.run(
                ["python3", file_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout or result.stderr
            await update.message.reply_text(f"📜 Output:\n{output[:4000]}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    else:
        await update.message.reply_text("📦 ZIP file uploaded (not auto-run).")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Commands:\n/start - Welcome\n/help - Help\nUpload a .py file to run it.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

print("🚀 Bot is running...")
app.run_polling()
