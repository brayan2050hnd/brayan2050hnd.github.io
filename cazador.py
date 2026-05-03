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
# ANIMAL PLANET — VERSIÓN FINAL CON VALIDACIÓN
# ============================================================
PAGINA_PRINCIPAL = "https://www.tvporinternet2.com/animal-planet-en-vivo-por-internet.html"
REFERER = PAGINA_PRINCIPAL
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
        m3u8_candidatos = []
        stream_valido = None

        # Interceptar peticiones de red
        async def interceptar(request):
            if ".m3u8" in request.url or ".mpd" in request.url:
                print(f"📡 Stream candidato: {request.url[:120]}")
                m3u8_candidatos.append(request.url)

        page.on("request", interceptar)

        try:
            print(f"Cargando página principal: {PAGINA_PRINCIPAL}")
            await page.goto(PAGINA_PRINCIPAL, wait_until="domcontentloaded", timeout=60000)
            print("Página principal cargada (DOM). Esperando iframe 'player'...")

            # Esperar a que aparezca el iframe del reproductor
            try:
                await page.wait_for_selector('iframe[name="player"]', timeout=15000)
                print("Iframe 'player' presente.")
            except:
                print("No se encontró el iframe 'player'. Continuando sin él...")

            await asyncio.sleep(5)

            # Obtener el frame "player"
            frame = None
            for f in page.frames:
                if f.name == "player":
                    frame = f
                    break

            if frame:
                print("Frame 'player' obtenido. Preparando reproducción...")

                # Ocultar anuncio bloqueante
                try:
                    await frame.evaluate("""
                        const ad = document.getElementById('don\\'tfoid');
                        if (ad) ad.style.display = 'none';
                    """)
                    print("Anuncio ocultado.")
                except Exception as e:
                    print(f"No se pudo ocultar anuncio: {e}")

                # Iniciar reproducción con JavaScript
                await frame.evaluate("""
                    (() => {
                        try { if (typeof jwplayer !== 'undefined') { jwplayer().play(); } } catch(e) {}
                        try { if (typeof videojs !== 'undefined') { videojs('player').play(); } } catch(e) {}
                        try { const v = document.querySelector('video'); if (v) v.play(); } catch(e) {}
                    })();
                """)
                print("Reproducción forzada vía JS.")

            # Esperar a que aparezcan stream candidates
            print("Esperando hasta 60 segundos para capturar streams...")
            for i in range(12):
                await asyncio.sleep(5)
                if m3u8_candidatos:
                    # Probar cada candidato inmediatamente desde el contexto de la página
                    for candidato in m3u8_candidatos[-3:]:  # probamos los últimos 3
                        print(f"🔍 Verificando: {candidato[:100]}...")
                        # Hacer un fetch desde el mismo navegador (respeta cookies, referer, etc.)
                        status = await page.evaluate("""
                            async (url) => {
                                try {
                                    const resp = await fetch(url, {
                                        method: 'GET',
                                        headers: {
                                            'Referer': arguments[1],
                                            'User-Agent': arguments[2]
                                        }
                                    });
                                    return resp.status;
                                } catch(e) {
                                    return 0;
                                }
                            }
                        """, candidato, REFERER, USER_AGENT)
                        if status == 200:
                            print(f"✅ Stream VÁLIDO (status {status}): {candidato[:100]}")
                            stream_valido = candidato
                            break
                        else:
                            print(f"❌ Stream inválido (status {status})")
                    if stream_valido:
                        break
                if stream_valido:
                    break

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

        return stream_valido


def actualizar_animal_planet():
    print("\n🔎 Buscando señal de ANIMAL PLANET...")
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
