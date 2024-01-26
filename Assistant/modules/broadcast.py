import asyncio
from typing import cast

from telegram import Message, Update, error
from telegram.ext import ContextTypes
from telegram.helpers import mention_html

from Assistant.database.block_db import get_banned_users
from Assistant.database.users_db import get_served_users


async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await cast(Message, update.effective_message).reply_document(document="log.txt")
    except Exception:
        await cast(Message, update.effective_message).reply_text("404: ɴᴏᴛ ғᴏᴜɴᴅ ")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = cast(Message, update.effective_message)
    bot = context.bot
    users = len(await get_served_users())
    blacked = len(await get_banned_users())
    await message.reply_text(
        f"<u><b>ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛs ᴏғ {mention_html(bot.id, bot.first_name)} :</b></u>\n\n➻ <b>ʙʟᴏᴄᴋᴇᴅ:</b> {blacked}\n➻ <b>ᴜsᴇʀs :</b> {users}\n"
    )


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = cast(Message, update.effective_message)
    bot, args = context.bot, context.args
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if not args and not message.reply_to_message:
            return await message.reply_text(
                "<b>ᴇxᴀᴍᴘʟᴇ </b>:\n/broadcast [ᴍᴇssᴀɢᴇ] ᴏʀ [ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ]"
            )
        query = message.text.split(None, 1)[1]
    susr = 0
    served_users = []
    susers = await get_served_users()
    for user in susers:
        served_users.append(int(user["user_id"]))
    for i in served_users:
        try:
            m = (
                await bot.copy_message(chat_id=i, from_chat_id=y, message_id=x)
                if message.reply_to_message
                else await bot.send_message(i, text=query)
            )
            susr += 1
            await asyncio.sleep(0.3)
        except error.RetryAfter as e:
            flood_time = int(e.value)
            if flood_time > 200:
                continue
            await asyncio.sleep(flood_time)
        except:
            continue

    try:
        await message.reply_text(f"<b>ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ {susr} ᴜsᴇʀs.</b>")
    except:
        pass
