import discord
import requests

DISCORD_TOKEN = "MTU3MDgxOTMwMzA2NDg2MjgxMQ.G6wmgF._Z9XdDxSq3elYI35MV3dxFEUYBub5OdShtkqfc"
TELEGRAM_BOT_TOKEN = "8847863527:AAEkpYS_px58XEmW59S4Sou1utNi9G4p7u4"
TELEGRAM_CHAT_ID = "-1003903013247"  # Например: "-1001234567890"
TARGET_CHANNEL_ID = 1561452282015645756

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Бот {client.user} запущен! Слушаю ветку {TARGET_CHANNEL_ID}")

@client.event
async def on_message(message):
    # Игнорируем сообщения самого пересыльщика
    if message.author.id == client.user.id:
        return

    # Проверяем, что сообщение пришло из нужной ветки
    if message.channel.id == TARGET_CHANNEL_ID:
        log_parts = []
        
        # Если есть обычный текст
        if message.content:
            log_parts.append(message.content)
            
        # Если лог пришел в виде карточки (Embed) от вебхука/бота игры
        for embed in message.embeds:
            if embed.title:
                log_parts.append(f"*{embed.title}*")
            if embed.description:
                log_parts.append(embed.description)
            for field in embed.fields:
                log_parts.append(f"*{field.name}:* {field.value}")

        if not log_parts:
            return

        final_text = "📝 **Новый лог:**\n\n" + "\n".join(log_parts)
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": final_text,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)

client.run(DISCORD_TOKEN)