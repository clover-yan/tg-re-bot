import asyncio
import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.helpers import escape_markdown

load_dotenv()
os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
	raise ValueError(
	    "BOT_TOKEN is not set in environment variables or .env file")


async def re_command(update: Update,
                     context: ContextTypes.DEFAULT_TYPE) -> None:
	message = update.effective_message
	if not message:
		return

	reply = message.reply_to_message
	if not reply:
		await message.reply_text("请回复一条消息后使用 /re")
		return

	sender = message.from_user
	if not sender:
		return

	sender_name = escape_markdown(sender.full_name or "用户", version=2)
	mention_md = f"[{sender_name}](tg://user?id={sender.id})"

	replied_md = reply.text_markdown_v2 or reply.caption_markdown_v2 or ""

	if not replied_md:
		await message.reply_text("被回复的消息没有文字内容")
		return

	await message.reply_text(
	    f"{mention_md}: {replied_md}",
	    parse_mode="MarkdownV2",
	)

	try:
		await message.delete()
	except Exception:
		pass


def main() -> None:
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)

	application = Application.builder().token(BOT_TOKEN).build()
	application.add_handler(CommandHandler("re", re_command))
	application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
	main()
