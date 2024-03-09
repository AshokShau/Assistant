from typing import cast

from telegram import Message, Update
from telegram.ext import ContextTypes

import config
from Assistant import LOGGER, SUDO_USERS
from Assistant.database.block_db import is_banned_user
from Assistant.database.forward_db import is_group


async def incoming_groups(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot
    message = cast(Message, update.effective_message)
    if not await is_group():
        return None
    if reply := message.reply_to_message:
        if reply.forward_origin.type == "user":
            user = reply.forward_origin.sender_user
            if not user:
                return None

        try:
            return await bot.copy_message(
                user.id,
                message.chat.id,
                message.id,
            )
        except Exception as e:
            LOGGER.warning(str(e))
            return await message.reply_text(f"ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ\n\nᴇʀʀᴏʀ:{e} ")


async def incoming_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot
    message = cast(Message, update.effective_message)
    if await is_banned_user(message.from_user.id):
        return None
    if message.from_user.id in SUDO_USERS:
        if reply := message.reply_to_message:
            if reply.forward_origin.type == "user":
                user = reply.forward_origin.sender_user
                if not user:
                    return None

            try:
                return await bot.copy_message(
                    user.id,
                    message.chat.id,
                    message.id,
                )
            except Exception as e:
                LOGGER.warning(str(e))
                return await message.reply_text(
                    f"ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ\n\nᴇʀʀᴏʀ:{e} "
                )
    elif await is_group():
        await bot.forward_messages(
            chat_id=config.LOGGER_ID,
            from_chat_id=message.chat_id,
            message_id=message.message_id,
        )
    else:
        for x in SUDO_USERS:
            try:
                await bot.forward_message(
                    chat_id=x,
                    from_chat_id=message.chat_id,
                    message_id=message.message_id,
                )
            except Exception as e:
                LOGGER.warning(str(e))
