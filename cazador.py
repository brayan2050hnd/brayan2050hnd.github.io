import cloudscraper
import re
import json
import subprocess

# ============================================================
# CANAL ZAZ — sin cambios, funciona perfecto
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
# CANAL CHOLUVISION — extracción desde YouTube (cliente Android)
# ============================================================
def actualizar_choluvision():
    youtube_url = "https://www.youtube.com/live/TEqTZ34X-_Q"
    print(f"\nExtrayendo stream de CHOLUVISION desde: {youtube_url}")
    
    try:
        # Comando con user-agent móvil y cliente Android para evitar bloqueo
        comando = [
            "yt-dlp",
            "-g",
            "--extractor-args", "youtube:player_client=android",
            "--user-agent", "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            youtube_url
        ]
        resultado = subprocess.run(
            comando,
            capture_output=True, text=True, check=True, timeout=30
        )
        link = resultado.stdout.strip()
        if not link:
            print("❌ yt-dlp no devolvió ninguna URL.")
            return
        
        print(f"✅ Enlace M3U8 obtenido: {link}")

        # Guardar en honduras.json
        try:
            with open('honduras.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("⚠️ honduras.json no existe. Creándolo...")
            data = []

        for canal in data:
            if "CHOLUVISION" in canal.get('nombre', '').upper():
                canal['url'] = link
                print("URL de CHOLUVISION actualizada en honduras.json.")
                break
        else:
            # Si no encuentra el canal, lo agrega al final
            print("⚠️ No se encontró 'CHOLUVISION' en honduras.json. Agregando entrada nueva.")
            data.append({
                "nombre": "CHOLUVISION",
                "url": link
            })

        with open('honduras.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando yt-dlp: {e.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")


# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    actualizar_zaz()
    actualizar_choluvision()
