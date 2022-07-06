
from bot.client import Client
from pyrogram import filters
from pyrogram import types
from bot.core.db.add import add_user_to_database


@Client.on_message(filters.command(["start", "ping"]) & filters.private)
async def ping_handler(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("je ne sais pas pour vous monsieur :(")
    await add_user_to_database(c, m)
    await c.send_flooded_message(
        chat_id=m.chat.id,
        text="<b>𝙷𝙴𝚈 je suis renommer bot!</b>\n\n"
             "<b> Je peux renommer le média sans le télécharger!</b>\n"
             "<b>la vitesse dépend de votre support DC.</b>\n\n"
             "<b>envoyez-moi simplement des médias et répondez-y avec /rename 𝙲𝙾𝙼𝙼𝙰𝙽𝙳E.</b>",
        reply_markup=types.InlineKeyboardMarkup([[
           types.InlineKeyboardButton("paramètres du bot",
                                      callback_data="showSettings")
        ]])
    )


@Client.on_message(filters.command("help") & filters.private)
async def help_handler(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("I don't know about you sar :(")
    await add_user_to_database(c, m)
    await c.send_flooded_message(
        chat_id=m.chat.id,
        text="<b>je peux renommer le média sans le télécharger!</b>\n"
             "<b>la vitesse dépend de votre support DC.</b>\n\n"
             "<b>envoyez-moi simplement des médias et répondez-y avec /rename 𝙲𝙾𝙼𝙼𝙰𝙽𝙳E.</b>\n\n"
             "<b>pour définir une réponse miniature personnalisée à n'importe quelle image avec/set_thumbnail</b>\n\n"
             "<b>pour voir la vignette personnalisée, appuyez sur /show_thumbnail</b>",
        reply_markup=types.InlineKeyboardMarkup([[
           types.InlineKeyboardButton("parametres du bot",
                                      callback_data="showSettings")]])
    )
