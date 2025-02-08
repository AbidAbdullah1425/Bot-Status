from pyrogram import Client, filters
import os
from bot import Bot

FILE_PATH = "channel_id.txt"

@Bot.on_message(filters.command("save"))
async def save_channel(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/save <channel_id>`")

    channel_id = message.command[1]

    # Save to file
    with open(FILE_PATH, "w") as file:
        file.write(channel_id)

    await message.reply(f"Channel ID saved: `{channel_id}`")

@Bot.on_message(filters.command("get"))
async def get_channel(client, message):
    if not os.path.exists(FILE_PATH):
        return await message.reply("No channel ID found.")

    # Read from file
    with open(FILE_PATH, "r") as file:
        channel_id = file.read().strip()

    await message.reply(f"Saved Channel ID: `{channel_id}`")
