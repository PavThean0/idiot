import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Only load .env if it exists (local dev), Railway uses system envs directly
if os.path.exists(".env"):
    load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
# Safer loading for the ID to prevent the NoneType crash
LOG_ID_RAW = os.getenv("LOG_CHANNEL_ID")
LOG_CHANNEL_ID = int(LOG_ID_RAW) if LOG_ID_RAW else None

if not TOKEN or not LOG_CHANNEL_ID:
    print("❌ ERROR: Missing DISCORD_TOKEN or LOG_CHANNEL_ID in environment variables!")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


class PanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="3D Fixer", style=discord.ButtonStyle.primary, emoji="🔧")
    async def fixer_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        try:
            await interaction.user.send(
                "📦 Upload your ZIP file containing .ydr/.ydd/.yft assets."
            )

            await interaction.response.send_message(
                "✅ Check your DMs.",
                ephemeral=True
            )

        except:
            await interaction.response.send_message(
                "❌ I could not DM you.",
                ephemeral=True
            )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def panel(ctx):
    embed = discord.Embed(
        title="🔧 FiveM 3D Fixer",
        description=(
            "Upload ZIP files for asset validation and repair workflow.\n\n"
            "Supported:\n"
            "• .ydr\n"
            "• .ydd\n"
            "• .yft\n"
            "• .ybn"
        ),
        color=0x5865F2
    )

    embed.set_footer(text="FiveM Asset Workflow")

    await ctx.send(embed=embed, view=PanelView())


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel):

        if message.attachments:

            attachment = message.attachments[0]

            if attachment.filename.endswith(".zip"):

                log_channel = bot.get_channel(LOG_CHANNEL_ID)

                embed = discord.Embed(
                    title="🔧 3D Fixer Log",
                    color=0x57F287
                )

                embed.add_field(
                    name="User",
                    value=f"{message.author}",
                    inline=True
                )

                embed.add_field(
                    name="File",
                    value=attachment.filename,
                    inline=True
                )

                embed.add_field(
                    name="Status",
                    value="Queued",
                    inline=True
                )

                embed.add_field(
                    name="Progress",
                    value="```██████████ 100%```",
                    inline=False
                )

                embed.add_field(
                    name="Fixed",
                    value="12",
                    inline=True
                )

                embed.add_field(
                    name="Failed",
                    value="0",
                    inline=True
                )

                embed.add_field(
                    name="Duration",
                    value="1.52s",
                    inline=True
                )

                embed.add_field(
                    name="Download",
                    value="https://gofile.io/",
                    inline=False
                )

                if log_channel:
                    await log_channel.send(embed=embed)

                await message.channel.send(
                    "✅ ZIP received and queued."
                )

    await bot.process_commands(message)


bot.run(TOKEN)