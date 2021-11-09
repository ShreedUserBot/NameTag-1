from pyrogram import filters, Client
import logging
import os
from pyrogram.types import (
   ChatPermissions,
   InlineKeyboardButton,
   InlineKeyboardMarkup
)

logging.basicConfig(level=logging.INFO)

API_ID = int(os.environ.get("API_ID", 6))
API_HASH = os.environ.get("API_HASH", "dgajqls0ka18kak18841kl")
TOKEN = os.environ.get("TOKEN", None)
TAG = os.environ.get("TAG", None)
OWNER_ID = int(os.environ.get("OWNER_ID", 1382528596))
GROUP = os.environ.get("GROUP", "Qrupunuzun adını bura yazın")
ADD_BUTTON = os.environ.get("ADD_BUTTON", "Qrupa əlavə et")
GROUP_URL = os.environ.get("GROUP_URL", "Qroup Linkini bura yazın)
BAN_MSG = os.environ.get("BAN_MSG")
UN_BAN = os.environ.get("UN_BAN", "🔊 Səsimi aç")


tagcheck = Client(
   "tagcheck",
   bot_token=TOKEN,
   api_id=API_ID,
   api_hash=API_HASH
)

user_s = {}

async def is_admin(message):
    user = await tagcheck.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in ("administrator", "creator"):
      return True
    return False

@tagcheck.on_message(filters.command("start"))
async def start(_, message):
   await message.reply(f"Salam {message.from_user.mention} bu bot {GROUP} üçün hazırlanmışdır\nGrupumuza qatıl",
         reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{GROUP}", url=f"{GROUP_URL}")],
            [InlineKeyboardButton(F"{ADD_BUTTON}", url=f"{GROUP_URL}?startgroup=a")]
            
           ]
         ))

@tagcheck.on_message(filters.group)
async def tag_check(_, message):
    if await is_admin(message):
       return
    user = message.from_user.id
    if TAG not in message.from_user.first_name:
       await tagcheck.restrict_chat_member(
        message.chat.id,
        user,
        ChatPermissions(),
       )
       text = f"""
{BAN_MSG}
"""
       await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{UN_BAN}", callback_data="unmute")]
           ]
         )
       )
       user_s.update({"user_id": user})

@tagcheck.on_callback_query(filters.regex("unmute"))
async def unmute(client, cb):
    try:
       user = user_s["user_id"]
    except KeyError:
      await cb.answer(
        "Ayda!\nDeyəsən ID`zi serverden itirdim\nSəsinizi açmaq üçün adminlərə müraciət edin", 
        show_alert=True
      )
      return
    if cb.from_user.id != user:
      await cb.answer("Bu Düymə sizin üçün deyil!", show_alert=True)
      return

    if TAG in cb.from_user.first_name:
      await tagcheck.unban_chat_member(cb.message.chat.id, user)
      await cb.answer("Aramıza qatıldığın üçün təşəkkürlər 🥳\nAramıza Xoş Gəldin❤ ", show_alert=True)
      await cb.message.delete()
      return
    await cb.answer("Klan tağını yazmadan bu düymədən istifadə edə bilmərsiniz❗️", show_alert=True)


tagcheck.run()
