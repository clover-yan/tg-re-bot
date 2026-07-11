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

_LOCALE = {
    "user": {"zh-hans": "用户", "zh-hant": "用戶", "en": "User"},
    "group": {"zh-hans": "群组", "zh-hant": "群組", "en": "Group"},
}


def _i18n(key: str, lang: str | None) -> str:
    if not lang:
        return _LOCALE[key]["zh-hans"]
    if lang.startswith("zh"):
        if "hant" in lang.replace("-", "").lower():
            return _LOCALE[key]["zh-hant"]
        if "tw" in lang.lower() or "hk" in lang.lower():
            return _LOCALE[key]["zh-hant"]
        return _LOCALE[key]["zh-hans"]
    return _LOCALE[key]["en"]


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

	if sender.id == 1087968824 and message.sender_chat:
		chat = message.sender_chat
		title = escape_markdown(message.author_signature, version=2) if message.author_signature else None
		if chat.username:
			mention_md = f"[{escape_markdown(chat.title or _i18n("group", sender.language_code), version=2)}]({chat.username})"
		else:
			mention_md = escape_markdown(chat.title or _i18n("group", sender.language_code), version=2)
		if title:
			mention_md += f" ({title})"
	else:
		sender_name = escape_markdown(sender.full_name or _i18n("user", sender.language_code), version=2)
		mention_md = f"[{sender_name}](tg://user?id={sender.id})"

	replied_md = reply.text_markdown_v2 or reply.caption_markdown_v2 or ""

	if not replied_md:
		await message.reply_text("被回复的消息没有文字内容")
		return

	reply_to = reply.reply_to_message.message_id if reply.reply_to_message else None

	try:
		await context.bot.send_message(
			chat_id=message.chat_id,
			text=f"{mention_md}: {replied_md}",
			parse_mode="MarkdownV2",
			reply_to_message_id=reply_to,
		)
	except Exception:
		await context.bot.send_message(
			chat_id=message.chat_id,
			text=f"{mention_md}: {replied_md}",
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
