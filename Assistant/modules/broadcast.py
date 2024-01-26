import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from Assistant import SUDO_USERS, Abishnoi
from Assistant.database.block_db import get_banned_users
from Assistant.database.users_db import get_served_users


@Abishnoi.on_message(filters.command("stats") & filters.user(SUDO_USERS))
async def stats(client: Abishnoi, message: Message):
    users = len(await get_served_users())
    chats = len(await get_banned_users())
    await message.reply_text(
        f"<u><b>ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛs ᴏғ {client.me.mention} :</b></u>\n\n➻ <b>ʙʟᴏᴄᴋᴇᴅ:</b> {chats}\n➻ <b>ᴜsᴇʀs :</b> {users}\n"
    )


@Abishnoi.on_message(filters.command("broadcast") & filters.user(SUDO_USERS))
async def broadcast(cli: Abishnoi, message: Message):
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
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
                await cli.copy_message(chat_id=i, from_chat_id=y, message_id=x)
                if message.reply_to_message
                else await cli.send_message(i, text=query)
            )
            susr += 1
            await asyncio.sleep(0.2)
        except FloodWait as e:
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
