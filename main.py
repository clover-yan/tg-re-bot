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


def _schedule_delete(message, delay: float = 5.0) -> None:

	async def _delete_later() -> None:
		await asyncio.sleep(delay)
		try:
			await message.delete()
		except Exception:
			pass

	asyncio.create_task(_delete_later())


_LOCALE = {
    "user": {
        "zh-hans": "用户",
        "zh-hant": "用戶",
        "en": "User"
    },
    "group": {
        "zh-hans": "群组",
        "zh-hant": "群組",
        "en": "Group"
    },
    "not_replying": {
        "zh-hans": "请使用 /re 回复一条消息",
        "zh-hant": "請使用 /re 回覆一條消息",
        "en": "Please reply to a message with /re"
    },
    "no_text": {
        "zh-hans": "被回复的消息没有文字内容",
        "zh-hant": "被回覆的消息沒有文字內容",
        "en": "The replied message has no text content"
    },
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
		warning = await message.reply_text(
		    _i18n("not_replying", message.from_user.language_code))
		_schedule_delete(warning)
		return

	sender = message.from_user
	if not sender:
		return

	if sender.id == 1087968824 and message.sender_chat:
		chat = message.sender_chat
		title = escape_markdown(
		    message.author_signature,
		    version=2) if message.author_signature else None
		if chat.username:
			mention_md = f'[{escape_markdown(chat.title or _i18n("group", sender.language_code), version=2)}](https://t.me/{chat.username})'
		else:
			mention_md = escape_markdown(
			    chat.title or _i18n("group", sender.language_code), version=2)
		if title:
			mention_md += f" \\({title}\\)"
	else:
		sender_name = escape_markdown(sender.full_name
		                              or _i18n("user", sender.language_code),
		                              version=2)
		mention_md = f"[{sender_name}](tg://user?id={sender.id})"

	replied_md = reply.text_markdown_v2 or reply.caption_markdown_v2 or ""

	if not replied_md:
		warning = await message.reply_text(
		    _i18n("no_text", message.from_user.language_code))
		_schedule_delete(warning)
		return

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
