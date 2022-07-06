
from bot.client import Client
from pyrogram import filters
from pyrogram import types
from bot.core.db.database import db
from bot.core.db.add import add_user_to_database


@Client.on_message(filters.command("show_thumbnail") & filters.private)
async def show_thumbnail(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("I don't know about you sir :(")
    await add_user_to_database(c, m)
    thumbnail = await db.get_thumbnail(m.from_user.id)
    if not thumbnail:
        return await m.reply_text("vous n'avez pas défini de vignette personnalisée!")
    await c.send_photo(m.chat.id, thumbnail, caption="𝙲𝚄𝚂𝚃𝙾𝙼 𝚃𝙷𝚄𝙼𝙱𝙽𝙰𝙸𝙻!",
                       reply_markup=types.InlineKeyboardMarkup(
                           [[types.InlineKeyboardButton("supprimer la vignette!",
                                                        callback_data="deleteThumbnail")]]
                       ))


@Client.on_message(filters.command("set_thumbnail") & filters.private)
async def set_thumbnail(c: Client, m: "types.Message"):
    if (not m.reply_to_message) or (not m.reply_to_message.photo):
        return await m.reply_text("répondez à n'importe quelle image pour l'enregistrer en tant que vignette personnalisée!!")
    if not m.from_user:
        return await m.reply_text("I don't know about you sar :(")
    await add_user_to_database(c, m)
    await db.set_thumbnail(m.from_user.id, m.reply_to_message.photo.file_id)
    await m.reply_text("Okay,\n"
                       "Je vais utiliser cette image comme vignette personnalisée.",
                       reply_markup=types.InlineKeyboardMarkup(
                           [[types.InlineKeyboardButton("supprimer la vignette!",
                                                        callback_data="deleteThumbnail")]]
                       ))


@Client.on_message(filters.command("delete_thumbnail") & filters.private)
async def delete_thumbnail(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("I don't know about you sar :(")
    await add_user_to_database(c, m)
    await db.set_thumbnail(m.from_user.id, None)
    await m.reply_text("𝙾𝙺𝙰𝚈,\n"
                       " je supprime la vignette personnalisée de la base de données.")
