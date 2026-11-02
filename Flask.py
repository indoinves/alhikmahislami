from flask import Flask, render_template_string, send_from_directory, abort, jsonify, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOMAIN_URL = "https://alhikmah.my.id"

# Meta HTML Lengkap dengan OpenGraph, PWA, & Google AdSense
META_HEAD = """
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ALHIKMAH - Berita, kajian, artikel dan tools Islami</title>
    <link rel="icon" href="/favicon.ico">
    <link rel="apple-touch-icon" href="https://blogger.googleusercontent.com/img/a/AVvXsEiW2Sfw5ogSKhZbFiB-VdNXwmZoMGLTGPgx5ZYrTY8859clBvRGxgx-Dwc3i03YiUs1WiiL84uTSAlZ8civ17IWTI5Emt2vXmpuT-yRTzf4620rY_4Ib_vmUEGFfLXjzMiCfmQoWUg1mmj5hQu1IpD1CYguF9GocJ81MhsQTuPgt79-I8uOaPyGT0Qzs00=s200">
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#0b6b4f">
    <link rel="alternate" type="application/rss+xml" title="ALHIKMAH RSS" href="/rss.xml">
    <link rel="alternate" type="application/atom+xml" title="ALHIKMAH Atom" href="/atom.xml">
    <meta name="google-site-verification" content="QT96Rd0InOuqkb4s1Wu5BlgGD_pCNOy8CsCtveF1zEA">
    <meta name="google-site-verification" content="SumuNvHw_nB3fsevMIU9N_0Oi7YWb9ykHovu0gjAbso">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="ALHIKMAH">
    <meta property="og:title" content="ALHIKMAH - Berita, kajian, artikel dan tools Islami">
    <meta property="og:description" content="ALHIKMAH: warta, kajian Islam, artikel budaya, dan tools Islami gratis.">
    <meta property="og:url" content="https://alhikmah.my.id/">
    <meta property="og:image" content="https://alhikmah.my.id/images.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6718454554209533" crossorigin="anonymous"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background: #f4f7f6; color: #333; }
        header { background: #0b6b4f; color: white; padding: 2rem 1rem; text-align: center; }
        .container { max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }
        .card { background: white; padding: 1.5rem; margin-bottom: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        h1, h2, h3 { margin-top: 0; color: #0b6b4f; }
        header h1 { color: white; }
        a { color: #0b6b4f; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .badge { background: #e0f2f1; color: #0b6b4f; padding: 0.3rem 0.6rem; border-radius: 4px; font-size: 0.85rem; font-weight: bold; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1rem; }
        .grid-item { background: #f9f9f9; padding: 1rem; border-radius: 6px; border-left: 4px solid #0b6b4f; }
        .btn { background: #0b6b4f; color: white; padding: 0.5rem 1rem; border: none; border-radius: 4px; cursor: pointer; display: inline-block; text-decoration: none; }
        .btn:hover { background: #084c37; color: white; }
        input, textarea, select { width: 100%; padding: 0.5rem; margin-top: 0.5rem; margin-bottom: 1rem; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        .nav-section { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
        .nav-tag { background: #eef2f3; padding: 0.4rem 0.8rem; border-radius: 4px; font-size: 0.9rem; }
    </style>
</head>
"""

# ==================== STRUKTUR KATEGORI & HALAMAN ====================
PROJECT_FOLDERS = [
    "aplikasi", "calligraphy", "code", "collor", "eq", 
    "finder", "img", "kodepost", "maps", "qr", 
    "quran", "seo", "source", "tools", "vidio"
]

CATEGORY_NEWS = ["news", "politics", "economy", "tech", "sports", "international", "kitab", "kajian", "jurnal"]
CATEGORY_BUDAYA = ["culture", "sejarah", "arts", "kisah", "zodiak", "di-yogyakarta"]
LEGAL_PAGES = ["index", "about", "kontak", "kebijakan-privasi", "syarat-ketentuan", "rubrik", "license", "disclaimer", "forum", "partner", "arsip", "warta-langganan"]

# Gabungan seluruh rute halaman teks/kategori
ALL_ROUTES = CATEGORY_NEWS + CATEGORY_BUDAYA + LEGAL_PAGES

# Database Artikel Simulasi
DATABASE_ARTIKEL = [
    {
        "id": 1,
        "title": "Perkembangan Teknologi Ekonomi Syariah di Era Digital",
        "slug": "perkembangan-teknologi-ekonomi-syariah",
        "category": "economy",
        "date": "2026-06-01",
        "content": "Ekonomi syariah berbasis teknologi digital mengalami pertumbuhan pesat, memberikan kemudahan transaksi serta transparansi bagi umat..."
    },
    {
        "id": 2,
        "title": "Jejak Sejarah dan Budaya Islam di DI Yogyakarta",
        "slug": "jejak-sejarah-dan-budaya-islam-di-di-yogyakarta",
        "category": "di-yogyakarta",
        "date": "2026-06-02",
        "content": "Yogyakarta menyimpan warisan sejarah budaya Islam yang kaya, mulai dari arsitektur masjid kuno hingga tradisi pesantren keraton..."
    }
]

# ==================== HOMEPAGE ====================
@app.route('/')
def index():
    news_links = "".join([f'<a href="/{c}" class="nav-tag">📌 {c.replace("-", " ").title()}</a>' for c in CATEGORY_NEWS])
    budaya_links = "".join([f'<a href="/{b}" class="nav-tag">🏛️ {b.replace("-", " ").title()}</a>' for b in CATEGORY_BUDAYA])
    legal_links = "".join([f'<a href="/{l}" class="nav-tag">⚖️ {l.replace("-", " ").title()}</a>' for l in LEGAL_PAGES])
    folders_html = "".join([f'<div class="grid-item">📁 <a href="/{f}"><b>{f.capitalize()}</b></a><br><small>View Now</small></div>' for f in PROJECT_FOLDERS])
    
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="id">
    {META_HEAD}
    <body>
        <header>
            <div style="font-size: 1.5rem; font-family: serif;">الأمل</div>
            <h1>ALHIKMAH</h1>
            <p>Ahlan wa Sahlan — Warta, kajian, dan tools Islami dalam satu genggaman.</p>
        </header>
        <div class="container">
            <div class="card">
                <h2>📰 Kategori News & Warta</h2>
                <div class="nav-section">{news_links}</div>
            </div>

            <div class="card">
                <h2>🎭 Budaya & Sastra</h2>
                <div class="nav-section">{budaya_links}</div>
            </div>

            <div class="card">
                <h2>⚖️ Halaman Legal & Informasi</h2>
                <div class="nav-section">{legal_links}</div>
            </div>

            <div class="card">
                <h2>⚙️ Panel Kontrol & Artikel</h2>
                <p><a href="/admin/buat-artikel" class="btn" style="background:#e67e22; color:white;">➕ Buat Artikel Baru</a> | <a href="/rss.xml" class="btn">📡 RSS Feed</a></p>
            </div>

            <div class="card">
                <h2>🚀 Live Applications & Directories</h2>
                <div class="grid">
                    {folders_html}
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

# ==================== ROUTING KATEGORI & HALAMAN LEGAL ====================
@app.route('/<path_name>')
def handle_dynamic_routes(path_name):
    path_clean = path_name.lower().strip('/')
    
    # Periksa apakah masuk ke folder proyek
    if path_clean in PROJECT_FOLDERS:
        return render_template_string(f"""
        <!DOCTYPE html>
        <html lang="id">
        {META_HEAD}
        <body>
            <header>
                <h1>Direktori: {path_clean.upper()}</h1>
                <p>Platform ALHIKMAH Live Section</p>
            </header>
            <div class="container">
                <div class="card">
                    <span class="badge">Live Application Active</span>
                    <h2>Modul: {path_clean.capitalize()}</h2>
                    <p>Anda sedang mengakses direktori interaktif <b>{path_clean}</b>.</p>
                    <hr><a href="/">&larr; Kembali ke Beranda Utama</a>
                </div>
            </div>
        </body>
        </html>
        """)
        
    # Periksa apakah masuk ke kategori News, Budaya, atau Legal
    if path_clean in ALL_ROUTES or path_clean == "index":
        if path_clean == "index":
            return redirect(url_for('index'))
            
        return render_template_string(f"""
        <!DOCTYPE html>
        <html lang="id">
        {META_HEAD}
        <body>
            <header>
                <h1>ALHIKMAH - {path_clean.replace('-', ' ').title()}</h1>
            </header>
            <div class="container">
                <div class="card">
                    <h2>Rubrik / Kategori: {path_clean.replace('-', ' ').upper()}</h2>
                    <p>Menampilkan arsip warta, berita, dan informasi terbaru dari rubrik <b>{path_clean}</b>.</p>
                    <hr>
                    <h3>Daftar Terkait:</h3>
                    <ul>
                        <li><a href="/">Telusuri Berita Utama Terkini</a></li>
                        <li><a href="/sitemap.xml">Lihat Peta Situs Lengkap</a></li>
                    </ul>
                    <br><a href="/">&larr; Kembali ke Beranda Utama</a>
                </div>
            </div>
        </body>
        </html>
        """)
        
    abort(404)

# ==================== ARTIKEL & ADMIN ====================
@app.route('/article/<slug>')
def view_article(slug):
    article = next((art for art in DATABASE_ARTIKEL if art["slug"] == slug), None)
    if not article:
        abort(404)
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="id">
    {META_HEAD}
    <body>
        <header>
            <h1>{article["title"]}</h1>
            <p>Kategori: {article["category"].upper()} | Dipublikasikan: {article["date"]}</p>
        </header>
        <div class="container">
            <div class="card">
                <p>{article["content"]}</p>
                <br><a href="/">&larr; Kembali ke Beranda</a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/admin/buat-artikel', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        content = request.form.get('content')
        slug = title.lower().replace(' ', '-').replace(',', '').replace('?', '')
        
        new_art = {
            "id": len(DATABASE_ARTIKEL) + 1,
            "title": title,
            "slug": slug,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "content": content
        }
        DATABASE_ARTIKEL.append(new_art)
        return redirect(url_for('index'))
        
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="id">
    {META_HEAD}
    <body>
        <header>
            <h1>Buat Artikel Otomatis</h1>
        </header>
        <div class="container">
            <div class="card">
                <form method="POST">
                    <label>Judul Artikel:</label>
                    <input type="text" name="title" required placeholder="Judul berita/kajian...">
                    <label>Kategori:</label>
                    <select name="category">
                        <option value="news">News</option>
                        <option value="politics">Politics</option>
                        <option value="economy">Economy</option>
                        <option value="culture">Culture</option>
                        <option value="di-yogyakarta">DI Yogyakarta</option>
                        <option value="kajian">Kajian</option>
                    </select>
                    <label>Isi Konten:</label>
                    <textarea name="content" rows="6" required placeholder="Tulis isi berita..."></textarea>
                    <button type="submit" class="btn">Publikasikan</button>
                </form>
                <br><a href="/">&larr; Batal</a>
            </div>
        </div>
    </body>
    </html>
    """)

# ==================== SITEMAP & FEEDS ====================
@app.route('/sitemap.xml')
def generate_sitemap():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.append(f'  <url><loc>{DOMAIN_URL}/</loc></url>')
    for r in ALL_ROUTES:
        xml.append(f'  <url><loc>{DOMAIN_URL}/{r}</loc></url>')
    for f in PROJECT_FOLDERS:
        xml.append(f'  <url><loc>{DOMAIN_URL}/{f}</loc></url>')
    for art in DATABASE_ARTIKEL:
        xml.append(f'  <url><loc>{DOMAIN_URL}/article/{art["slug"]}</loc></url>')
    xml.append('</urlset>')
    return "\n".join(xml), 200, {'Content-Type': 'application/xml; charset=utf-8'}

@app.route('/rss.xml')
def rss_feed():
    rss = ['<?xml version="1.0" encoding="UTF-8" ?>', '<rss version="2.0"><channel>']
    rss.append('<title>ALHIKMAH RSS Feed</title>')
    rss.append(f'<link>{DOMAIN_URL}</link>')
    rss.append('<description>Warta, kajian Islam, dan tools Islami</description>')
    for art in DATABASE_ARTIKEL:
        rss.append(f'<item><title>{art["title"]}</title><link>{DOMAIN_URL}/article/{art["slug"]}</link><description>{art["content"][:100]}...</description><pubDate>{art["date"]}</pubDate></item>')
    rss.append('</channel></rss>')
    return "\n".join(rss), 200, {'Content-Type': 'application/xml; charset=utf-8'}

# ==================== ROOT FILES & ERROR HANDLER ====================
ROOT_FILES = {
    "ads.txt": "google.com, pub-6718454554209533, DIRECT, f08c47fec0942fa0",
    "app-ads.txt": "google.com, pub-6718454554209533, DIRECT, f08c47fec0942fa0",
    "robots.txt": f"User-agent: *\nAllow: /\nSitemap: {DOMAIN_URL}/sitemap.xml",
    "manifest.json": '{"name": "ALHIKMAH", "short_name": "Alhikmah", "start_url": "/", "display": "standalone", "theme_color": "#0b6b4f"}'
}

@app.route('/<filename>')
def serve_root_files(filename):
    if filename in ROOT_FILES:
        return ROOT_FILES[filename], 200, {'Content-Type': 'text/plain; charset=utf-8'}
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.isfile(file_path):
        return send_from_directory(BASE_DIR, filename)
    abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="id">
    {META_HEAD}
    <body>
        <header style="background: #a93226;">
            <h1>404 - Halaman Tidak Ditemukan</h1>
            <p>Maaf, tautan atau kategori yang Anda tuju tidak tersedia.</p>
        </header>
        <div class="container" style="text-align: center;">
            <div class="card">
                <a href="/" class="btn">Kembali ke Beranda</a>
            </div>
        </div>
    </body>
    </html>
    """), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
