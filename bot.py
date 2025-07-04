from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.idle import idle
import asyncio
import random
import requests

API_ID = 18088290
API_HASH = "1b06cbb45d19188307f10bcf275341c5"
BOT_TOKEN = "7628770960:AAGmj_-7sus8JXzk65glY0KUjGOVydfEy8o"
PRIVATE_CHANNEL_ID = -1002899840201

SUPABASE_URL = "https://cjwdjcbeixwpsahuwkdb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
# (তুমি এখানে সম্পূর্ণ KEY দিও)

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🧠 Save link to Supabase
def save_to_supabase(token, msg_id):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    data = {"token": token, "msg_id": msg_id}
    requests.post(f"{SUPABASE_URL}/rest/v1/links", json=data, headers=headers)

# 🔍 Get message ID from token
def get_msg_id_from_token(token):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    params = {"token": f"eq.{token}"}
    response = requests.get(f"{SUPABASE_URL}/rest/v1/links", headers=headers, params=params)
    if response.status_code == 200 and response.json():
        return response.json()[0]["msg_id"]
    return None

# 🎬 /start handler
@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    args = message.text.split()
    if len(args) == 2:
        token = args[1]
        msg_id = get_msg_id_from_token(token)
        if msg_id:
            try:
                sent = await client.copy_message(chat_id=message.chat.id, from_chat_id=PRIVATE_CHANNEL_ID, message_id=msg_id)
                await message.reply(
                    "✅ Video sent!\n🕒 This video will be auto-deleted after 30 minutes.\n\n"
                    "✅ ভিডিও পাঠানো হয়েছে!\n⏳ এই ভিডিওটি ৩০ মিনিট পরে স্বয়ংক্রিয়ভাবে মুছে যাবে।"
                )
                await asyncio.sleep(1800)
                await sent.delete()
            except Exception as e:
                await message.reply(f"❌ ভিডিও পাঠাতে সমস্যা:\n`{e}`")
        else:
            await message.reply("⛔ Invalid or expired link.")
    else:
        await message.reply("👋 Welcome!\nSend /genlink <video link>")

# 🔗 /genlink handler
@bot.on_message(filters.command("genlink"))
async def genlink(client, message: Message):
    if len(message.command) < 2:
        await message.reply("⚠️ Usage: /genlink <video link>")
        return

    link = message.command[1]
    if not link.startswith("https://t.me/c/"):
        await message.reply("❌ Invalid link format.")
        return

    try:
        msg_id = int(link.split("/")[-1])
        token = str(random.randint(100000, 999999))
        save_to_supabase(token, msg_id)
        bot_username = (await client.get_me()).username
        deep_link = f"https://t.me/{bot_username}?start={token}"
        await message.reply(f"✅ ভিডিও লিংক তৈরি হয়েছে:\n🔗 {deep_link}")
    except Exception as e:
        await message.reply(f"❌ Error:\n`{e}`")
