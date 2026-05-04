import cloudscraper
import re
import json
import subprocess
import requests
import os

# ============================================================
# CANAL ZAZ — NO SE TOCA, FUNCIONA PERFECTO
# ============================================================
def actualizar_zaz():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    fuente_web = "https://www.cxtvenvivo.com/tv-en-vivo/zaz-tv"
    print(f"Buscando señal de ZAZ en: {fuente_web}")

    try:
        response = scraper.get(fuente_web, timeout=15).text
        
        links = re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', response)
        
        if not links:
            iframes = re.findall(r'src=["\'](https?://[^\s<>"\']+?)["\']', response)
            for frame_url in iframes:
                if 'google' in frame_url or 'facebook' in frame_url: continue
                try:
                    f_res = scraper.get(frame_url, headers={'Referer': fuente_web}, timeout=10).text
                    links.extend(re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', f_res))
                except:
                    continue

        link_valido = None
        for l in links:
            l_limpio = l.replace('\\/', '/').split('"')[0].split("'")[0]
            if any(x in l_limpio.lower() for x in ['ads', 'click', 'pop', 'wcpkck']):
                continue
            link_valido = l_limpio
            break

        if link_valido:
            print(f"¡LOGRADO! Link de ZAZ encontrado: {link_valido}")

            with open('mexico.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for canal in data:
                if canal.get('nombre') == "ZAZ":
                    canal['url'] = link_valido
                    print("URL de ZAZ actualizada en el JSON.")

            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print("No se encontró ningún link .m3u8 válido para ZAZ.")

    except Exception as e:
        print(f"Error en la captura: {e}")


# ============================================================
# CANAL CHOLUVISION — OBTIENE EL ID DEL CANAL Y BUSCA EN VIVO
# ============================================================
def actualizar_choluvision():
    API_KEY = os.environ.get('YOUTUBE_API_KEY')
    VIDEO_ID = "TEqTZ34X-_Q"  # ID del video de ejemplo para obtener el canal

    if not API_KEY:
        print("❌ Error: No se encontró la clave de API de YouTube en los secretos.")
        return

    print("\nObteniendo ID del canal de CHOLUVISION...")
    
    # Paso 1: Obtener el ID del canal a partir del ID del video
    video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={VIDEO_ID}&key={API_KEY}"
    
    try:
        video_resp = requests.get(video_url).json()
        items = video_resp.get("items", [])
        if not items:
            print("❌ No se pudo obtener información del video.")
            return
        channel_id = items[0]["snippet"]["channelId"]
        print(f"ℹ️ ID del canal obtenido: {channel_id}")
    except Exception as e:
        print(f"❌ Error al obtener ID del canal: {e}")
        return

    # Paso 2: Buscar transmisiones en vivo del canal
    print("Verificando si CHOLUVISION está en vivo...")
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"

    try:
        respuesta = requests.get(search_url).json()
        items = respuesta.get("items", [])

        if items:
            video_id = items[0]["id"]["videoId"]
            nuevo_link = f"https://www.youtube.com/embed/{video_id}?rel=0&showinfo=0&modestbranding=1&playsinline=1"
            print(f"✅ Enlace de CHOLUVISION actualizado: {nuevo_link}")

            # Guardar en honduras.json
            try:
                with open('honduras.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []

            encontrado = False
            for canal in data:
                if "CHOLUVISION" in canal.get('nombre', '').upper():
                    canal['url'] = nuevo_link
                    encontrado = True
                    print("URL de CHOLUVISION actualizada en honduras.json.")
                    break

            if not encontrado:
                print("⚠️ No se encontró 'CHOLUVISION' en honduras.json. Agregando entrada nueva.")
                data.append({
                    "nombre": "CHOLUVISION",
                    "imagen": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Golden_TV_Logo.png",
                    "url": nuevo_link,
                    "pais": "HONDURAS"
                })

            with open('honduras.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print("ℹ️ CHOLUVISION no está transmitiendo en este momento. No se actualiza el enlace.")

    except Exception as e:
        print(f"❌ Error al verificar el directo: {e}")


# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    actualizar_zaz()
    actualizar_choluvision()
