import discord
from discord import app_commands
from discord.ui import Select, View, Button
import os


BOT_TOKEN = "โทเค่นบอท"  


YOUR_QR_IMAGE = "รูปคิวอาโค๊ต"

LOG_CHANNEL_ID = ไอดีห้องดิสคอร์ด 
REVIEW_LINK = "ลิงค์ห้อง"


products = {
    "1": {"title": "1", "desc": "รายละเอียด \n• ระยะเวลา: ถาวร", "price": "100 บาท", "status": "🟢 Online", "image_url": "รูปเพิ่มเติม"},
    "2": {"title": "2", "desc": "รายละเอียด \n• ระยะเวลา: ถาวร", "price": "200 บาท", "status": "🟢 Online", "image_url": "รูปเพิ่มเติม"},
    "3": {"title": "3", "desc": "รายละเอียด \n• ระยะเวลา: ถาวร", "price": "300 บาท", "status": "🟢 Online", "image_url": "รูปเพิ่มเติม"},
    "4": {"title": "4", "desc": "รายละเอียด \n• ระยะเวลา: ถาวร", "price": "400 บาท", "status": "🟢 Online", "image_url": "รูปเพิ่มเติม"},
    "5": {"title": "5", "desc": "รายละเอียด \n• ระยะเวลา: ถาวร", "price": "500 บาท", "status": "🔥 Hot", "image_url": "รูปเพิ่มเติม"},
    "6": {"title": "6", "desc": "รายละเอียด \n• ระยะเวลา: ถาวร", "price": "600 บาท", "status": "🔥 Hot", "image_url": "รูปเพิ่มเติม"},
    "7": {"title": "7", "desc": "รายละเอียด \n• ระยะเวลา: ถาวร", "price": "700 บาท", "status": "🔥 Hot", "image_url": "รูปเพิ่มเติม"},
    "8": {"title": "8", "desc": "รายละเอียด \n• ระยะเวลา: ถาวร", "price": "800 บาท", "status": "🔥 Value", "image_url": "รูปเพิ่มเติม"},
    "9": {"title": "9", "desc": "รายละเอียด \n• ระยะเวลา: ถาวร", "price": "900 บาท", "status": "👑 Best", "image_url": "รูปเพิ่มเติม"}
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
            discord.SelectOption(label="1", description="100 บาท", emoji="📱", value="1"),
            discord.SelectOption(label="2", description="200 บาท", emoji="🎮", value="2"),
            discord.SelectOption(label="3", description="300 บาท", emoji="🚀", value="3"),
            discord.SelectOption(label="4", description="400 บาท", emoji="🗑️", value="4"),
            discord.SelectOption(label="5 ", description="500 บาท", emoji="🎁", value="5"),
            discord.SelectOption(label="6: ", description="600 บาท", emoji="🎁", value="6"),
            discord.SelectOption(label="7: ", description="700 บาท", emoji="🎁", value="7"),
            discord.SelectOption(label="8: ", description="800 บาท", emoji="🎁", value="8"),
            discord.SelectOption(label="9: ", description="900 บาท", emoji="👑", value="9"),
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

        ticket_btn = discord.ui.Button(label="💳 แจ้งโอน / เปิด Ticket", style=discord.ButtonStyle.success, emoji="🎟️", url="ลิงค์ห้องticket")
        view.add_item(qr_btn)
        view.add_item(ticket_btn)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        try:
            if client.get_channel(LOG_CHANNEL_ID):
                await client.get_channel(LOG_CHANNEL_ID).send(embed=discord.Embed(title="ลูกค้าสนใจสินค้า", description=f"User: {interaction.user.name}\nItem: {data['title']}", color=0xffa500))
        except: pass

@client.tree.command(name="ชื่อบอท", description="ส่งป้ายประกาศร้านค้า")
async def ezproductnow(interaction: discord.Interaction):
    embed = discord.Embed(title="✨ EzProduct 24hr/7d", description="เลือกรายการสินค้าได้จากเมนูด้านล่าง 👇", color=0x2b2d31)
    embed.set_image(url="รูปแบนเนอร์")
    embed.add_field(name="📦 รายการสินค้า", value="> 1\n> 2\n> 3r\n> 4", inline=True)
    embed.add_field(name="🎁 แพคเกจสุดคุ้ม", value="> แพค 1-3: Steam+... `450.-`\n> แพค 4: Boost+Wipe `150.-`\n> แพค 5: รวม 3 อย่าง `200.-`", inline=True)
    
    view = View()
    view.add_item(ProductSelect())
    view.add_item(discord.ui.Button(label="⭐️ เช็คเครดิต", style=discord.ButtonStyle.link, url=ห้องเครดิต))
    await interaction.response.send_message(embed=embed, view=view)

client.run(BOT_TOKEN)
