import cloudscraper
import re
import json
import asyncio
from playwright.async_api import async_playwright

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
# ANIMAL PLANET — ESTRATEGIA CORREGIDA
# ============================================================
STEALTH_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'languages', { get: () => ['es-HN', 'es', 'en-US', 'en'] });
Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
window.chrome = { runtime: {} };
"""

URL_PRINCIPAL = "https://www.tvporinternet2.com/animal-planet-en-vivo-por-internet.html"
URL_PLAYER    = "https://www.tvporinternet2.com/live/animalplanet.php"

async def capturar_animal_planet():
    link_encontrado = None
    m3u8_candidatos = []

    # Palabras clave prohibidas en la URL del stream
    PALABRAS_PROHIBIDAS = [
        'sharethis', 'doubleclick', 'googleads', 'googlevideo',
        'facebook', 'twitter', 'pinterest', 'whatsapp', 'telegram',
        'ads', 'adservice', 'adnxs', 'criteo', 'outbrain', 'taboola'
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="es-HN",
            timezone_id="America/Tegucigalpa",
        )
        await context.add_init_script(STEALTH_SCRIPT)

        # --- Página principal: obtener cookies y el iframe del reproductor ---
        pagina_principal = await context.new_page()
        try:
            print("Cargando página principal...")
            await pagina_principal.goto(URL_PRINCIPAL, wait_until="networkidle", timeout=60000)
            print("Página principal cargada.")

            # Extraer el src del iframe del reproductor (normalmente con "live" en la URL)
            iframe_src = await pagina_principal.evaluate("""
                () => {
                    const iframes = document.querySelectorAll('iframe');
                    for (const iframe of iframes) {
                        const src = iframe.src || '';
                        if (src.includes('live') || src.includes('player') || src.includes('animalplanet')) {
                            return src;
                        }
                    }
                    return null;
                }
            """)
            if iframe_src:
                print(f"Iframe del reproductor encontrado: {iframe_src}")
            else:
                print("No se encontró iframe del reproductor, usando URL por defecto.")
                iframe_src = URL_PLAYER
        except Exception as e:
            print(f"Error en página principal: {e}")
            iframe_src = URL_PLAYER
        finally:
            await pagina_principal.close()

        # --- Ahora dentro del reproductor ---
        pagina_player = await context.new_page()

        # Interceptar peticiones de red en este contexto
        def interceptar(request):
            url = request.url
            # Solo nos interesan streams
            if ".m3u8" in url or ".mpd" in url:
                # Rechazar si contiene palabras prohibidas
                url_lower = url.lower()
                if any(p in url_lower for p in PALABRAS_PROHIBIDAS):
                    return
                print(f"  -> Stream candidato: {url[:100]}...")
                m3u8_candidatos.append(url)
        pagina_player.on("request", interceptar)

        try:
            print(f"Cargando reproductor: {iframe_src}")
            await pagina_player.goto(iframe_src, wait_until="networkidle", timeout=60000)
            print("Reproductor cargado.")

            # Intentar hacer clic en el botón de play para forzar la carga
            selectores_play = [
                '.jw-icon-playback', '.jw-icon-display', '.vjs-big-play-button',
                'button[aria-label="Play"]', '.play-button', '.fp-play'
            ]
            for sel in selectores_play:
                try:
                    el = await pagina_player.wait_for_selector(sel, timeout=5000)
                    if el:
                        await el.click()
                        print(f"Click en {sel}")
                        break
                except:
                    continue

            # Esperar hasta 30 segundos a que aparezca un m3u8
            intentos = 0
            while not m3u8_candidatos and intentos < 6:
                print(f"Esperando stream... ({intentos+1}/6)")
                await asyncio.sleep(5)
                intentos += 1

            if m3u8_candidatos:
                link_encontrado = m3u8_candidatos[0]
                print(f"Stream capturado: {link_encontrado[:100]}...")
            else:
                # Último intento: extraer con JS desde el reproductor
                js_result = await pagina_player.evaluate("""
                    () => {
                        try {
                            if (typeof jwplayer !== 'undefined') {
                                return jwplayer().getPlaylist()[0].file;
                            }
                        } catch(e) {}
                        try {
                            const v = document.querySelector('video');
                            if (v && v.src) return v.src;
                        } catch(e) {}
                        return null;
                    }
                """)
                if js_result and ("m3u8" in js_result or "mpd" in js_result):
                    link_encontrado = js_result
                    print(f"Stream obtenido por JS: {link_encontrado[:100]}...")

        except Exception as e:
            print(f"Error en el reproductor: {e}")
        finally:
            await pagina_player.close()
            await browser.close()

    return link_encontrado


def actualizar_animal_planet():
    print("\nBuscando señal de ANIMAL PLANET...")
    link = asyncio.run(capturar_animal_planet())

    if link:
        print(f"¡LOGRADO! Link encontrado: {link}")
        try:
            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for canal in data:
                if "ANIMAL PLANET" in canal.get('nombre', '').upper():
                    canal['url'] = link
                    print("URL de Animal Planet actualizada en usa.json.")

            with open('usa.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar: {e}")
    else:
        print("No se encontró ningún link .m3u8 para Animal Planet.")


# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    actualizar_zaz()
    actualizar_animal_planet()
