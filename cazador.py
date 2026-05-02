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
# ANIMAL PLANET — apunta directo al iframe del player
# ============================================================
STEALTH_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'languages', { get: () => ['es-HN', 'es', 'en-US', 'en'] });
Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
window.chrome = { runtime: {} };
"""

URL_PRINCIPAL   = "https://www.tvporinternet2.com/animal-planet-en-vivo-por-internet.html"
URL_PLAYER      = "https://www.tvporinternet2.com/live/animalplanet.php"

async def capturar_animal_planet():
    link_encontrado = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ]
        )

        for intento in range(3):
            if link_encontrado:
                break
            if intento > 0:
                print(f"  Reintento {intento}/2...")
                await asyncio.sleep(5)

            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 720},
                locale="es-HN",
                timezone_id="America/Tegucigalpa",
                extra_http_headers={
                    "Accept-Language": "es-HN,es;q=0.9,en;q=0.8",
                    # Referer = página principal para que el player crea que viene de ahí
                    "Referer": URL_PRINCIPAL
                }
            )
            await context.add_init_script(STEALTH_SCRIPT)

            # Capturar CUALQUIER .m3u8 (sin filtrar por keyword)
            def interceptar(request):
                nonlocal link_encontrado
                url = request.url
                if ".m3u8" in url and not link_encontrado:
                    # Ignorar anuncios
                    if any(x in url.lower() for x in ['ads', 'doubleclick', 'googlevideo']):
                        return
                    print(f"  ✅ M3U8 capturado: {url[:80]}...")
                    link_encontrado = url

            context.on("request", interceptar)
            page = await context.new_page()

            try:
                print(f"  Intento {intento + 1}: cargando player directo...")

                # Paso 1: visitar la página principal primero (para que el servidor
                # vea el historial de navegación correcto)
                await page.goto(URL_PRINCIPAL, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(3)

                # Paso 2: navegar directo al iframe del player con el referer ya establecido
                await page.goto(URL_PLAYER, wait_until="networkidle", timeout=60000)
                await asyncio.sleep(5)

                # Paso 3: simular humano
                await page.mouse.move(640, 360)
                await asyncio.sleep(2)

                # Paso 4: intentar click en play con varios selectores
                selectores_play = [
                    '.jw-icon-display',
                    '.jw-display-icon-display',
                    '.jw-display',
                    'button[aria-label="Play"]',
                    '.vjs-big-play-button',
                    '.play-button',
                    'video',
                    '.fp-play',
                    '#player',
                ]
                for sel in selectores_play:
                    try:
                        el = await page.query_selector(sel)
                        if el:
                            await el.click()
                            print(f"  Click en: {sel}")
                            await asyncio.sleep(10)
                            break
                    except:
                        pass

                # Paso 5: esperar más si todavía no capturó
                if not link_encontrado:
                    print("  Esperando que el player genere el stream...")
                    await asyncio.sleep(15)

            except Exception as e:
                print(f"  ❌ Error: {e}")
            finally:
                await context.close()

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
