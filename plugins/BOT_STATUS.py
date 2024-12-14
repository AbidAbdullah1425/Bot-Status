from pyrogram import Client, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import ClientSession
from datetime import datetime, timedelta
from database.database import Database
from config import API_ID, API_HASH, BOT_TOKEN, UPDATE_CHANNEL, OWNER

from bot import Bot

# Initialize MongoDB Database
db = Database()
# Initialize scheduler
scheduler = AsyncIOScheduler()

# Utility function to fetch current time
def current_time():
    return datetime.utcnow()

# Calculate uptime
def calculate_uptime(start_time):
    if not start_time:
        return "N/A"
    delta = datetime.utcnow() - start_time
    days, seconds = delta.days, delta.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{days}d {hours}h {minutes}m"

# Add a bot for status checking
@Bot.on_message(filters.private & filters.command("add_bot") & filters.user(OWNER))
async def add_bot(client, message):
    try:
        args = message.text.split(" ", 3)
        if len(args) < 4:
            await message.reply("Invalid arguments. Please specify <Bot Name>, <Account Name>, and <URL>.")
            return

        bot_name, account_name, bot_url = args[1], args[2], args[3]

        # Add bot to database
        db.insert_or_update(
            collection="koyeb_bots",
            query={"name": bot_name, "account": account_name},
            update={
                "$set": {
                    "url": bot_url,
                    "status": "Unknown",
                    "last_checked": current_time(),
                    "uptime_start": None,
                    "message_id": None,
                }
            },
            upsert=True,
        )
        await message.reply(f"Bot '{bot_name}' (Account: {account_name}) added successfully.")
    except Exception as e:
        await message.reply(f"Error: {e}")

# Remove a bot dynamically via PM
@Bot.on_message(filters.private & filters.command("remove_bot") & filters.user(OWNER))
async def remove_bot(client, message):
    args = message.text.split(" ", 2)
    if len(args) < 3:
        await message.reply("Invalid arguments. Please specify <Bot Name> and <Account Name>.")
        return

    bot_name, account_name = args[1], args[2]
    result = db.delete_one(collection="koyeb_bots", query={"name": bot_name, "account": account_name})
    if result.deleted_count:
        await message.reply(f"Bot '{bot_name}' (Account: {account_name}) removed successfully.")
    else:
        await message.reply(f"No bot found with name '{bot_name}' under account '{account_name}'.")

# List all added bots
@Bot.on_message(filters.private & filters.command("list_bots") & filters.user(OWNER))
async def list_bots(client, message):
    bots = db.find_all(collection="koyeb_bots")
    if not bots:
        await message.reply("No bots have been added.")
        return

    response = "**Monitored Bots:**\n\n"
    for bot in bots:
        response += f"- **Name**: {bot['name']}\n  **Account**: {bot['account']}\n  **URL**: {bot['url']}\n\n"
    response += f"**Total Bots:** {len(bots)}"
    await message.reply(response)

# Check bot status periodically
async def check_bot_status():
    async with ClientSession() as session:
        bots = db.find_all(collection="koyeb_bots")
        for bot in bots:
            try:
                async with session.get(bot["url"]) as response:
                    status = "Up" if response.status == 200 else "Down"
                    if bot["status"] != status:
                        bot["status"] = status
                        bot["last_checked"] = current_time()
                        db.insert_or_update(
                            collection="koyeb_bots",
                            query={"name": bot["name"], "account": bot["account"]},
                            update={"$set": bot},
                        )
                        # Notify channel and owner
                        message_text = f"**Bot Name**: {bot['name']}\n**Status**: {status}\n**Uptime**: {calculate_uptime(bot['uptime_start'])}"
                        if bot["message_id"]:
                            await Bot.edit_message_text(
                                chat_id=UPDATE_CHANNEL, message_id=bot["message_id"], text=message_text
                            )
                        else:
                            sent_message = await Bot.send_message(chat_id=UPDATE_CHANNEL, text=message_text)
                            bot["message_id"] = sent_message.message_id
                            db.insert_or_update(
                                collection="koyeb_bots",
                                query={"name": bot["name"], "account": bot["account"]},
                                update={"$set": {"message_id": sent_message.message_id}},
                            )
                        # Notify owner
                        await Bot.send_message(chat_id=OWNER, text=message_text)
            except Exception as e:
                print(f"Error checking bot '{bot['name']}': {e}")

# Start the periodic status check
scheduler.add_job(check_bot_status, "interval", minutes=1)
scheduler.start()
