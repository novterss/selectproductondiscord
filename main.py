import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View
import os
from myserver import keep_alive 

# ดึง Token จาก Environment Variable (ปลอดภัยกว่า)
BOT_TOKEN = os.getenv('TOKEN') 

products = {
    "sms": {
        "title": "📱 ยิงเบอร์ (SMS Spammer)",
        "desc": "ระบบยิง SMS ใส่เบอร์เป้าหมาย \n• ใช้งานง่าย เร็ว แรง \n• ระยะเวลา: **ถาวร**",
        "price": "100 บาท",
        "image_url": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ZneXF6M3ZneXF6M3ZneXF6M3ZneXF6M3ZneXF6M3ZneXF6JmN0PWc/KyGF9Cq8tqWv3y70Hk/giphy.gif"
    },
    "steam": {
        "title": "🎮 เกมสตีมออนไลน์ (Steam Unlocker)",
        "desc": "เล่นเกมออนไลน์ได้ทุกเกม (ทะลุเกมดัง) \n• เล่นกับเพื่อนได้ปกติ \n• ระยะเวลา: **ถาวร**",
        "price": "400 บาท",
        "image_url": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ZneXF6M3ZneXF6M3ZneXF6M3ZneXF6M3ZneXF6M3ZneXF6JmN0PWc/fDH4k0jMh70lK/giphy.gif"
    },
    "boost": {
        "title": "🚀 โปรแกรมบูส FPS",
        "desc": "เพิ่มความลื่นไหล ลดอาการแลค \n• ปรับจูนระบบ Windows \n• ระยะเวลา: **ถาวร**",
        "price": "100 บาท",
        "image_url": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ZneXF6M3ZneXF6M3ZneXF6M3ZneXF6M3ZneXF6M3ZneXF6JmN0PWc/3o7TKsAdsDjlhY6Cwo/giphy.gif"
    },
    "wipe": {
        "title": "🗑️ โปรแกรมลบประวัติ",
        "desc": "ล้างข้อมูลขยะและร่องรอยการใช้งาน \n• สะอาดหมดจด ไม่โดนตรวจ \n• ระยะเวลา: **ถาวร**",
        "price": "100 บาท",
        "image_url": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ZneXF6M3ZneXF6M3ZneXF6M3ZneXF6M3ZneXF6M3ZneXF6JmN0PWc/xT9DPldJGTZNrGWYhO/giphy.gif"
    }
}

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
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
        ]
        super().__init__(placeholder="🔻 คลิกเพื่อเลือกดูสินค้า...", options=options)

    async def callback(self, interaction: discord.Interaction):
        data = products[self.values[0]]
        embed = discord.Embed(title=data['title'], description=data['desc'], color=0x00ff00)
        embed.add_field(name="💰 ราคา", value=f"```fix\n{data['price']}\n```", inline=False)
        embed.set_image(url=data['image_url'])
        view = View()
        view.add_item(discord.ui.Button(label="💳 สั่งซื้อ (Ticket)", style=discord.ButtonStyle.success, url="ใส่ลิ้งค์ห้องTicketของคุณที่นี่"))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@client.tree.command(name="ezproductnow", description="ส่งป้ายประกาศร้านค้า")
async def ezproductnow(interaction: discord.Interaction):
    embed = discord.Embed(title="✨ REZ SERVICES STORE", description="เลือกสินค้าได้เลยครับ", color=0x2b2d31)
    embed.add_field(name="📦 รายการ", value="> 📱 SMS: 100.-\n> 🎮 Steam: 400.-\n> 🚀 FPS: 100.-\n> 🗑️ Wipe: 100.-", inline=False)
    await interaction.response.send_message(embed=embed, view=View().add_item(ProductSelect()))

keep_alive()
client.run(BOT_TOKEN)