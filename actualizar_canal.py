import json, requests, re, os, sys
nombre, iframe_url = sys.argv[1], sys.argv[2]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
r = requests.get(iframe_url, headers=headers)
m3u8 = re.search(r'https?://[^\s"\']+\.m3u8(?:[^\s"\']*)', r.text)
url_final = m3u8.group(0) if m3u8 else iframe_url
with open("honduras.json", "r+", encoding="utf-8") as f:
    data = json.load(f)
    for c in data:
        if c['nombre'].strip().lower() == nombre.strip().lower():
            c['url'] = url_final
            break
    f.seek(0); json.dump(data, f, indent=4, ensure_ascii=False); f.truncate()
os.system("git add honduras.json && git commit -m 'Auto update' && git push origin main")
