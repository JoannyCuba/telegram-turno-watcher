from telethon import TelegramClient, events
import re

# === CONFIGURACIÓN ===
api_id = 27405613  # Reemplazá con tu API ID real
api_hash = '6fdf293c9673229709d5dcb67b872284'  # Reemplazá con tu API HASH real
phone = '+5352526284'  # Tu número de Telegram con el código de país

# Turnos por grupo
turnos_por_grupo = {
    -1001945898634: 3463,  # Grupo 1 → Turno 3463
    -1001906412008: 4323,  # Grupo 2 → Turno 4323
    -1002057387506: 1607   # Grupo 3 → Turno 1607
}

# Tu usuario para recibir alerta (puede ser ID o username sin @)
usuario_destino = 'Joanny_Benejam'  # o 1444436304

# === INICIO DE CLIENTE TELEGRAM ===
client = TelegramClient("session", api_id, api_hash)

# === FUNCIÓN PARA DETECTAR TURNOS EN RANGOS ===
def turno_en_rango(turno, texto):
    rangos = re.findall(r'Del (\d+) al (\d+)', texto)
    for inicio, fin in rangos:
        if int(inicio) <= turno <= int(fin):
            return True
    return False

# === ESCUCHADOR DE MENSAJES ===
@client.on(events.NewMessage(chats=list(turnos_por_grupo.keys())))
async def handler(event):
    mensaje = event.raw_text
    chat_id = event.chat_id
    nombre_grupo = event.chat.title or "Grupo desconocido"
    turno_usuario = turnos_por_grupo.get(chat_id)

    if turno_usuario and turno_en_rango(turno_usuario, mensaje):
        alerta = f"🚨 ¡Tu turno {turno_usuario} fue anunciado en el grupo '{nombre_grupo}'!"
        print(f"✅ {alerta}")
        await client.send_message(usuario_destino, alerta)
    else:
        print(f"📩 [{nombre_grupo}] Mensaje sin coincidencias: {mensaje[:50]}...")

# === CONECTAR Y EJECUTAR ===
client.start(phone=phone)
client.run_until_disconnected()
