import discord
from discord.ext import commands
import os
from openai import OpenAI

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f" Logged in as {bot.user}")

def ask_ai(prompt):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        return response.output_text
    except Exception as e:
        return f"Error: {e}"

@bot.command()
async def explain(ctx, *, topic):
    prompt = f"Explain this topic in simple terms for studying: {topic}"
    reply = ask_ai(prompt)
    await ctx.send(reply)


@bot.command()
async def question(ctx, *, topic):
    prompt = f"Create 5 study questions about: {topic}"
    reply = ask_ai(prompt)
    await ctx.send(reply)


@bot.command()
async def answers(ctx, *, topic):
    prompt = f"Provide answers to common questions about: {topic}"
    reply = ask_ai(prompt)
    await ctx.send(reply)


@bot.command()
async def studymode(ctx, *, topic):
    await ctx.send(f"Study mode started for: **{topic}**")

    questions = ask_ai(f"Create 3 quiz questions about {topic}")
    await ctx.send("**Questions:**\n" + questions)

    answers = ask_ai(f"Provide answers for these questions:\n{questions}")
    await ctx.send("**Answers:**\n" + answers)


bot.run(DISCORD_TOKEN)
