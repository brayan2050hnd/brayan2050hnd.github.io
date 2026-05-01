import cloudscraper
import re
import json

def actualizar_zaz(scraper):
    fuente_zaz = "https://www.cxtvenvivo.com/tv-en-vivo/zaz-tv"
    try:
        res = scraper.get(fuente_zaz, timeout=15).text
        links = re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', res)
        if links:
            link_v = links[0].replace('\\/', '/')
            with open('mexico.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            for canal in data:
                if canal.get('nombre') == "ZAZ":
                    canal['url'] = link_v
            with open('mexico.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("¡LOGRADO!: ZAZ actualizado.")
    except Exception as e:
        print(f"Error en ZAZ: {e}")

def actualizar_animal_planet(scraper):
    # Nueva fuente que me pasaste
    fuente_ap = "https://www.tvporinternet2.com/animal-planet-en-vivo-por-internet.html"
    print(f"Buscando Animal Planet en: {fuente_ap}")
    
    try:
        headers = {'Referer': 'https://www.google.com/'}
        response = scraper.get(fuente_ap, headers=headers, timeout=15).text
        
        # 1. Buscamos links m3u8 directos o dentro de scripts
        links = re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', response)
        
        # 2. Si no hay, buscamos iframes (reproductores ocultos)
        if not links:
            iframes = re.findall(r'src=["\'](https?://[^\s<>"\']+?)["\']', response)
            for f_url in iframes:
                if any(x in f_url for x in ['google', 'ads', 'facebook', 'twitter']): continue
                try:
                    f_res = scraper.get(f_url, headers={'Referer': fuente_ap}, timeout=10).text
                    links.extend(re.findall(r'https?://[^\s<>"\']+?\.m3u8[^\s<>"\']*', f_res))
                    if links: break
                except: continue

        link_final = None
        for l in links:
            l_limpio = l.replace('\\/', '/').split('"')[0].split("'")[0]
            # Filtro de seguridad: ignorar basura de anuncios
            if any(x in l_limpio.lower() for x in ['wcpkck', 'ads', 'pop', 'click']): continue
            link_final = l_limpio
            break

        if link_final:
            with open('usa.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            for canal in data:
                if "ANIMAL PLANET" in canal.get('nombre', '').upper():
                    canal['url'] = link_final
            with open('usa.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"¡LOGRADO!: Animal Planet actualizado con {link_final}")
        else:
            print("No se encontró link m3u8 para Animal Planet en esta web.")

    except Exception as e:
        print(f"Error en Animal Planet: {e}")

def main():
    # Simulamos un navegador Android para que la web nos dé el link m3u8 móvil
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'android','desktop': False})
    actualizar_zaz(scraper)
    actualizar_animal_planet(scraper)

if __name__ == "__main__":
    main()
