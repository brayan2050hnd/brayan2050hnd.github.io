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
# ANIMAL PLANET — MÉTODO IDÉNTICO A WEB VIDEO CASTER
# ============================================================
PAGINA_PRINCIPAL = "https://www.tvporinternet2.com/animal-planet-en-vivo-por-internet.html"
REFERER = PAGINA_PRINCIPAL

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
            user_agent="Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36",
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
        stream_final = None

        try:
            print(f"Cargando página principal: {PAGINA_PRINCIPAL}")
            await page.goto(PAGINA_PRINCIPAL, wait_until="domcontentloaded", timeout=60000)
            print("Página principal cargada. Esperando iframe 'player'...")

            # Esperar hasta 30 segundos a que aparezca el iframe
            try:
                await page.wait_for_selector('iframe[name="player"]', timeout=30000)
            except:
                print("No se encontró el iframe 'player'. Abortando.")
                return None

            # Obtener el frame
            frame = None
            for _ in range(10):  # Reintentar hasta 5 segundos
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
            # Ocultar elementos que bloquean clics
            await frame.evaluate("""
                const blockers = document.querySelectorAll('a, div[style*="absolute"], iframe');
                blockers.forEach(el => {
                    if (el.offsetHeight < 50 || el.id === 'don\\'tfoid') {
                        el.style.display = 'none';
                    }
                });
            """)

            # Forzar reproducción
            await frame.evaluate("""
                (() => {
                    try { if (typeof jwplayer !== 'undefined') { jwplayer().play(); } } catch(e) {}
                    try { if (typeof videojs !== 'undefined') { videojs('player').play(); } } catch(e) {}
                    try { const v = document.querySelector('video'); if (v) v.play(); } catch(e) {}
                })();
            """)
            print("Reproducción forzada. Esperando que el video cargue...")

            # Esperar a que la etiqueta <video> tenga un src con .m3u8
            # (hasta 60 segundos)
            for intento in range(12):
                await asyncio.sleep(5)
                # Buscar el src del video dentro del iframe
                video_src = await frame.evaluate("""
                    () => {
                        const v = document.querySelector('video');
                        if (v && v.src && v.src.includes('.m3u8')) return v.src;
                        // También buscar en JW Player
                        try { if (typeof jwplayer !== 'undefined') { const pl = jwplayer().getPlaylist(); if (pl && pl[0]) return pl[0].file; } } catch(e) {}
                        return null;
                    }
                """)
                if video_src:
                    print(f"📡 Stream encontrado en el DOM: {video_src[:100]}...")
                    # Verificar que el servidor acepta este enlace (usando las cookies del contexto)
                    status = await frame.evaluate("""
                        async (url) => {
                            try {
                                const resp = await fetch(url, { method: 'GET' });
                                return resp.status;
                            } catch(e) { return 0; }
                        }
                    """, video_src)
                    if status == 200:
                        print(f"✅ Stream VÁLIDO (status 200).")
                        stream_final = video_src
                        break
                    else:
                        print(f"❌ Stream inválido (status {status}), esperando más...")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

        return stream_final


def actualizar_animal_planet():
    print("\n🔎 Buscando señal de ANIMAL PLANET (modo Web Video Caster)...")
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
