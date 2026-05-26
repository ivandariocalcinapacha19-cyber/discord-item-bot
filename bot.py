from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

WEBHOOK_URL = "https://discord.com/api/webhooks/1508949153898827908/YQuEo3fOKNvsjwauxJZ1KqXvK5M85DMq7Cg_1SmDb-ayYsVdbe9yVRJnlKI1bx5aaVrd"

@app.route('/items', methods=['POST'])
def recibir_items():
    datos = request.json
    items = datos.get('items', [])
    
    print(f"📦 Recibido {len(items)} items")
    
    for item in items:
        if "item-potion51" in item.get('imagen', ''):
            mensaje = f"🎯 **¡ITEM DETECTADO!**\n📦 `{item['imagen']}`\n💰 Precio: {item['precio']}\n⏱️ Tiempo: {item['tiempo']}"
            requests.post(WEBHOOK_URL, json={"content": mensaje})
            print(f"✅ Alerta enviada: {item['imagen']}")
    
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

