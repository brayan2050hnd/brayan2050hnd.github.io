import cloudscraper
import re
import json
import asyncio
import requests
from playwright.async_api import async_playwright

# ============================================================
# CANAL ZAZ — funciona, no se toca
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
# ANIMAL PLANET — ENFOQUE FINAL
# ============================================================
PAGINA_PRINCIPAL = "https://www.tvporinternet2.com/animal-planet-en-vivo-por-internet.html"
PLAYER_IFRAME_SRC = "https://www.tvporinternet2.com/live/animalplanet.php"  # se obtiene del atributo src
USER_AGENT = "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36"

async def capturar_animal_planet():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process"
            ]
        )

        context = await browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 412, "height": 823},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
            locale="es-HN",
            timezone_id="America/Tegucigalpa",
            extra_http_headers={
                "Accept-Language": "es-HN,es;q=0.9,en;q=0.8",
                "Origin": "https://www.tvporinternet2.com"
            }
        )

        page = await context.new_page()
        
        # Lista para capturar los .m3u8
        m3u8_urls = []
        
        # Interceptamos todas las peticiones de red
        page.on("request", lambda request: (
            m3u8_urls.append(request.url) if ".m3u8" in request.url or ".mpd" in request.url else None
        ))

        stream_funcional = None

        try:
            print(f"Cargando página principal: {PAGINA_PRINCIPAL}")
            await page.goto(PAGINA_PRINCIPAL, wait_until="domcontentloaded", timeout=60000)
            print("Página cargada. Esperando iframe 'player'...")

            # Esperar al iframe
            try:
                await page.wait_for_selector('iframe[name="player"]', timeout=20000)
            except:
                print("No se encontró el iframe 'player'.")
                return None

            # Obtener el frame del iframe
            frame = None
            for _ in range(10):
                await asyncio.sleep(0.5)
                for f in page.frames:
                    if f.name == "player":
                        frame = f
                        break
                if frame:
                    break

            if not frame:
                print("No se pudo acceder al frame 'player'.")
                return None

            print("Frame 'player' obtenido. Ocultando anuncios...")
            # Ocultar elementos que podrían bloquear
            await frame.evaluate("""
                const ad = document.getElementById('don\\'tfoid');
                if (ad) ad.style.display = 'none';
                const overlays = document.querySelectorAll('div[style*="absolute"], a[target="_blank"]');
                overlays.forEach(el => { if (el.offsetHeight < 100) el.style.display = 'none'; });
            """)

            # Forzar reproducción con JavaScript
            await frame.evaluate("""
                (() => {
                    try { if (typeof jwplayer !== 'undefined') { jwplayer().play(); } } catch(e) {}
                    try { if (typeof videojs !== 'undefined') { videojs('player').play(); } } catch(e) {}
                    try { const v = document.querySelector('video'); if (v) v.play(); } catch(e) {}
                })();
            """)
            print("Reproducción forzada. Esperando stream...")

            # Dar tiempo a que el reproductor pida el stream
            await asyncio.sleep(8)

            # Ahora recorremos las URLs capturadas y validamos con requests
            for url in m3u8_urls:
                print(f"🔍 Verificando URL: {url[:120]}...")
                # Validar con un GET (o HEAD) usando el Referer del iframe
                try:
                    resp = requests.get(url, headers={
                        "Referer": PLAYER_IFRAME_SRC,
                        "User-Agent": USER_AGENT
                    }, timeout=10)
                    if resp.status_code == 200:
                        print(f"✅ Stream VÁLIDO (status 200): {url[:120]}")
                        stream_funcional = url
                        break
                    else:
                        print(f"❌ Status {resp.status_code}")
                except Exception as e:
                    print(f"❌ Error de conexión: {e}")

            # Si no se encontró, esperar un poco más y volver a probar
            if not stream_funcional:
                print("Esperando 5 segundos más y revisando nuevas peticiones...")
                await asyncio.sleep(5)
                for url in m3u8_urls:
                    if stream_funcional:
                        break
                    if url not in m3u8_urls[:len(m3u8_urls)-len(m3u8_urls)]:  # solo los nuevos
                        print(f"🔍 Verificando URL tardía: {url[:120]}...")
                        try:
                            resp = requests.get(url, headers={
                                "Referer": PLAYER_IFRAME_SRC,
                                "User-Agent": USER_AGENT
                            }, timeout=10)
                            if resp.status_code == 200:
                                print(f"✅ Stream VÁLIDO: {url[:120]}")
                                stream_funcional = url
                                break
                        except:
                            pass

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

        return stream_funcional


def actualizar_animal_planet():
    print("\n🔎 Buscando señal de ANIMAL PLANET...")
    link = asyncio.run(capturar_animal_planet())

    if link:
        print(f"¡LOGRADO! Link funcional: {link}")
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
        print("No se encontró ningún link .m3u8 válido para Animal Planet.")


# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    actualizar_zaz()
    actualizar_animal_planet()
