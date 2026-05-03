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
# ANIMAL PLANET — PRUEBA TODAS LAS OPCIONES DE REPRODUCTOR
# ============================================================
REFERER = "https://www.tvporinternet2.com/animal-planet-en-vivo-por-internet.html"

# Lista de URLs de reproductores alternativos (Opción 1, 2, 3, etc.)
URLS_REPRODUCTOR = [
    "https://www.tvporinternet2.com/live/animalplanet.php",
    "https://www.tvporinternet2.com/live2/animalplanet.php",
    "https://www.tvporinternet2.com/live3/animalplanet.php",
    "https://www.tvporinternet2.com/live4/animalplanet.php",
    "https://www.tvporinternet2.com/live5/animalplanet.php",
    "https://www.tvporinternet2.com/live6/animalplanet.php",
]

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

        # Contexto móvil realista
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36",
            viewport={"width": 412, "height": 823},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
            locale="es-HN",
            timezone_id="America/Tegucigalpa",
            extra_http_headers={
                "Accept-Language": "es-HN,es;q=0.9,en;q=0.8",
                "Referer": REFERER,
                "Origin": "https://www.tvporinternet2.com"
            }
        )

        for idx, url_player in enumerate(URLS_REPRODUCTOR, 1):
            print(f"\n🔍 Probando Opción {idx}: {url_player}")
            m3u8_encontrado = None
            page = await context.new_page()

            # Interceptar peticiones
            async def interceptar(request):
                url = request.url
                if ".m3u8" in url or ".mpd" in url:
                    print(f"   📡 Stream candidato: {url[:120]}")
                    nonlocal m3u8_encontrado
                    if not m3u8_encontrado:
                        m3u8_encontrado = url
            page.on("request", interceptar)

            try:
                # Cargar el reproductor (evento "load", sin esperar networkidle)
                await page.goto(url_player, wait_until="load", timeout=60000)
                print("   Página cargada (load).")

                # Simular toque en el centro del reproductor
                await page.mouse.move(200, 400)
                await page.wait_for_timeout(500)
                await page.mouse.click(200, 400)

                # Intentar hacer clic en botones de play
                selectores = [
                    '.jw-icon-playback', '.jw-icon-display', '.vjs-big-play-button',
                    'button[aria-label="Play"]', '.play-button', '.fp-play',
                    'video', '.jwplayer'
                ]
                for sel in selectores:
                    try:
                        el = await page.query_selector(sel)
                        if el:
                            await el.click()
                            print(f"   Click en {sel}")
                            break
                    except:
                        continue

                # Esperar hasta 45 segundos a que aparezca el stream
                for intento in range(9):
                    if m3u8_encontrado:
                        break
                    print(f"   Esperando stream... ({intento+1}/9)")
                    await asyncio.sleep(5)

            except Exception as e:
                print(f"   Error: {e}")
            finally:
                await page.close()

            if m3u8_encontrado:
                print(f"\n✅ ¡STREAM ENCONTRADO! {m3u8_encontrado[:100]}...")
                await browser.close()
                return m3u8_encontrado

        await browser.close()
    return None


def actualizar_animal_planet():
    print("\n🔎 Buscando señal de ANIMAL PLANET en todas las opciones...")
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
        print("No se encontró ningún link .m3u8 válido para Animal Planet.")


# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    actualizar_zaz()
    actualizar_animal_planet()
