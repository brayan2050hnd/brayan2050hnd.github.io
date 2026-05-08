import cloudscraper
import re
import json

# ============================================================
# LA SOLUCIÓN DEFINITIVA PARA YOUTUBE (CERO BLOQUEOS)
# ============================================================
def actualizar_canal_youtube(
    canal_nombre,
    html_file,
    json_file,
    pais,
    imagen_url,
    channel_id,
    filter_live=False, 
    random_select=False
):
    print(f"\n📡 Configurando señal permanente para {canal_nombre}...")

    # MAGIA: Usamos el parámetro nativo de YouTube 'live_stream?channel=' 
    # Esto le dice a YouTube que auto-redireccione siempre al directo actual del canal.
    embed_url = f"https://www.youtube.com/embed/live_stream?channel={channel_id}&autoplay=1&rel=0&modestbranding=1&playsinline=1"

    # 1. CREAR EL ARCHIVO HTML CON EL ENLACE MÁGICO
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{canal_nombre}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ width: 100%; height: 100%; overflow: hidden; background: #000; }}
        iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }}
    </style>
</head>
<body>
    <iframe src="{embed_url}" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</body>
</html>"""

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"   --> Archivo HTML {html_file} inyectado con éxito.")

    # 2. ACTUALIZAR ARCHIVO JSON
    url_html_github = f"https://brayan2050hnd.github.io/{html_file}"
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    canal_existe = False
    for canal in data:
        if canal.get("nombre", "").strip().upper() == canal_nombre.strip().upper():
            canal["url"] = url_html_github
            canal_existe = True
            break

    if not canal_existe:
        data.append({
            "nombre": canal_nombre,
            "imagen": imagen_url,
            "url": url_html_github,
            "pais": pais
        })
        
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"✅ ¡{canal_nombre} asegurado y listo para transmitir!")


# ============================================================
# CANAL ZAZ — INTACTO
# ============================================================
def actualizar_zaz():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    fuente_web = "https://www.cxtvenvivo.com/tv-en-vivo/zaz-tv"
    print(f"\nBuscando señal de ZAZ en: {fuente_web}")

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
            if any(x in l_limpio.lower() for x in ['ads', 'click', 'pop', 'wcpkck']): continue
            link_valido = l_limpio
            break

        if link_valido:
            print(f"¡LOGRADO! Link de ZAZ encontrado: {link_valido}")
            with open('mexico.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            for canal in data:
                if canal.get('nombre') == "ZAZ":
                    canal['url'] = link_valido
            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print("No se encontró ningún link .m3u8 válido para ZAZ.")
    except Exception as e:
        print(f"Error en la captura: {e}")

# ============================================================
# CANAL TELEMUNDO MIAMI — INTACTO
# ============================================================
def actualizar_telemundo_miami():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    fuente_web = "https://www.cxtvenvivo.com/tv-en-vivo/telemundo-51-miami"
    print(f"\nBuscando señal de Telemundo Miami en: {fuente_web}")

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
            if any(x in l_limpio.lower() for x in ['ads', 'click', 'pop', 'wcpkck']): continue
            link_valido = l_limpio
            break

        if link_valido:
            print(f"¡LOGRADO! Link de Telemundo Miami encontrado: {link_valido}")
            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            for canal in data:
                if "TELEMUNDO MIAMI" in canal.get('nombre', '').upper():
                    canal['url'] = link_valido
                    break
            else:
                data.append({"nombre": "TELEMUNDO MIAMI", "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Telemundo_logo_2018.svg/640px-Telemundo_logo_2018.svg.png", "url": link_valido, "pais": "USA"})
            with open('usa.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print("No se encontró ningún link para Telemundo Miami.")
    except Exception as e:
        print(f"Error en la captura: {e}")

# ============================================================
# CANAL TELEMUNDO CALIFORNIA — INTACTO
# ============================================================
def actualizar_telemundo_california():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    fuente_web = "https://www.cxtvenvivo.com/tv-en-vivo/telemundo-california"
    print(f"\nBuscando señal de Telemundo California en: {fuente_web}")

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
            if any(x in l_limpio.lower() for x in ['ads', 'click', 'pop', 'wcpkck']): continue
            link_valido = l_limpio
            break

        if link_valido:
            print(f"¡LOGRADO! Link de Telemundo California encontrado: {link_valido}")
            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            for canal in data:
                if "TELEMUNDO CALIFORNIA" in canal.get('nombre', '').upper():
                    canal['url'] = link_valido
                    break
            else:
                data.append({"nombre": "TELEMUNDO CALIFORNIA", "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Telemundo_logo_2018.svg/640px-Telemundo_logo_2018.svg.png", "url": link_valido, "pais": "USA"})
            with open('usa.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print("No se encontró ningún link para Telemundo California.")
    except Exception as e:
        print(f"Error en la captura: {e}")

# ============================================================
# EJECUCIÓN DEL SCRIPT
# ============================================================
if __name__ == "__main__":
    print("Iniciando cacería de enlaces...")
    
    actualizar_zaz()
    actualizar_telemundo_miami()
    actualizar_telemundo_california()

    actualizar_canal_youtube(
        canal_nombre="CHOLUVISION",
        html_file="choluvision.html",
        json_file="honduras.json",
        pais="HONDURAS",
        imagen_url="https://upload.wikimedia.org/wikipedia/commons/d/d6/Golden_TV_Logo.png",
        channel_id="UCdEAEJ8Sdyn0kIQ3wbcX5ow"
    )

    actualizar_canal_youtube(
        canal_nombre="TELEMUNDO FLORIDA",
        html_file="telemundo_florida.html",
        json_file="usa.json",
        pais="USA",
        imagen_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Telemundo_logo_2018.svg/640px-Telemundo_logo_2018.svg.png",
        channel_id="UCsDG_lFhRcvC14XRYVLeIfA"
    )

    actualizar_canal_youtube(
        canal_nombre="USA",
        html_file="usa.html",
        json_file="usa.json",
        pais="USA",
        imagen_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/USA_Network_logo.svg/640px-USA_Network_logo.svg.png",
        channel_id="UCAAxhCE6iHfINacI4FCx_8A"
    )

    actualizar_canal_youtube(
        canal_nombre="DISNEY CHANNEL",
        html_file="disney.html",
        json_file="usa.json",
        pais="USA",
        imagen_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Disney_Channel_logo.svg/640px-Disney_Channel_logo.svg.png",
        channel_id="UCayRpbmAiiuU50OpDPVSjwA"
    )

    actualizar_canal_youtube(
        canal_nombre="UNIVERSAL KIDS",
        html_file="universal_kids.html",
        json_file="usa.json",
        pais="USA",
        imagen_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Universal_Kids_logo.svg/640px-Universal_Kids_logo.svg.png",
        channel_id="UCY26xU0-avwTJ6F6TzUZVEw"
    )
    
    print("\n✅ ¡Actualización completada a prueba de fallos!")

