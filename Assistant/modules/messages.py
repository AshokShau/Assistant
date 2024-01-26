from pyrogram import filters
from pyrogram.types import Message

import config
from Assistant import LOGGER, SUDO_USERS, Abishnoi
from Assistant.database.block_db import is_banned_user
from Assistant.database.forward_db import is_group


@Abishnoi.on_message(filters.group & filters.user(SUDO_USERS), group=1)
async def incoming_groups(app: Abishnoi, message: Message):
    if not await is_group():
        return
    if message.reply_to_message:
        if (
            message.text == "/unblock"
            or message.text == "/block"
            or message.text == "/broadcast"
            or message.text == "/stats"
        ):
            return
        user = message.reply_to_message.forward_from
        if not user:
            return
        user_id = user.id
        try:
            return await app.copy_message(
                user_id,
                message.chat.id,
                message.id,
            )
        except Exception as e:
            return await message.reply_text(f"ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ\n\nᴇʀʀᴏʀ:{e} ")


@Abishnoi.on_message(filters.private & ~filters.me, group=-1)
async def incoming_private(app: Abishnoi, message):
    if await is_banned_user(message.from_user.id):
        return
    if message.from_user.id in SUDO_USERS:
        if message.reply_to_message:
            if (
                message.text == "/unblock"
                or message.text == "/block"
                or message.text == "/broadcast"
                or message.text == "/stats"
            ):
                return
            user = message.reply_to_message.forward_from
            if not user:
                return
            user_id = user.id
            try:
                return await app.copy_message(
                    user_id,
                    message.chat.id,
                    message.id,
                )
            except Exception as e:
                return await message.reply_text(
                    f"ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ\n\nᴇʀʀᴏʀ:{e} "
                )
    else:
        if await is_group():
            if message.text == "/start" or message.text == "/help":
                return
            await app.forward_messages(
                config.LOGGER_ID,
                message.chat.id,
                message.id,
            )
        else:
            if message.text == "/start" or message.text == "/help":
                return
            for user in SUDO_USERS:
                try:
                    await app.forward_messages(user, message.chat.id, message.id)
                except Exception as e:
                    LOGGER.error(f"{e}")
