from datetime import datetime, timedelta

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN, GROUP_ID
from filters import Admin
from bad_words import bad_words

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.filters_factory.bind(Admin)


@dp.message_handler()
async def filter_message(message: types.Message):
    for words in bad_words:
        if words in message.text:
            await message.delete()


@dp.message_handler(content_types=["new_chat_members"])
async def on_user_join(message: types.Message):
    await message.delete()


@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!")
async def ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Оберіть повідомлення потенційного порушника")
        return

    await message.bot.delete_message(chat_id=GROUP_ID, message.message_id)
    await message.bot.kick_chat_member(chat_id=GROUP_ID, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply("Користувач забанен")


@dp.message_handler(is_admin=True, commands=["mute"])
async def mute(message):
    name = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
        await message.reply("Оберіть повідомлення потенційного порушника")
        return
    try:
        muteint = int(message.text.split()[1])
        mutetype = message.text.split()[2]
        comment = " ".join(message.text.split()[3:])
    except Exception:
        await message.reply('Невiрно!\nПриклад:\n`/mute 1 ч причина`')
        return
    if mutetype == "ч":
        dt = datetime.now() + timedelta(hours=muteint)
        timestamp = dt.timestamp()
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                       types.ChatPermissions(False), until_date=timestamp)
        await message.reply(
            f' | {name}\n | </a>\n⏰ | <b>Термін покарання:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
            parse_mode='html')
    elif mutetype == "м":
        dt = datetime.now() + timedelta(minutes=muteint)
        timestamp = dt.timestamp()
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                       types.ChatPermissions(False), until_date=timestamp)
        await message.reply(
            f' | {name}\n | </a>\n⏰ | <b>Термін покарання:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
            parse_mode='html')
    elif mutetype == "д":
        dt = datetime.now() + timedelta(days=muteint)
        timestamp = dt.timestamp()
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                       types.ChatPermissions(False), until_date=timestamp)
        await message.reply(
            f' | {name}\n | </a>\n⏰ | <b>Термін покарання:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
            parse_mode='html')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
