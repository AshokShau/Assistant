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
            return None

        user_id = user.id
        try:
            return await bot.copy_message(
                user_id,
                message.chat.id,
                message.id,
            )
        except Exception as e:
            return await message.reply_text(f"ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ\n\nᴇʀʀᴏʀ:{e} ")


async def incoming_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot
    message = cast(Message, update.effective_message)
    if await is_banned_user(message.from_user.id):
        return None
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
                return None
            user_id = user.id
            try:
                return await bot.copy_message(
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
            await bot.forward_messages(
                chat_id=config.LOGGER_ID,
                from_chat_id=message.chat_id,
                message_id=message.message_id,
            )
        else:
            if message.text == "/start" or message.text == "/help":
                return
            for x in SUDO_USERS:
                try:
                    await bot.forward_message(
                        chat_id=x,
                        from_chat_id=message.chat_id,
                        message_id=message.message_id,
                    )
                except Exception as e:
                    LOGGER.warning(f"{e}")
