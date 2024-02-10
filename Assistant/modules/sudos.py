from typing import cast

from telegram import Message, Update, User
from telegram.ext import ContextTypes

from Assistant.database.block_db import (
    add_banned_user,
    is_banned_user,
    remove_banned_user,
)
from Assistant.database.forward_db import group_off, group_on


async def mode_func(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = cast(User, update.effective_user)
    message = cast(Message, update.effective_message)
    args = context.args
    usage = "<b>ᴜsᴀɢᴇ:</b>\n\n/mode [group | private]\n\n<b>ɢʀᴏᴜᴘ</b>: ᴀʟʟ ᴛʜᴇ ɪɴᴄᴏᴍɪɴɢ ᴍᴇssᴀɢᴇs ᴡɪʟʟ ʙᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴛᴏ ʟᴏɢ ɢʀᴏᴜᴘ.\n\n<b>ᴘʀɪᴠᴀᴛᴇ</b>: ᴀʟʟ ᴛʜᴇ ɪɴᴄᴏᴍɪɴɢ messages ᴡɪʟʟ ʙᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴛᴏ ᴛʜᴇ ᴘʀɪᴠᴀᴛᴇ ᴍᴇssᴀɢᴇs ᴏғ ᴀʟʟ sᴜᴅᴏ_ᴜsᴇʀs"
    if not args:
        return await message.reply_text(usage)

    state = args[0].lower()
    if state == "group":
        await group_on()
        await message.reply_text(
            "ɢʀᴏᴜᴘ ᴍᴏᴅᴇ <b>ᴇɴᴀʙʟᴇᴅ</b>. ᴀʟʟ ᴛʜᴇ ɪɴᴄᴏᴍɪɴɢ ᴍᴇssᴀɢᴇs ᴡɪʟʟ ʙᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴛᴏ ʟᴏɢ ɢʀᴏᴜᴘ"
        )
    elif state == "private":
        await group_off()
        await message.reply_text(
            "ᴘʀɪᴠᴀᴛᴇ ᴍᴏᴅᴇ <b>ᴇɴᴀʙʟᴇᴅ</b>. ᴀʟʟ ᴛʜᴇ ɪɴᴄᴏᴍɪɴɢ ᴍᴇssᴀɢᴇs ᴡɪʟʟ ʙᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴛᴏ ᴘʀɪᴠᴀᴛᴇ ᴍᴇssᴀɢᴇ ᴏғ ᴀʟʟ sᴜᴅᴏ_ᴜsᴇʀs"
        )
    else:
        await message.reply_text(usage)


async def block_func(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = cast(Message, update.effective_message)
    if not message.reply_to_message:
        return await message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ғᴏʀᴡᴀʀᴅᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʟᴏᴄᴋ ʜɪᴍ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ"
        )
    user = message.reply_to_message.forward_from
    try:
        user_id = user.id
    except Exception as e:
        return await message.reply_text(f"ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴜsᴇʀ.\n\nᴇʀʀᴏʀ: {e}")
    bot = context.bot
    if await is_banned_user(user_id):
        return await message.reply_text("ᴀʟʀᴇᴀᴅʏ ʙʟᴏᴄᴋᴇᴅ")
    await add_banned_user(user_id)
    await message.reply_text("ʙᴀɴɴᴇᴅ ᴜsᴇʀ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ")
    try:
        await bot.send_message(
            user_id, "ʏᴏᴜ'ʀᴇ ɴᴏᴡ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ ʙʏ ᴀᴅᴍɪɴs."
        )
    except Exception:
        pass


async def unblock_func(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = cast(User, update.effective_user)
    message = cast(Message, update.effective_message)
    if not message.reply_to_message:
        return await message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ғᴏʀᴡᴀʀᴅᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ ᴜɴʙʟᴏᴄᴋ ʜɪᴍ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ"
        )
    userrr = message.reply_to_message.forward_from
    if not userrr:
        return await message.reply_text("ᴘʟᴢ ʀᴇᴘʟʏ ᴛᴏ ᴀ ғᴏʀᴡᴀʀᴅ ᴍᴇssᴀɢᴇ ")
    bot = context.bot
    if not await is_banned_user(userrr.id):
        return await message.reply_text("ᴀʟʀᴇᴀᴅʏ ᴜɴʙʟᴏᴄᴋᴇᴅ")
    await remove_banned_user(userrr.id)
    await message.reply_text("ᴜɴʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ")
    try:
        await bot.send_message(
            userrr.id,
            "ʏᴏᴜ'ʀᴇ ɴᴏᴡ ᴜɴʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ ʙʏ ᴀᴅᴍɪɴs.",
        )
    except Exception:
        pass
