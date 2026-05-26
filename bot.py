from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

WEBHOOK_URL = "https://discord.com/api/webhooks/1508949153898827908/YQuEo3fOKNvsjwauxJZ1KqXvK5M85DMq7Cg_1SmDb-ayYsVdbe9yVRJnlKI1bx5aaVrd"

# Diccionario para guardar qué usuario busca qué item
busquedas = {}

@app.route('/items', methods=['POST'])
def recibir_items():
    datos = request.json
    items = datos.get('items', [])
    
    print(f"📦 Recibido {len(items)} items")
    
    for item in items:
        imagen = item.get('imagen', '')
        if imagen in busquedas:
            user_id = busquedas[imagen]
            mensaje = f"<@{user_id}> 🎯 **¡ITEM DETECTADO!**\n📦 `{imagen}`\n💰 Precio: {item['precio']}\n⏱️ Tiempo: {item['tiempo']}"
            requests.post(WEBHOOK_URL, json={"content": mensaje})
            print(f"✅ Alerta enviada a <@{user_id}> por {imagen}")
    
    return {"status": "ok"}

@app.route('/buscar', methods=['POST'])
def buscar():
    datos = request.json
    user_id = datos.get('user_id')
    item = datos.get('item')
    
    if user_id and item:
        busquedas[item] = user_id
        print(f"🔍 Usuario {user_id} ahora busca: {item}")
        return {"status": "ok"}
    return {"status": "error"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
