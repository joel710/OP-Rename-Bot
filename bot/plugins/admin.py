
import shutil
import psutil
from pyrogram import filters
from pyrogram.types import (
    Message
)
from configs import Config
from bot.client import Client
from bot.core.db.database import db
from bot.core.display import humanbytes
from bot.core.handlers.broadcast import broadcast_handler


@Client.on_message(filters.command("status") & filters.user(Config.OWNER_ID))
async def status_handler(_, m: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    await m.reply_text(
        text=f"**Espace disque total:** {total} \n"
             f"**Espace utilisé:** {used}({disk_usage}%) \n"
             f"**Espace libre:** {free} \n"
             f"**CPU Usage:** {cpu_usage}% \n"
             f"**RAM Usage:** {ram_usage}%\n\n"
             f"**Nombre total d'utilisateurs dans la base de données:** `{total_users}`",
        parse_mode="Markdown",
        quote=True
    )


@Client.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID) & filters.reply)
async def broadcast_in(_, m: Message):
    await broadcast_handler(m)
