from . import db

modelist = {}
modedb = db["mode"]


async def is_group() -> bool:
    chat_id = 123
    mode = modelist.get(chat_id)
    if not mode:
        user = await modedb.find_one({"chat_id": chat_id})
    if not user:
        modelist[chat_id] = False
        return False
    return mode


async def group_on():
    chat_id = 123
    modelist[chat_id] = True
    user = await modedb.find_one({"chat_id": chat_id})
    if not user:
        return await modedb.insert_one({"chat_id": chat_id})


async def group_off():
    chat_id = 123
    modelist[chat_id] = False
    user = await modedb.find_one({"chat_id": chat_id})
    if user:
        return await modelist.delete_one({"chat_id": chat_id})
