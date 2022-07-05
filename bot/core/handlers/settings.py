# (c) @AbirHasan2005

import asyncio
from pyrogram import types, errors
from configs import Config
from bot.core.db.database import db


async def show_settings(m: "types.Message"):
    usr_id = m.chat.id
    user_data = await db.get_user_data(usr_id)
    if not user_data:
        await m.edit("Failed to fetch your data from database!")
        return
    upload_as_doc = user_data.get("upload_as_doc", True)
    caption = user_data.get("caption", None)
    apply_caption = user_data.get("apply_caption", True)
    thumbnail = user_data.get("thumbnail", None)
    buttons_markup = [
        [types.InlineKeyboardButton(f"téléchargé en tant que document {'✅' if upload_as_doc else '🗑️'}",
                                    callback_data="triggerUploadMode")],
        [types.InlineKeyboardButton(f"appliquer la légende {'✅' if apply_caption else '🗑️'}",
                                    callback_data="triggerApplyCaption")],
        [types.InlineKeyboardButton(f"appliquer la légende par défaut {'🗑️' if caption else '✅'}",
                                    callback_data="triggerApplyDefaultCaption")],
        [types.InlineKeyboardButton("définir une légende personnalisée",
                                    callback_data="setCustomCaption")],
        [types.InlineKeyboardButton(f"{'𝙲𝙷𝙰𝙽𝙶𝙴' if thumbnail else '𝚂𝙴𝚃'} 𝚃𝙷𝚄𝙼𝙱𝙽𝙰𝙸𝙻",
                                    callback_data="setThumbnail")]
    ]
    if thumbnail:
        buttons_markup.append([types.InlineKeyboardButton("afficher la vignette",
                                                          callback_data="showThumbnail")])
    if caption:
        buttons_markup.append([types.InlineKeyboardButton("afficher la légende",
                                                          callback_data="showCaption")])
    buttons_markup.append([types.InlineKeyboardButton("fermer",
                                                      callback_data="closeMessage")])

    try:
        await m.edit(
            text="**- personnaliser les paramètres du bot -**",
            reply_markup=types.InlineKeyboardMarkup(buttons_markup),
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )
    except errors.MessageNotModified: pass
    except errors.FloodWait as e:
        await asyncio.sleep(e.x)
        await show_settings(m)
    except Exception as err:
        Config.LOGGER.getLogger(__name__).error(err)
