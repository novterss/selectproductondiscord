import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View, Button
import os
from myserver import keep_alive 

# --- CONFIG ---
BOT_TOKEN = os.getenv('TOKEN') 

# ลิงก์รูป QR Code (ใส่ลิงก์ของคุณที่นี่)
YOUR_QR_IMAGE = "https://media.discordapp.net/attachments/1452735658354278582/1456039160245915731/IMG_7873.jpg?ex=6956e9a3&is=69559823&hm=a6f246191e87dfcafdac7980aa1d79501dda1b25b6b99ae9380e69b8194719c4&=&format=webp&width=940&height=1294"

LOG_CHANNEL_ID = 1456037561591005380 
REVIEW_LINK = "https://discord.com/channels/1452701844366168126/1452716968925855966"

# --- DATA ---
products = {
    "sms": {"title": "📱 ยิงเบอร์ SMS", "desc": "ยิงเบอร์เป้าหมาย \n• ระยะเวลา: ถาวร", "price": "100 บาท", "status": "🟢 Online", "image_url": "https://media1.tenor.com/m/mQfF_M43QzsAAAAC/rhythmdoctor-gaming.gif"},
    "steam": {"title": "🎮 Steam Unlocker", "desc": "เล่นเกมสตีมออนไลน์ \n• ระยะเวลา: ถาวร", "price": "400 บาท", "status": "🟢 Online", "image_url": "https://media1.tenor.com/m/0J9ze1ghwzMAAAAd/pc-gamers-too-many-games.gif"},
    "boost": {"title": "🚀 Boost FPS", "desc": "บูสคอมลื่น ลดแลค \n• ระยะเวลา: ถาวร", "price": "100 บาท", "status": "🟢 Online", "image_url": "https://images.nvidia.com/geforce-com/international/images/what-is-fps-and-how-it-heps-you-win-games/High-FPS-Ghosting.gif"},
    "wipe": {"title": "🗑️ History Wiper", "desc": "ลบประวัติสะอาด \n• ระยะเวลา: ถาวร", "price": "100 บาท", "status": "🟢 Online", "image_url": "https://media.tenor.com/hQ0tnsbxOw0AAAAM/microsoft-windows-windows.gif"},
    "pack1": {"title": "🎁 แพค 1 (Steam+Boost)", "desc": "คุ้มกว่าซื้อแยก \n• ระยะเวลา: ถาวร", "price": "450 บาท", "status": "🔥 Hot", "image_url": "https://media1.tenor.com/m/0J9ze1ghwzMAAAAd/pc-gamers-too-many-games.gif"},
    "pack2": {"title": "🎁 แพค 2 (Steam+SMS)", "desc": "สายป่วนสายเล่น \n• ระยะเวลา: ถาวร", "price": "450 บาท", "status": "🔥 Hot", "image_url": "https://media1.tenor.com/m/0J9ze1ghwzMAAAAd/pc-gamers-too-many-games.gif"},
    "pack3": {"title": "🎁 แพค 3 (Steam+Wipe)", "desc": "เล่นสนุกไร้ร่องรอย \n• ระยะเวลา: ถาวร", "price": "450 บาท", "status": "🔥 Hot", "image_url": "https://media1.tenor.com/m/0J9ze1ghwzMAAAAd/pc-gamers-too-many-games.gif"},
    "pack4": {"title": "🎁 แพค 4 (Boost+Wipe)", "desc": "สายคลีนคอมแรง \n• ระยะเวลา: ถาวร", "price": "150 บาท", "status": "🔥 Value", "image_url": "https://images.nvidia.com/geforce-com/international/images/what-is-fps-and-how-it-heps-you-win-games/High-FPS-Ghosting.gif"},
    "pack5": {"title": "🎁 แพค 5 (รวม 3 อย่าง)", "desc": "Boost+Wipe+SMS \n• ระยะเวลา: ถาวร", "price": "200 บาท", "status": "👑 Best", "image_url": "https://media.tenor.com/hQ0tnsbxOw0AAAAM/microsoft-windows-windows.gif"}
}

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f'Ready: {self.user}')

client = MyClient()

class ProductSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="ยิงเบอร์ SMS", description="100 บาท", emoji="📱", value="sms"),
            discord.SelectOption(label="เกมสตีมออนไลน์", description="400 บาท", emoji="🎮", value="steam"),
            discord.SelectOption(label="โปรแกรมบูส FPS", description="100 บาท", emoji="🚀", value="boost"),
            discord.SelectOption(label="โปรแกรมลบประวัติ", description="100 บาท", emoji="🗑️", value="wipe"),
            discord.SelectOption(label="แพค 1: Steam + Boost", description="450 บาท", emoji="🎁", value="pack1"),
            discord.SelectOption(label="แพค 2: Steam + SMS", description="450 บาท", emoji="🎁", value="pack2"),
            discord.SelectOption(label="แพค 3: Steam + Wipe", description="450 บาท", emoji="🎁", value="pack3"),
            discord.SelectOption(label="แพค 4: Boost + Wipe", description="150 บาท", emoji="🎁", value="pack4"),
            discord.SelectOption(label="แพค 5: Boost + Wipe + SMS", description="200 บาท", emoji="👑", value="pack5"),
        ]
        super().__init__(placeholder="🔻 เลือกสินค้า...", options=options)

    async def callback(self, interaction: discord.Interaction):
        data = products[self.values[0]]
        embed = discord.Embed(title=data['title'], description=data['desc'], color=0x00ff00)
        embed.add_field(name="💰 ราคา", value=f"```fix\n{data['price']}\n```", inline=True)
        embed.add_field(name="📡 สถานะ", value=f"`{data['status']}`", inline=True)
        embed.set_image(url=data['image_url'])
        
        view = View()
        qr_btn = discord.ui.Button(label="💸 QR โอนเงิน", style=discord.ButtonStyle.primary, emoji="📲")
        async def qr_callback(interaction: discord.Interaction):
            embed_qr = discord.Embed(title="📲 สแกนเพื่อชำระเงิน", description=f"ยอด: **{data['price']}**", color=0x0099ff)
            embed_qr.set_image(url=YOUR_QR_IMAGE)
            await interaction.response.send_message(embed=embed_qr, ephemeral=True)
        qr_btn.callback = qr_callback

        ticket_btn = discord.ui.Button(label="💳 แจ้งโอน / เปิด Ticket", style=discord.ButtonStyle.success, emoji="🎟️", url="https://discord.com/channels/1452701844366168126/1452717523601461258")
        view.add_item(qr_btn)
        view.add_item(ticket_btn)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        try:
            if client.get_channel(LOG_CHANNEL_ID):
                await client.get_channel(LOG_CHANNEL_ID).send(embed=discord.Embed(title="ลูกค้าสนใจสินค้า", description=f"User: {interaction.user.name}\nItem: {data['title']}", color=0xffa500))
        except: pass

@client.tree.command(name="ezproductnow", description="ส่งป้ายประกาศร้านค้า")
async def ezproductnow(interaction: discord.Interaction):
    embed = discord.Embed(title="✨ EzProduct 24hr/7d", description="เลือกรายการสินค้าได้จากเมนูด้านล่าง 👇", color=0x2b2d31)
    embed.set_image(url="https://media.discordapp.net/attachments/1452735658354278582/1456035716386652192/Gemini_Generated_Image_dk9shdk9shdk9shd_1.png?ex=6956e66e&is=695594ee&hm=ac36d115e2b5ff00d4ea0380151e1ee58a6eedd7a9cc5d2cea94d1a47417d0a3&=&format=webp&quality=lossless&width=982&height=1296")
    embed.add_field(name="📦 รายการสินค้า", value="> 📱 SMS Spammer\n> 🎮 Steam Unlocker\n> 🚀 FPS Booster\n> 🗑️ History Wiper", inline=True)
    embed.add_field(name="🎁 แพคเกจสุดคุ้ม", value="> แพค 1-3: Steam+... `450.-`\n> แพค 4: Boost+Wipe `150.-`\n> แพค 5: รวม 3 อย่าง `200.-`", inline=True)
    
    view = View()
    view.add_item(ProductSelect())
    view.add_item(discord.ui.Button(label="⭐️ เช็คเครดิต", style=discord.ButtonStyle.link, url=REVIEW_LINK))
    await interaction.response.send_message(embed=embed, view=view)

keep_alive()
client.run(BOT_TOKEN)
