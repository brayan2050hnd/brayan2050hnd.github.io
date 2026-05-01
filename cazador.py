import json
import asyncio
from playwright.async_api import async_playwright

async def capturar_link():
    url_objetivo = "https://www.tvporinternet2.com/animal-planet-en-vivo-por-internet.html"
    link_encontrado = None

    async with async_playwright() as p:
        # Abrimos un navegador invisible
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = await context.new_page()

        # Esta es la parte mágica: "Escuchamos" todas las peticiones de red
        def interceptar_peticiones(request):
            nonlocal link_encontrado
            # Si la petición es un m3u8 y contiene la palabra clave que viste en Web Video Caster
            if ".m3u8" in request.url and "regionales" in request.url:
                link_encontrado = request.url
                print(f"¡CAPTURADO EN LA RED!: {link_encontrado}")

        page.on("request", interceptar_peticiones)

        print(f"Navegando a la página...")
        try:
            # Entramos y esperamos a que cargue el contenido
            await page.goto(url_objetivo, wait_until="networkidle", timeout=60000)
            
            # Esperamos 15 segundos extra para que el JavaScript genere el link
            await asyncio.sleep(15) 
            
        except Exception as e:
            print(f"Error al cargar: {e}")
        
        await browser.close()
    
    return link_encontrado

def actualizar_json(nuevo_link):
    if not nuevo_link:
        print("No se pudo capturar ningún link esta vez.")
        return

    try:
        with open('usa.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for canal in data:
            if "ANIMAL PLANET" in canal.get('nombre', '').upper():
                canal['url'] = nuevo_link
                print("usa.json actualizado con el link dinámico.")

        with open('usa.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar el JSON: {e}")

if __name__ == "__main__":
    # Ejecutamos el capturador
    loop = asyncio.get_event_loop()
    link = loop.run_until_complete(capturar_link())
    
    # Si lo encontró, lo guarda
    if link:
        actualizar_json(link)
