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
API_HASH = os.environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
TOKEN = os.environ.get("TOKEN", None)
TAG = os.environ.get("TAG", None)
OWNER_ID = int(os.environ.get("OWNER_ID", 1382528596))


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
   await message.reply(f"Salam {message.from_user.mention}\nGrupumuza qatıl",
         reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("ᴍᴀғɪᴀ sᴛ✩ᴛᴇ", url="t.me/NewMafiaState")],
            [InlineKeyboardButton("ᴍᴀғɪᴀ sᴛ✩ᴛᴇ", url="t.me/https://t.me/StateTagBot?startgroup=a")]
            
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
👋 **Salam {message.from_user.mention}**
ᴍᴀғɪᴀ sᴛ✩ᴛᴇ Grupuna xoş gəldin

Grupun qaydalarına əsasən aramıza qatılmaq üçün
Adınızın Qabağına Qrup tağını yazmalısınız.

**Group Tağımız:** `{TAG}`
**Nümunə:** `Şamil ¦ sᴛ✩ᴛᴇ

**Tağı yazdınsa __🔊 SƏSMİ AÇ__ düyməsinə kliklə**
"""
       await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔊 Səsimi aç", callback_data="unmute")]
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
      await cb.answer("Səsiniz uğurla açıldı!")
      await cb.message.delete("Təşəkkürlər")
      return
    await cb.answer("Tağı yazmadan səsi aça bilmərsən! 😎", show_alert=True)


tagcheck.run()
