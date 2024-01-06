from telethon import events
from userbot import client

info = {'category': 'tools', 'pattern': 'wallet', 'description': 'Посмотреть баланс в CryptoBot'}

EMOJI_MAP = {
    "USDT": "<emoji document_id=6032709766881479783>💵</emoji>",
    "TON": "<emoji document_id=6032804204622384196>💵</emoji>",
    "BTC": "<emoji document_id=6032744483102133873>💵</emoji>",
    "ETH": "<emoji document_id=6032967271645711263>💵</emoji>",
    "BNB": "<emoji document_id=6032733926072520137>💵</emoji>",
    "BUSD": "<emoji document_id=6033097439219551284>💵</emoji>",
    "USDC": "<emoji document_id=6030553792083135328>💵</emoji>",
}

client.parse_mode = 'html'

@client.on(events.NewMessage(pattern=r'[.!/].*wallet'))
async def wallet_command(event):
    async with event.client.conversation("https://t.me/CryptoBot") as conv:
        m = await conv.send_message("/wallet")
        r = await conv.get_response()

        await event.client.delete_messages(event.chat_id, m)

        button = None
        for row in r.reply_markup.rows:
            for btn in row.buttons:
                if btn.text == "Show Small Balances":
                    button = btn
                    break
            if button:
                break

        if button:
            await event.click(button=button)

            r = await event.client.get_messages(event.chat_id, ids=r.id)

            await r[0].click(0)

        balance_info = "\n\n".join(
            f"{next((emoji for trigger, emoji in EMOJI_MAP.items() if trigger in line), '<emoji document_id=5471952986970267163>💎</emoji>')} <b>{line.split(maxsplit=1)[1]}</b>"
            for line in r.text.splitlines()
            if line.startswith("·") and ": 0 " not in line
        )

        if balance_info:
            response = f"{balance_info}"
        else:
            response = "Empty balance"
        
    await client.edit_message(event.message, f"👛 Твой <a href='https://t.me/CryptoBot'>CryptoBot</a> кошелёк:\n\n{response}", link_preview=False, parse_mode='HTML')
