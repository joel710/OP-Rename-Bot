
from pyrogram import types
from bot.client import Client
from bot.core.db.database import db
from bot.core.file_info import (
    get_media_file_name,
    get_media_file_size,
    get_file_type,
    get_file_attr
)
from bot.core.display import humanbytes
from bot.core.handlers.settings import show_settings


@Client.on_callback_query()
async def cb_handlers(c: Client, cb: "types.CallbackQuery"):
    if cb.data == "showSettings":
        await cb.answer()
        await show_settings(cb.message)
    elif cb.data == "showThumbnail":
        thumbnail = await db.get_thumbnail(cb.from_user.id)
        if not thumbnail:
            await cb.answer("vous n'avez défini aucune vignette personnalisée!", show_alert=True)
        else:
            await cb.answer()
            await c.send_photo(cb.message.chat.id, thumbnail, "vignette personnalisée",
                               reply_markup=types.InlineKeyboardMarkup([[
                                   types.InlineKeyboardButton(" supprimer la vignette",
                                                              callback_data="deleteThumbnail")
                               ]]))
    elif cb.data == "deleteThumbnail":
        await db.set_thumbnail(cb.from_user.id, None)
        await cb.answer("𝙾𝙺𝙰𝚈, j'ai supprimé votre vignette personnalisée. maintenant t appliquera la vignette par défaut.", show_alert=True)
        await cb.message.delete(True)
    elif cb.data == "setThumbnail":
        await cb.answer()
        await cb.message.edit("envoyez-moi une photo pour la définir comme vignette personnalisée.\n\n"
                              "appuyez /cancel pour annuler le processus..")
        from_user_thumb: "types.Message" = await c.listen(cb.message.chat.id)
        if not from_user_thumb.photo:
            await cb.message.edit("<b>processus annulé</b>")
            return await from_user_thumb.continue_propagation()
        else:
            await db.set_thumbnail(cb.from_user.id, from_user_thumb.photo.file_id)
            await cb.message.edit("𝙾𝙺𝙰𝚈!\n"
                                  "maintenant, je vais appliquer cette vignette à la prochaine 𝚄𝙿𝙻𝙾𝙰𝙳𝚂.",
                                  reply_markup=types.InlineKeyboardMarkup(
                                      [[types.InlineKeyboardButton("paramètres du bot",
                                                                   callback_data="showSettings")]]
                                  ))
    elif cb.data == "setCustomCaption":
        await cb.answer()
        await cb.message.edit("Okay,\n"
                              " envoyez-moi votre légende personnalisée.\n\n"
                              "appuyez /cancel pour annuler le processus..")
        user_input_msg: "types.Message" = await c.listen(cb.message.chat.id)
        if not user_input_msg.text:
            await cb.message.edit("<b>processus annulé</b>")
            return await user_input_msg.continue_propagation()
        if user_input_msg.text and user_input_msg.text.startswith("/"):
            await cb.message.edit("<b>processus annulé</b>")
            return await user_input_msg.continue_propagation()
        await db.set_caption(cb.from_user.id, user_input_msg.text.markdown)
        await cb.message.edit("légende personnalisée ajoutée avec succès!",
                              reply_markup=types.InlineKeyboardMarkup(
                                  [[types.InlineKeyboardButton("paramètres du bot",
                                                               callback_data="showSettings")]]
                              ))
    elif cb.data == "triggerApplyCaption":
        await cb.answer()
        apply_caption = await db.get_apply_caption(cb.from_user.id)
        if not apply_caption:
            await db.set_apply_caption(cb.from_user.id, True)
        else:
            await db.set_apply_caption(cb.from_user.id, False)
        await show_settings(cb.message)
    elif cb.data == "triggerApplyDefaultCaption":
        await db.set_caption(cb.from_user.id, None)
        await cb.answer("𝙾𝙺𝙰𝚈,  Maintenant, je conserverai la légende par défaut.", show_alert=True)
        await show_settings(cb.message)
    elif cb.data == "showCaption":
        caption = await db.get_caption(cb.from_user.id)
        if not caption:
            await cb.answer("vous n'avez défini aucune légende personnalisée!", show_alert=True)
        else:
            await cb.answer()
            await cb.message.edit(
                text=caption,
                parse_mode="Markdown",
                reply_markup=types.InlineKeyboardMarkup([[
                    types.InlineKeyboardButton("𝙱𝙰𝙲𝙺", callback_data="showSettings")
                ]])
            )
    elif cb.data == "triggerUploadMode":
        await cb.answer()
        upload_as_doc = await db.get_upload_as_doc(cb.from_user.id)
        if upload_as_doc:
            await db.set_upload_as_doc(cb.from_user.id, False)
        else:
            await db.set_upload_as_doc(cb.from_user.id, True)
        await show_settings(cb.message)
    elif cb.data == "showFileInfo":
        replied_m = cb.message.reply_to_message
        _file_name = get_media_file_name(replied_m)
        text = f"**𝙵𝙸𝙻𝙴 𝙽𝙰𝙼𝙴 :** `{_file_name}`\n\n" \
               f"**𝙵𝙸𝙻𝙴 𝙴𝚇𝚃𝙴𝙽𝚂𝙸𝙾𝙽 :** `{_file_name.rsplit('.', 1)[-1].upper()}`\n\n" \
               f"**𝙵𝙸𝙻𝙴 𝚃𝚈𝙿𝙴 :** `{get_file_type(replied_m).upper()}`\n\n" \
               f"**𝙵𝙸𝙻𝙴 𝚂𝙸𝚉𝙴 :** `{humanbytes(get_media_file_size(replied_m))}`\n\n" \
               f"**𝙵𝙸𝙻𝙴 𝙵𝙾𝚁𝙼𝙰𝚃 :** `{get_file_attr(replied_m).mime_type}`"
        await cb.message.edit(
            text=text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton("𝙲𝙻𝙾𝚂𝙴", callback_data="closeMessage")]]
            )
        )
    elif cb.data == "closeMessage":
        await cb.message.delete(True)
