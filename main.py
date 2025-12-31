import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View, Button
import os
from myserver import keep_alive 

# --- 1. การตั้งค่า (CONFIG) ---
BOT_TOKEN = os.getenv('TOKEN') 

# ลิงก์รูป QR Code ของคุณ
YOUR_QR_IMAGE = "https://media.discordapp.net/attachments/1452735658354278582/1456039160245915731/IMG_7873.jpg?ex=6956e9a3&is=69559823&hm=a6f246191e87dfcafdac7980aa1d79501dda1b25b6b99ae9380e69b8194719c4&=&format=webp&width=940&height=1294"

LOG_CHANNEL_ID = 1456037561591005380 
REVIEW_LINK = "https://discord.com/channels/1452701844366168126/1452716968925855966"

# --- 2. ข้อมูลสินค้า (เพิ่มแพคเกจ) ---
products = {
    # --- สินค้าเดี่ยว ---
    "sms": {
        "title": "📱 ยิงเบอร์ (SMS Spammer)",
        "desc": "ระบบยิง SMS ใส่เบอร์เป้าหมาย \n• ใช้งานง่าย เร็ว แรง \n• ระยะเวลา: **ถาวร**",
        "price": "100 บาท", 
        "status": "🟢 Online (ปกติ)",
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
        "status": "🟢 Online (ปกติ)",
        "image_url": "https://images.nvidia.com/geforce-com/international/images/what-is-fps-and-how-it-heps-you-win-games/High-FPS-Ghosting.gif"
    },
    "wipe": {
        "title": "🗑️ โปรแกรมลบประวัติ",
        "desc": "ล้างข้อมูลขยะและร่องรอยการใช้งาน \n• สะอาดหมดจด ไม่โดนตรวจ \n• ระยะเวลา: **ถาวร**",
        "price": "100 บาท",
        "status": "🟢 Online (ปกติ)",
        "image_url": "https://media.tenor.com/hQ0tnsbxOw0AAAAM/microsoft-windows-windows.gif"
    },
    # --- แพคเกจสุดคุ้ม ---
    "pack1": {
        "title": "🎁 แพคสุดคุ้ม 1 (Steam + Boost FPS)",
        "desc": "ได้ทั้งเกมสตีมและตัวบูส FPS \n• คุ้มกว่าซื้อแยก! \n• ระยะเวลา: **ถาวร**",
        "price": "450 บาท",
        "status": "🔥 ขายดี (Hot)",
        "image_url": "https://media1.tenor.com/m/0J9ze1ghwzMAAAAd/pc-gamers-too-many-games.gif"
    },
    "pack2": {
        "title": "🎁 แพคสุดคุ้ม 2 (Steam + SMS)",
        "desc": "ได้ทั้งเกมสตีมและระบบยิงเบอร์ \n• ครบเครื่องเรื่องป่วนและเล่น \n• ระยะเวลา: **ถาวร**",
        "price": "450 บาท",
        "status": "🔥 ขายดี (Hot)",
        "image_url": "https://media1.tenor.com/m/0J9ze1ghwzMAAAAd/pc-gamers-too-many-games.gif"
    },
    "pack3": {
        "title": "🎁 แพคสุดคุ้ม 3 (Steam + Wipe)",
        "desc": "ได้ทั้งเกมสตีมและตัวลบประวัติ \n• เล่นสนุกไร้ร่องรอย \n• ระยะเวลา: **ถาวร**",
        "price": "450 บาท",
        "status": "🔥 ขายดี (Hot)",
        "image_url": "https://media1.tenor.com/m/0J9ze1ghwzMAAAAd/pc-gamers-too-many-games.gif"
    },
    "pack4": {
        "title": "🎁 แพคสุดคุ้ม 4 (Boost + Wipe)",
        "desc": "บูสคอมแรงพร้อมลบประวัติ \n• สายคลีน สายแรงห้ามพลาด \n• ระยะเวลา: **ถาวร**",
        "price": "150 บาท",
        "status": "🔥 สุดคุ้ม (Value)",
        "image_url": "https://images.nvidia.com/geforce-com/international/images/what-is-fps-and-how-it-heps-you-win-games/High-FPS-Ghosting.gif"
    },
    "pack5": {
        "title": "🎁 แพคสุดคุ้ม 5 (Boost + Wipe + SMS)",
        "desc": "มัดรวม 3 อย่าง (บูส+ลบประวัติ+ยิงเบอร์) \n• คุ้มที่สุดในร้าน! \n• ระยะเวลา: **ถาวร**",
        "price": "200 บาท",
        "status": "👑 คุ้มที่สุด (Best)",
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
            # สินค้าเดี่ยว
            discord.SelectOption(label="ยิงเบอร์ SMS", description="100 บาท", emoji="📱", value="sms"),
            discord.SelectOption(label="เกมสตีมออนไลน์", description="400 บาท", emoji="🎮", value="steam"),
            discord.SelectOption(label="โปรแกรมบูส FPS", description="100 บาท", emoji="🚀", value="boost"),
            discord.SelectOption(label="โปรแกรมลบประวัติ", description="100 บาท", emoji="🗑️", value="wipe"),
            # แพคเกจ
            discord.SelectOption(label="แพค 1: Steam + Boost", description="450 บาท", emoji="🎁", value="pack1"),
            discord.SelectOption(label="แพค 2: Steam + SMS", description="450 บาท", emoji="🎁", value="pack2"),
            discord.SelectOption(label="แพค 3: Steam + Wipe", description="450 บาท", emoji="🎁", value="pack3"),
            discord.SelectOption(label="แพค 4: Boost + Wipe", description="150 บาท", emoji="🎁", value="pack4"),
            discord.SelectOption(label="แพค 5: Boost + Wipe + SMS", description="200 บาท", emoji="👑", value="pack5"),
        ]
        super().__init__(placeholder="🔻 คลิกเพื่อเลือกดูสินค้า...", options=options)

    async def callback(self, interaction: discord.Interaction):
        data = products[self.values[0]]
        
        # เตรียม Embed รายละเอียด
        embed = discord.Embed(title=data['title'], description=data['desc'], color=0x00ff00)
        embed.add_field(name="💰 ราคา", value=f"```fix\n{data['price']}\n```", inline=True)
        embed.add_field(name="📡 สถานะ", value=f"`{data['status']}`", inline=True)
        embed.set_image(url=data['image_url'])
        
        view = View()
        
        # ปุ่ม 1: QR Code
        qr_btn = discord.ui.Button(label="💸 QR โอนเงิน", style=discord.ButtonStyle.primary, emoji="📲")
        
        async def qr_callback(interaction: discord.Interaction):
            # สร้าง Embed QR Code
            embed_qr = discord.Embed(
                title="📲 สแกน QR เพื่อชำระเงิน", 
                description=f"สินค้า: **{data['title']}**\nยอดที่ต้องโอน: **{data['price']}**\n\n📌 *กรุณากรอกยอดเงินให้ตรงกับราคาสินค้านะครับ*", 
                color=0x0099ff
            )
            # ใช้ตัวแปร YOUR_QR_IMAGE ที่ตั้งไว้ด้านบน
            embed_qr.set_image(url=YOUR_QR_IMAGE)
            
            await interaction.response.send_message(embed=embed_qr, ephemeral=True)

        qr_btn.callback = qr_callback
        
        # ปุ่ม 2: Ticket
        ticket_btn = discord.ui.Button(label="💳 แจ้งโอน / เปิด Ticket", style=discord.ButtonStyle.success, emoji="🎟️", url="https://discord.com/channels/1452701844366168126/1452717523601461258")

        view.add_item(qr_btn)
        view.add_item(ticket_btn)
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        # Admin Logger
        try:
            log_channel = client.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                log_embed = discord.Embed(title="🕵️‍♂️ ลูกค้าสนใจสินค้า", color=0xffa500)
                log_embed.add_field(name="ลูกค้า", value=f"{interaction.user.name}", inline=True)
                log_embed.add_field(name="สินค้า", value=data['title'], inline=True)
                await log_channel.send(embed=log_embed)
        except:
            pass

@client.tree.command(name="ezproductnow", description="ส่งป้ายประกาศร้านค้า")
async def ezproductnow(interaction: discord.Interaction):
    embed = discord.Embed(title="✨ EzProduct 24hr/7d", description="บริการจำหน่ายโปรแกรมและเครื่องมือคุณภาพสูง\nเลือกรายการสินค้าได้จากเมนูด้านล่าง 👇", color=0x2b2d31)
    
    # รูป Banner หน้าร้าน
    embed.set_image(url="https://media.discordapp.net/attachments/1452735658354278582/1456035716386652192/Gemini_Generated_Image_dk9shdk9shdk9shd_1.png?ex=6956e66e&is=695594ee&hm=ac36d115e2b5ff00d4ea0380151e1ee58a6eedd7a9cc5d2cea94d1a47417d0a3&=&format=webp&quality=lossless&width=982&height=1296")
    
    # อัปเดตรายการสินค้าหน้าแรกให้โชว์แพคเกจด้วย
    embed.add_field(name="📦 รายการสินค้า", value="> 📱 SMS Spammer\n> 🎮 Steam Unlocker\n> 🚀 FPS Booster\n> 🗑️ History Wiper", inline=True)
    embed.add_field(name="🎁 แพคเกจสุดคุ้ม", value="> แพค 1-3: Steam+ของแถม `450.-`\n> แพค 4: Boost+Wipe `150.-`\n> แพค 5: รวม 3 อย่าง `200.-`", inline=True)
    
    embed.set_footer(text="มั่นใจด้วยเครดิตลูกค้าจริง | ปลอดภัย 100%")

    main_view = View()
    main_view.add_item(ProductSelect())
    main_view.add_item(discord.ui.Button(label="⭐️ เช็คเครดิต / รีวิว", style=discord.ButtonStyle.link, url=REVIEW_LINK))

    await interaction.response.send_message(embed=embed, view=main_view)

keep_alive()
client.run(BOT_TOKEN)
