import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View, Button
import os
from myserver import keep_alive 

# --- 1. การตั้งค่า (CONFIG) ---
BOT_TOKEN = os.getenv('TOKEN') 
LOG_CHANNEL_ID = 1456037561591005380  # <--- แก้ตรงนี้: ใส่เลข ID ห้องที่อยากให้บอทแจ้งเตือนแอดมิน (เป็นตัวเลข ไม่ต้องมีเครื่องหมายคำพูด)
REVIEW_LINK = "https://discord.com/channels/1452701844366168126/1452716968925855966" # <--- แก้ตรงนี้: ใส่ลิงก์ห้องรีวิวของคุณ

# --- 2. ข้อมูลสินค้า (เพิ่ม Status) ---
products = {
    "sms": {
        "title": "📱 ยิงเบอร์ (SMS Spammer)",
        "desc": "ระบบยิง SMS ใส่เบอร์เป้าหมาย \n• ใช้งานง่าย เร็ว แรง \n• ระยะเวลา: **ถาวร**",
        "price": "100 บาท",
        "status": "🟢 Online (ปกติ)", # สถานะสินค้า
        "image_url": "https://media1.tenor.com/m/mQfF_M43QzsAAAAC/rhythmdoctor-gaming.gif"
    },
    "steam": {
        "title": "🎮 เกมสตีมออนไลน์ (Steam Unlocker)",
        "desc": "เล่นเกมออนไลน์ได้ทุกเกม (ทะลุเกมดัง) \n• เล่นกับเพื่อนได้ปกติ \n• ระยะเวลา: **ถาวร**",
        "price": "400 บาท",
        "status": "🟢 Online (ปกติ)",
        "image_url": "https://media1.tenor.com/m/0J9ze1ghwzMAAAAd/pc-gamers-too-many-games.gif"
    },
    "boost": {
        "title": "🚀 โปรแกรมบูส FPS",
        "desc": "เพิ่มความลื่นไหล ลดอาการแลค \n• ปรับจูนระบบ Windows \n• ระยะเวลา: **ถาวร**",
        "price": "100 บาท",
        "status": "🟢 Online (ปกติ)", # ลองเปลี่ยนสถานะดูได้
        "image_url": "https://images.nvidia.com/geforce-com/international/images/what-is-fps-and-how-it-heps-you-win-games/High-FPS-Ghosting.gif"
    },
    "wipe": {
        "title": "🗑️ โปรแกรมลบประวัติ",
        "desc": "ล้างข้อมูลขยะและร่องรอยการใช้งาน \n• สะอาดหมดจด ไม่โดนตรวจ \n• ระยะเวลา: **ถาวร**",
        "price": "100 บาท",
        "status": "🟢 Online (ปกติ)",
        "image_url": "https://media.tenor.com/hQ0tnsbxOw0AAAAM/microsoft-windows-windows.gif"
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
            discord.SelectOption(label="ยิงเบอร์ SMS", description="100 บาท | 🟢 Online", emoji="📱", value="sms"),
            discord.SelectOption(label="เกมสตีมออนไลน์", description="400 บาท | 🟢 Online", emoji="🎮", value="steam"),
            discord.SelectOption(label="โปรแกรมบูส FPS", description="100 บาท | 🟢 Online", emoji="🚀", value="boost"),
            discord.SelectOption(label="โปรแกรมลบประวัติ", description="100 บาท | 🟢 Online", emoji="🗑️", value="wipe"),
        ]
        super().__init__(placeholder="🔻 คลิกเพื่อเลือกดูสินค้า...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # 1. ดึงข้อมูลสินค้า
        data = products[self.values[0]]
        
        # 2. สร้าง Embed รายละเอียดสินค้า
        embed = discord.Embed(title=data['title'], description=data['desc'], color=0x00ff00)
        embed.add_field(name="💰 ราคา", value=f"```fix\n{data['price']}\n```", inline=True)
        embed.add_field(name="📡 สถานะ", value=f"`{data['status']}`", inline=True) # โชว์สถานะตรงนี้
        embed.set_image(url=data['image_url'])
        
        view = View()
        view.add_item(discord.ui.Button(label="💳 สั่งซื้อ (Ticket)", style=discord.ButtonStyle.success, url="https://discord.com/channels/1452701844366168126/1452717523601461258"))
        
        # 3. ส่งข้อมูลให้ลูกค้าเห็นคนเดียว (Ephemeral)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        # --- ส่วนของ Admin Logger (แจ้งเตือนแอดมิน) ---
        try:
            log_channel = client.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                # สร้าง Embed สั้นๆ แจ้งเตือน
                log_embed = discord.Embed(title="🕵️‍♂️ มีลูกค้าสนใจสินค้า!", color=0xffa500)
                log_embed.add_field(name="ลูกค้า", value=f"{interaction.user.name} ({interaction.user.mention})", inline=True)
                log_embed.add_field(name="ดูสินค้า", value=data['title'], inline=True)
                log_embed.set_footer(text=f"Time: {interaction.created_at.strftime('%H:%M:%S')}")
                await log_channel.send(embed=log_embed)
        except Exception as e:
            print(f"Logger Error: {e}")

@client.tree.command(name="ezproductnow", description="ส่งป้ายประกาศร้านค้า")
async def ezproductnow(interaction: discord.Interaction):
    embed = discord.Embed(title="✨ EzProduct 24hr/7d", description="บริการจำหน่ายโปรแกรมและเครื่องมือคุณภาพสูง\nเลือกรายการสินค้าได้จากเมนูด้านล่าง 👇", color=0x2b2d31)
    
    # รูป Banner ใหญ่หน้าร้าน
    embed.set_image(url="https://media.discordapp.net/attachments/1452735658354278582/1456035716386652192/Gemini_Generated_Image_dk9shdk9shdk9shd_1.png?ex=6956e66e&is=695594ee&hm=ac36d115e2b5ff00d4ea0380151e1ee58a6eedd7a9cc5d2cea94d1a47417d0a3&=&format=webp&quality=lossless&width=982&height=1296")
    
    embed.add_field(name="📦 รายการสินค้า", value="> 📱 SMS Spammer\n> 🎮 Steam Unlocker\n> 🚀 FPS Booster\n> 🗑️ History Wiper", inline=False)
    embed.set_footer(text="มั่นใจด้วยเครดิตลูกค้าจริง | ปลอดภัย 100%")

    # สร้าง View หลักที่มี Dropdown + ปุ่มรีวิว
    main_view = View()
    main_view.add_item(ProductSelect()) # ใส่ Dropdown
    main_view.add_item(discord.ui.Button(label="⭐️ เช็คเครดิต / รีวิว", style=discord.ButtonStyle.link, url=REVIEW_LINK)) # ใส่ปุ่มรีวิว

    await interaction.response.send_message(embed=embed, view=main_view)

keep_alive()
client.run(BOT_TOKEN)
