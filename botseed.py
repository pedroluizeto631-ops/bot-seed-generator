import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random

# =====================
# CARREGAR TOKEN
# =====================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN não encontrado no .env")

# =====================
# INTENTS
# =====================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

# =====================
# SEEDS
# =====================
JAVA_SEEDS = [
    {"seed": "2318176229889913168", "desc": "Vila costeira próxima ao spawn, ótima para progressão rápida."},
    {"seed": "16912565435231", "desc": "Vale cercado por montanhas e Cherry Grove, ideal para construção."},
    {"seed": "3838492495747609467", "desc": "Planícies amplas com rios longos."},
    {"seed": "902384902384", "desc": "Caverna gigante logo no spawn."},
    {"seed": "555666777", "desc": "Ilha isolada para survival hardcore."},
    {"seed": "192837465", "desc": "Deserto com vila e templo próximos."},
    {"seed": "777888999", "desc": "Montanhas altas com neve e muitos minérios."},
    {"seed": "1010101010", "desc": "Floresta densa para bases escondidas."},
    {"seed": "246824682", "desc": "Spawn com vários biomas próximos."},
    {"seed": "314159265", "desc": "Seed equilibrada para qualquer estilo."}
]

BEDROCK_SEEDS = [
    {"seed": "4504535438041489910", "desc": "Terreno plano com rios, ideal para cidades grandes."},
    {"seed": "1817024869", "desc": "Planície infinita com cavernas abertas."},
    {"seed": "2318176229889913168", "desc": "Vila costeira e stronghold próximos."},
    {"seed": "999888777", "desc": "Spawn ótimo para speedrun Bedrock."},
    {"seed": "123123123", "desc": "Ilha grande cercada por oceano."},
    {"seed": "888777666", "desc": "Montanhas e vales naturais."},
    {"seed": "456456456", "desc": "Muitas vilas próximas."},
    {"seed": "321321321", "desc": "Terreno perfeito para redstone."},
    {"seed": "2020202020", "desc": "Biomas raros próximos ao spawn."},
    {"seed": "909090909", "desc": "Seed equilibrada para multiplayer."}
]

# =====================
# FUNÇÃO EMBED
# =====================
def criar_embed(plataforma, seed, desc, user):
    embed = discord.Embed(
        title=f"🌍 Minecraft {plataforma}",
        description=f"**Seed:** `{seed}`\n📝 {desc}",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Gerado para {user.name}")
    embed.set_thumbnail(url=user.display_avatar.url)
    return embed

# =====================
# VIEWS
# =====================
class PlataformaView(discord.ui.View):
    def __init__(self, autor):
        super().__init__(timeout=60)
        self.autor = autor

    async def interaction_check(self, interaction):
        return interaction.user == self.autor

    @discord.ui.button(label="Java", style=discord.ButtonStyle.green)
    async def java(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content="☕ **Minecraft Java**",
            view=SeedView(self.autor, "Java")
        )

    @discord.ui.button(label="Bedrock", style=discord.ButtonStyle.blurple)
    async def bedrock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content="🪨 **Minecraft Bedrock**",
            view=SeedView(self.autor, "Bedrock")
        )

class SeedView(discord.ui.View):
    def __init__(self, autor, plataforma):
        super().__init__(timeout=120)
        self.autor = autor
        self.plataforma = plataforma
        self.seed_atual = None

    async def interaction_check(self, interaction):
        return interaction.user == self.autor

    @discord.ui.button(label="🎲 Gerar seed", style=discord.ButtonStyle.gray)
    async def gerar(self, interaction: discord.Interaction, button: discord.ui.Button):
        lista = JAVA_SEEDS if self.plataforma == "Java" else BEDROCK_SEEDS
        self.seed_atual = random.choice(lista)

        embed = criar_embed(
            self.plataforma,
            self.seed_atual["seed"],
            self.seed_atual["desc"],
            interaction.user
        )

        await interaction.response.send_message(
            content=interaction.user.mention,
            embed=embed,
            view=self
        )



# =====================
# COMANDO
# =====================
@bot.command()
async def seed(ctx):
    await ctx.send(
        "🌍 **Escolha a plataforma:**",
        view=PlataformaView(ctx.author)
    )

# =====================
# EVENTO READY
# =====================
@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

# =====================
# START
# =====================
bot.run(TOKEN)
