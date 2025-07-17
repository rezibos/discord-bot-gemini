import discord
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 🔄 Load environment
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ⚙️ Setup Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel("gemini-1.5-flash")

# 🔧 Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 📜 Define help message globally
HELP_MESSAGE = """
**🔧 PERINTAH BOT:**
1. `!tanya [pertanyaan]` - Tanya ke Gemini AI  
   Contoh: `!tanya cara membuat website`

2. `!tolong` atau `!help` - Tampilkan pesan ini

3. `!ping` - Cek status bot
"""

@client.event
async def on_ready():
    print(f"✅ Bot online sebagai {client.user}")
    await client.change_presence(activity=discord.Game(name="!help untuk bantuan"))

@client.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == client.user:
        return

    content = message.content.strip()

    # 🤖 AI Question Command
    if content.startswith("!tanya"):
        pertanyaan = content[6:].strip()
        if not pertanyaan:
            await message.reply("❓ **Cara pakai:** `!tanya [pertanyaan anda]`\n**Contoh:** `!tanya cara membuat kopi`")
            return

        try:
            # Show typing indicator
            async with message.channel.typing():
                response = gemini.generate_content(pertanyaan)
                
                # Split response if too long (Discord limit is 2000 characters)
                response_text = response.text
                if len(response_text) > 2000:
                    # Send in chunks
                    for i in range(0, len(response_text), 2000):
                        chunk = response_text[i:i+2000]
                        await message.reply(chunk)
                else:
                    await message.reply(response_text)
                    
        except Exception as e:
            await message.reply(f"❌ **Error:** Tidak bisa memproses pertanyaan.\n**Detail:** {str(e)}")

    # 📜 Help Commands
    elif content in ["!tolong", "!help"]:
        await message.reply(HELP_MESSAGE)

    # 🏓 Ping Command
    elif content == "!ping":
        await message.reply("🏓 Pong! Bot sedang online.")

    elif content == "!pc++":
        # Membuat embed untuk tampilan yang lebih menarik
        embed = discord.Embed(
            title="📚 LINK PEMBELAJARAN C++",
            description="Kumpulan sumber belajar C++ terpilih untuk pemula hingga mahir",
            color=0x00D4FF  # Warna biru
        )
        
        # Menambahkan field untuk setiap kategori
        embed.add_field(
            name="🎯 Tutorial Dasar",
            value="""
            • [TutorialsPoint C++](<https://www.tutorialspoint.com/cplusplus/index.htm>)
            • [W3Schools C++](<https://www.w3schools.com/cpp/cpp_intro.asp>)
            • [LearnCpp.com](<https://www.learncpp.com/cpp-tutorial/introduction-to-object-oriented-programming/>)
            """,
            inline=False
        )
        
        embed.add_field(
            name="🔧 Praktek & Latihan",
            value="""
            • [Codecademy C++](<https://www.codecademy.com/enrolled/courses/learn-c-plus-plus>)
            • [GeeksforGeeks C++](<https://www.geeksforgeeks.org/batch/fork-cpp-2?tab=Chapters>)
            • [Coddy Tech](<https://coddy.tech/journeys>)
            """,
            inline=False
        )
        
        embed.add_field(
            name="📖 Referensi Lanjutan",
            value="""
            • [TPointTech Tutorial](<https://www.tpointtech.com/cpp-tutorial>)
            • [C++ Reference](<https://cppreference.com/>)
            """,
            inline=False
        )
        
        # Menambahkan footer
        embed.set_footer(text="💡 Tip: Mulai dari tutorial dasar, lalu lanjut ke praktek!")
        
        # Mengirim embed
        await message.reply(embed=embed)




    # ❓ Unknown Command
    elif content.startswith("!"):
        await message.reply(f"❓ Perintah `{content}` tidak dikenali.\nKetik `!help` untuk melihat daftar perintah.")

# 🚀 Run the bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ Error: DISCORD_TOKEN tidak ditemukan di file .env")
    elif not GEMINI_API_KEY:
        print("❌ Error: GEMINI_API_KEY tidak ditemukan di file .env")
    else:
        client.run(DISCORD_TOKEN)