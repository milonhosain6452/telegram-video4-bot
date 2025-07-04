from flask import Flask
import asyncio
from pyrogram import idle
from bot import bot

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running with Flask + Render!"

async def start_bot():
    await bot.start()
    print("✅ Bot started.")
    await idle()
    await bot.stop()

def run_all():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(start_bot())
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    run_all()
