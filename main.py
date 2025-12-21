import requests
import re
import datetime
from bs4 import BeautifulSoup

# --- AYARLAR ---
OUTPUT_FILE = "Canli_Spor_Hepsi.m3u"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
WORKING_BS1_URL = "https://andro.adece12.sbs/checklist/receptestt.m3u8"

# --- 1. WON-IPTV LİSTESİ (SABİT KANALLAR) ---
def get_won_iptv_static():
    print("[*] WON-IPTV kanalları (Ulusal ve Sinema) ekleniyor...")
    return [
        # ULUSAL
        {"n": "TRT 1 HD", "u": "https://tv-trt1.medya.trt.com.tr/master.m3u8", "g": "TURKIYE ULUSAL", "l": "https://feo.kablowebtv.com/resize/168A635D265A4328C2883FB4CD8FF/0/0/Vod/HLS/80196fc2-f4f6-4e35-ae29-7925a5885a20.png"},
        {"n": "ATV HD", "u": "https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv.m3u8", "g": "TURKIYE ULUSAL", "l": "https://feo.kablowebtv.com/resize/168A635D265A4328C2883FB4CD8FF/0/0/Vod/HLS/33b10329-faa9-4247-aa46-92a305ed5a92.png"},
        {"n": "KANAL D HD", "u": "https://demiroren.daioncdn.net/kanald/kanald.m3u8?app=kanald_web", "g": "TURKIYE ULUSAL", "l": "https://feo.kablowebtv.com/resize/168A635D265A4328C2883FB4CD8FF/500/500/channels/logos/d7c5d3d5-2942-4715-872f-73be070dc201.png"},
        {"n": "SHOW TV HD", "u": "https://ciner.daioncdn.net/showtv/showtv.m3u8?app=showtv_web", "g": "TURKIYE ULUSAL", "l": "https://feo.kablowebtv.com/resize/168A635D265A4328C2883FB4CD8FF/500/500/channels/logos/04fb743d-4a72-4907-8c54-f53b72c3600a.png"},
        {"n": "STAR TV HD", "u": "https://dogus.daioncdn.net/startv/startv.m3u8?app=startv_web", "g": "TURKIYE ULUSAL", "l": "https://feo.kablowebtv.com/resize/168A635D265A4328C2883FB4CD8FF/500/500/channels/logos/4a7901e4-dbc5-491d-b014-6da6fa236e99.png"},
        {"n": "NOW TV HD", "u": "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/nowtv/nowtv_720p.m3u8", "g": "TURKIYE ULUSAL", "l": "https://feo.kablowebtv.com/resize/168A635D265A4328C2883FB4CD8FF/0/0/Vod/HLS/25c7c620-dfe4-4c78-9d9b-185d8a91885f.png"},
        {"n": "TV 8 HD", "u": "https://tv8.daioncdn.net/tv8/tv8_1080p.m3u8?app=tv8_web", "g": "TURKIYE ULUSAL", "l": "https://feo.kablowebtv.com/resize/168A635D265A4328C2883FB4CD8FF/0/0/Vod/HLS/ab41b407-70c4-4634-8ed4-bf9be8cf81e2.png"},
        {"n": "TV 8.5 HD", "u": "https://tv8.daioncdn.net/tv8bucuk/tv8bucuk_1080p.m3u8?app=tv8bucuk_web", "g": "TURKIYE ULUSAL", "l": "https://feo.kablowebtv.com/resize/168A635D265A4328C2883FB4CD8FF/0/0/Vod/HLS/812f4ba5-846e-4ae9-90fc-8f9f481156b5.png"},
        {"n": "A2 HD", "u": "https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/a2tv/a2tv_1080p.m3u8", "g": "TURKIYE ULUSAL", "l": "https://feo.kablowebtv.com/resize/168A635D265A4328C2883FB4CD8FF/0/0/Vod/HLS/fee44d61-2476-40ae-89eb-f51a7428789d.png"},
        {"n": "CNBC-E HD", "u": "https://hnpsechtsc.turknet.ercdn.net/xpnvudnlsv/cnbc-e/cnbc-e.m3u8", "g": "TURKIYE ULUSAL", "l": "https://feo.kablowebtv.com/resize/168A635D265A4328C2883FB4CD8FF/0/0/Vod/HLS/16752eb5-4001-4b31-860c-ab947ed2c86d.png"},
        {"n": "TRT BELGESEL HD", "u": "http://tv-trtbelgesel.medya.trt.com.tr/master_720.m3u8", "g": "TURKIYE ULUSAL", "l": "https://feo.kablowebtv.com/resize/168A635D265A4328C2883FB4CD8FF/0/0/Vod/HLS/6925f7f0-2d64-4a15-99ec-e4a19c117279.png"},
        
        # SINEMA TV (WON-IPTV'DEKİ TÜM LİSTE)
        {"n": "Sinema TV 1 HD", "u": "https://cdn18.yayin.com.tr/nowplay/tracks-v1a1/mono.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
        {"n": "Sinema TV 2 HD", "u": "https://mediaserver1.castpin.com/hls/filbox/1_2/index.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
        {"n": "Sinema TV 3 HD", "u": "https://a8.radyotelekom.com.tr:3899/stream/play.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
        {"n": "Sinema TV 4 HD", "u": "https://raw.githubusercontent.com/Elvin4K/restream/refs/heads/pro4k/1siriustv.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
        {"n": "Sinema TV 5 HD", "u": "https://edge-e3.evrideo.tv/f2dcbecf-5af0-47db-a82e-032112050a23_1000027346_HLS/manifest.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
        {"n": "Sinema TV 6 HD", "u": "https://cdn-cine5.yayin.com.tr/cine5/cine5/chunklist.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
        {"n": "Sinema TV 7 HD", "u": "https://ip100.radyotelekomtv.com:3303/stream/play.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
        {"n": "Sinema TV 8 HD", "u": "https://host.onlineradyotv.net:8081/sdmtv/tracks-v1a1/mono.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
        {"n": "Sinema TV 9 HD", "u": "https://cdn-onstv.yayin.com.tr/onstv/index.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
        {"n": "Sinema TV 10 HD", "u": "https://live.artidijitalmedya.com/artidijital_bikanal/bikanal/chunks.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
        {"n": "Sinema TV 11 HD", "u": "https://live.artidijitalmedya.com/artidijital_cine1/cine1/chunks.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
        {"n": "Sinema TV 12 HD", "u": "https://ip100.radyotelekomtv.com:3784/stream/play.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
        {"n": "Sinema TV 13 HD", "u": "https://trn03.tulix.tv/gt-tivi6/tracks-v1a1/rewind-588800.m3u8", "g": "TURKIYE SINEMA", "l": "https://i.hizliresim.com/2qpuwst.jpg"},
    ]

# --- 2. VAVOO SPOR SİSTEMİ ---
def fetch_vavoo():
    print("[*] Vavoo Spor kanalları ekleniyor...")
    res = []
    pb = "https://yildiziptv-turktv.hf.space/proxy/hls/manifest.m3u8?d=https://vavoo.to/vavoo-iptv/play/"
    v_list = [
        {"n": "beIN SPORTS 1 HD", "id": "257621689779b8fed9899e"},
        {"n": "beIN SPORTS 2 FHD", "id": "3694662475b76c08f52108"},
        {"n": "beIN SPORTS 3 FHD", "id": "34101675603c7aea8fa6b1"},
        {"n": "beIN SPORTS MAX 1", "id": "2832430535849b88f81e2d"}
    ]
    for ch in v_list:
        res.append({"name": f"VAVOO - {ch['n']}", "url": f"{pb}{ch['id']}", "group": "VAVOO SPOR (STABIL)", "logo": "https://www.digiturkburada.com.tr/kanal3/bein-sports-hd-1-1.png"})
    return res

# --- 3. NETSPOR SİSTEMİ (BOT TARAMA) ---
def fetch_netspor():
    print("[*] Netspor güncel maçlar taranıyor...")
    results = []
    source = "https://netspor-amp.xyz/"
    base = "https://andro.adece12.sbs/checklist/"
    try:
        r = requests.get(source, headers=HEADERS, timeout=10)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        for div in soup.find_all('div', class_='mac', option=True):
            sid = div.get('option')
            title_div = div.find('div', class_='match-takimlar')
            if not title_div: continue
            title = title_div.get_text(strip=True)
            group = "Günün Maçları (Net)" if not div.find_parent('div', id='kontrolPanelKanallar') else "NET CANLI TV"
            
            # beIN 1 Otomatik Tamir
            f_url = WORKING_BS1_URL if sid == "androstreamlivebs1" else f"{base}{sid}.m3u8"
            results.append({"name": title, "url": f_url, "group": group, "ref": source})
    except: pass
    return results

# --- 4. TRGOALS / SELCUK SİSTEMİ ---
def fetch_others():
    print("[*] Diğer spor kaynakları taranıyor...")
    results = []
    # Trgoals tam liste ID'leri
    ids = {"yayin1":"BEIN 1", "yayinb2":"BEIN 2", "yayinss":"S SPORT", "yayint1":"TIVIBU 1"}
    # Aktif domain bulma ve ekleme mantığı (Basitleştirilmiş)
    # ... (Burada Trgoals ve Selçuk tarama kodun çalışmaya devam eder)
    return results

# --- ANA ÇALIŞTIRICI ---
def main():
    final_list = []
    
    # 1. WON-IPTV Ulusal ve Sinemalar (En Üstte)
    for c in get_won_iptv_static():
        final_list.append(f'#EXTINF:-1 tvg-logo="{c["l"]}" group-title="{c["g"]}",{c["n"]}\n{c["u"]}\n')
    
    # 2. Vavoo Spor
    for v in fetch_vavoo():
        final_list.append(f'#EXTINF:-1 tvg-logo="{v["logo"]}" group-title="{v["group"]}",{v["name"]}\n{v["url"]}\n')
        
    # 3. Netspor Bot Verileri
    for n in fetch_netspor():
        final_list.append(f'#EXTINF:-1 group-title="{n["group"]}",{n["name"]}\n#EXTVLCOPT:http-referrer={n["ref"]}\n{n["url"]}\n')

    # Dosyayı Kaydet
    with open(OUTPUT_FILE, "w", encoding="utf-8-sig") as f:
        f.write("#EXTM3U\n")
        f.write(f"# Son Guncelleme: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        f.writelines(final_list)
    print(f"\n[OK] Tüm kanallar (WON + Bot) başarıyla birleştirildi.")

if __name__ == "__main__":
    main()
