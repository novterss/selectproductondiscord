# 🤖 selectproductondiscord

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/Discord.py-2.0+-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord.py" />
</p>

---

## 🛒 Features
* **Automated Product Menu:** Smooth Slash Command (`/ezproductnow`) to display the store's offerings.
* **Interactive UI:** Utilizes Discord's modern `Select Menus` and `Buttons` for a premium user experience.
* **Instant QR Payment:** Ephemeral QR code generation for secure and private payments.
* **Admin Logging:** Real-time logging system to track customer interests in a dedicated channel.
* **Ticket Integration:** Seamless link to support tickets for payment verification.

## 🛠️ Configuration & Setup

1. **Install the library**

   ```bash
   pip install discord.py
   ```

2. **Set environment variables** (never put the token in the code)

   | Variable | Description |
   |---|---|
   | `DISCORD_BOT_TOKEN` | Your Discord bot token |
   | `QR_IMAGE_URL` | Direct link to your payment QR code image |
   | `LOG_CHANNEL_ID` | Channel ID for admin notifications |
   | `REVIEW_LINK` | Link to your reviews / vouch channel |

   ```bash
   # macOS / Linux
   export DISCORD_BOT_TOKEN="your-token"
   # Windows PowerShell
   $env:DISCORD_BOT_TOKEN = "your-token"
   ```

3. **Edit products** in the `products` dictionary inside `selectproduct.py`.

4. **Run the bot**

   ```bash
   python selectproduct.py
   ```

## 🚀 How to use

Once the bot is running, use the following Slash Command in your Discord server:
`/[your-bot-name]` - To summon the interactive store menu.

---

## 📸 Showcase

<p align="center">
  <img src="https://github.com/user-attachments/assets/15697dda-bf27-4ce0-bde5-07418849894d" width="30%" alt="Menu" />
  <img src="https://github.com/user-attachments/assets/bf8eb445-0c8f-457a-8fbb-ce85a4315972" width="30%" alt="Product" />
  <img src="https://github.com/user-attachments/assets/35695fff-ae7f-4d92-9861-24ca2bb4fa16" width="30%" alt="QR" />
</p>

## 🔒 Security Note
This bot uses **Ephemeral Messages** for payment information, ensuring that only the customer can see the QR code and payment details, keeping your transaction process private and clean.

---

<p align="center">
  Developed by <a href="https://github.com/novterss">novterss</a> | <b>EzplaystoreTh Official</b>
</p>
