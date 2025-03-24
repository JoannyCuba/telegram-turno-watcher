from telethon import TelegramClient, events
import re
import os

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
phone = os.environ.get("PHONE")
turno_usuario = int(os.environ.get("TURNO_USUARIO"))

client = TelegramClient("session", api_id, api_hash)

def turno_en_rango(turno, texto):
    rangos = re.findall(r'Del (\d+) al (\d+)', texto)
    for inicio, fin in rangos:
        if int(inicio) <= turno <= int(fin):
            return True
    return False

@client.on(events.NewMessage)
async def handler(event):
    mensaje = event.raw_text
    if turno_en_rango(turno_usuario, mensaje):
        print(f"✅ ¡Tu turno {turno_usuario} fue detectado!")

client.start(phone=phone)
client.run_until_disconnected()
