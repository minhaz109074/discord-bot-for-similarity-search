import ollama
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image
import io
from PIL import Image
from helper import find_similar_images, detect_faces_and_get_embedding, process_directory

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name}")

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello! I am here to help you. Ask me any question.")

@bot.command(name="ask")
async def ask(ctx, *, message):
    response = ollama.chat(model='llama2', messages=[
              {
                  'role': 'system',
                  'content': 'You will act as a assistant. You will provide answers to the users questions concisely with no more than 1000 words.'                 
              },
              {
                'role': 'user',
                'content': message,
              },
            ])
    await ctx.send(response['message']['content'])

@bot.command(name="summarise")
async def summarise(ctx, *, message):

    response = ollama.chat(model='llama2', messages=[
              {
                  'role': 'system',
                  'content': 'You will act as a assistant. You will summarise the provided messages concisely with no more than 1000 words.'                 
              },
              {
                'role': 'user',
                'content': message,
              },
            ])
    await ctx.send(response['message']['content'])

@bot.command(name="search")
async def find_similar(ctx):
    if not ctx.message.attachments:
        await ctx.send("Please upload an image.")
        return

    attachment = ctx.message.attachments[0]
    image_bytes = await attachment.read()

    image = Image.open(io.BytesIO(image_bytes))

    embedding = detect_faces_and_get_embedding(image)

    if embedding is None:
        await ctx.send("No faces detected or failed to calculate embedding.")
        return

    similar_images = find_similar_images(embedding)

    if not similar_images:
        await ctx.send("No similar images found.")
        return

    for image_path in similar_images:
        await ctx.send(file=discord.File(image_path))

if __name__ == "__main__":

    directory_path = 'images/'
    cascade_path = "E:/astha it/Python-discord-bot/models/haarcascade_frontalface_default.xml"
    input_image_path = 'images/minhazul_abedin_1.jpeg'

    process_directory(directory_path, cascade_path)
    #find_similar_images(input_image_path)
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
