from pyrogram import filters
from pyrogram.types import Message

from Assistant import SUDO_USERS, Abishnoi
from Assistant.database.block_db import (
    add_banned_user,
    is_banned_user,
    remove_banned_user,
)
from Assistant.database.forward_db import group_off, group_on


@Abishnoi.on_message(filters.command("mode") & filters.user(SUDO_USERS))
async def mode_func(_, message: Message):
    usage = "**ᴜsᴀɢᴇ:**\n\n/mode [group | private]\n\n**ɢʀᴏᴜᴘ**: ᴀʟʟ ᴛʜᴇ ɪɴᴄᴏᴍɪɴɢ ᴍᴇssᴀɢᴇs ᴡɪʟʟ ʙᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴛᴏ ʟᴏɢ ɢʀᴏᴜᴘ.\n\n**ᴘʀɪᴠᴀᴛᴇ**: ᴀʟʟ ᴛʜᴇ ɪɴᴄᴏᴍɪɴɢ messages ᴡɪʟʟ ʙᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴛᴏ ᴛʜᴇ ᴘʀɪᴠᴀᴛᴇ ᴍᴇssᴀɢᴇs ᴏғ ᴀʟʟ sᴜᴅᴏ_ᴜsᴇʀs"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "group":
        await group_on()
        await message.reply_text(
            "ɢʀᴏᴜᴘ ᴍᴏᴅᴇ **ᴇɴᴀʙʟᴇᴅ**. ᴀʟʟ ᴛʜᴇ ɪɴᴄᴏᴍɪɴɢ ᴍᴇssᴀɢᴇs ᴡɪʟʟ ʙᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴛᴏ ʟᴏɢ ɢʀᴏᴜᴘ"
        )
    elif state == "private":
        await group_off()
        await message.reply_text(
            "ᴘʀɪᴠᴀᴛᴇ ᴍᴏᴅᴇ **ᴇɴᴀʙʟᴇᴅ**. ᴀʟʟ ᴛʜᴇ ɪɴᴄᴏᴍɪɴɢ ᴍᴇssᴀɢᴇs ᴡɪʟʟ ʙᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴛᴏ ᴘʀɪᴠᴀᴛᴇ ᴍᴇssᴀɢᴇ ᴏғ ᴀʟʟ sᴜᴅᴏ_ᴜsᴇʀs"
        )
    else:
        await message.reply_text(usage)


@Abishnoi.on_message(filters.command("block") & filters.user(SUDO_USERS))
async def block_func(app: Abishnoi, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.forward_from
        try:
            user_id = user.id
        except Exception as e:
            return await message.reply_text(f"ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴜsᴇʀ.\n\nᴇʀʀᴏʀ: {e}")
        if await is_banned_user(user_id):
            return await message.reply_text("ᴀʟʀᴇᴀᴅʏ ʙʟᴏᴄᴋᴇᴅ")
        else:
            await add_banned_user(user_id)
            await message.reply_text("ʙᴀɴɴᴇᴅ ᴜsᴇʀ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ")
            try:
                await app.send_message(
                    user_id, "ʏᴏᴜ'ʀᴇ ɴᴏᴡ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ ʙʏ ᴀᴅᴍɪɴs."
                )
            except:
                pass
    else:
        return await message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ғᴏʀᴡᴀʀᴅᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʟᴏᴄᴋ ʜɪᴍ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ"
        )


@Abishnoi.on_message(filters.command("unblock") & filters.user(SUDO_USERS))
async def unblock_func(app: Abishnoi, message: Message):
    if message.reply_to_message:
        userrr = message.reply_to_message.forward_from
        if not userrr:
            return await message.reply_text("ᴘʟᴢ ʀᴇᴘʟʏ ᴛᴏ ᴀ ғᴏʀᴡᴀʀᴅ ᴍᴇssᴀɢᴇ ")
        if not await is_banned_user(userrr.id):
            return await message.reply_text("ᴀʟʀᴇᴀᴅʏ ᴜɴʙʟᴏᴄᴋᴇᴅ")
        else:
            await remove_banned_user(userrr.id)
            await message.reply_text("ᴜɴʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ")
            try:
                await app.send_message(
                    userrr.id,
                    "ʏᴏᴜ'ʀᴇ ɴᴏᴡ ᴜɴʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ ʙʏ ᴀᴅᴍɪɴs.",
                )
            except:
                pass
    else:
        return await message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ғᴏʀᴡᴀʀᴅᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ ᴜɴʙʟᴏᴄᴋ ʜɪᴍ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ"
        )
