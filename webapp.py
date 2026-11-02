from flask import Flask, render_template_string, send_from_directory, abort, jsonify, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOMAIN_URL = "https://alhikmah.my.id"

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
        h1, h2 { margin-top: 0; }
        a { color: #0b6b4f; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .badge { background: #e0f2f1; color: #0b6b4f; padding: 0.3rem 0.6rem; border-radius: 4px; font-size: 0.85rem; font-weight: bold; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1rem; }
        .grid-item { background: #f9f9f9; padding: 1rem; border-radius: 6px; border-left: 4px solid #0b6b4f; }
        .btn { background: #0b6b4f; color: white; padding: 0.5rem 1rem; border: none; border-radius: 4px; cursor: pointer; display: inline-block; text-decoration: none; }
        .btn:hover { background: #084c37; color: white; }
        input, textarea, select { width: 100%; padding: 0.5rem; margin-top: 0.5rem; margin-bottom: 1rem; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    </style>
</head>
"""

# Simulasi Database Artikel Otomatis
DATABASE_ARTIKEL = [
    {
        "id": 1,
        "title": "Keutamaan Silaturahmi dan Mempererat Ukhuwah Islamiyah",
        "slug": "keutamaan-silaturahmi-dan-mempererat-ukhuwah",
        "category": "hikmah",
        "date": "2026-06-01",
        "content": "Silaturahmi memiliki kedudukan yang sangat mulia dalam Islam. Selain memperpanjang umur dan melapangkan rezeki, silaturahmi juga merekatkan persaudaraan antar sesama muslim..."
    },
    {
        "id": 2,
        "title": "Panduan Praktis Ibadah di Bulan Suci Ramadhan",
        "slug": "panduan-praktis-ibadah-bulan-ramadhan",
        "category": "ramadhan",
        "date": "2026-06-02",
        "content": "Menyambut bulan suci Ramadhan, umat Islam dianjurkan untuk mempersiapkan diri baik secara fisik maupun spiritual melalui amalan-amalan sunnah..."
    }
]

PROJECT_FOLDERS = ["aplikasi", "calligraphy", "code", "collor", "eq", "finder", "img", "kodepost", "maps", "qr", "quran", "seo", "source", "tools", "vidio"]
STATIC_PAGES = ["about", "academy", "advertise", "archive", "articles", "assets", "budaya", "cerpen", "choices", "contact", "daerah", "disclaimer", "e-course", "editorial", "forum", "hikmah", "humor", "internasional", "join", "kesehatan", "khutbah", "license", "nasional", "news-update", "obituari", "partner", "pidato", "privacy", "private", "puisi", "pustaka", "ramadhan", "redaksi", "risalah", "seni", "sitemap", "terms", "tokoh", "tools", "training", "warta", "komunitas"]

# ==================== HOMEPAGE ====================
@app.route('/')
def index():
    articles_html = "".join([f'<li><a href="/article/{art["slug"]}"><b>{art["title"]}</b></a> <small>({art["category"].upper()})</small></li>' for art in DATABASE_ARTIKEL])
    folders_html = "".join([f'<div class="grid-item">📁 <a href="/{f}"><b>{f.capitalize()}</b></a></div>' for f in PROJECT_FOLDERS])
    
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
                <h2>📝 Artikel & Kajian Terbaru (Otomatis)</h2>
                <ul>
                    {articles_html}
                </ul>
                <hr>
                <a href="/admin/buat-artikel" class="btn">➕ Buat Artikel Otomatis Baru</a>
                <a href="/rss.xml" class="btn" style="background: #e67e22;">📡 RSS Feed</a>
                <a href="/atom.xml" class="btn" style="background: #d35400;">⚛️ Atom Feed</a>
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

# ==================== FITUR BACA ARTIKEL & AMP ====================
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
                <hr>
                <p><a href="/article/{article["slug"]}/amp" class="badge" style="padding: 0.5rem 1rem;">⚡ Buka Versi AMP (Super Cepat)</a></p>
                <br>
                <a href="/">&larr; Kembali ke Beranda</a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/article/<slug>/amp')
def view_article_amp(slug):
    article = next((art for art in DATABASE_ARTIKEL if art["slug"] == slug), None)
    if not article:
        abort(404)
        
    return f"""<!DOCTYPE html>
    <html ⚡ lang="id">
    <head>
        <meta charset="utf-8">
        <title>{article["title"]} (AMP)</title>
        <link rel="canonical" href="{DOMAIN_URL}/article/{slug}">
        <meta name="viewport" content="width=device-width,minimum-scale=1">
        <style>body {{ font-family: sans-serif; padding: 20px; background: #fff; color: #333; }}</style>
    </head>
    <body>
        <h1>{article["title"]}</h1>
        <p><em>Versi AMP Mobile Ready</em></p>
        <hr>
        <p>{article["content"]}</p>
        <p><a href="/article/{slug}">← Kembali ke Versi Reguler</a></p>
    </body>
    </html>"""

# ==================== ADMIN: BUAT ARTIKEL OTOMATIS ====================
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
                    <input type="text" name="title" required placeholder="Contoh: Keutamaan Sedekah Subuh">
                    
                    <label>Kategori (Rubrik):</label>
                    <select name="category">
                        <option value="hikmah">Hikmah</option>
                        <option value="ramadhan">Ramadhan</option>
                        <option value="khutbah">Khutbah</option>
                        <option value="warta">Warta</option>
                        <option value="articles">Articles</option>
                    </select>
                    
                    <label>Isi Konten Artikel:</label>
                    <textarea name="content" rows="6" required placeholder="Tulis kajian atau teks artikel di sini..."></textarea>
                    
                    <button type="submit" class="btn">Publikasikan Sekarang</button>
                </form>
                <br>
                <a href="/">&larr; Batal / Kembali</a>
            </div>
        </div>
    </body>
    </html>
    """)

# ==================== RSS & ATOM FEEDS ====================
@app.route('/rss.xml')
def rss_feed():
    rss = ['<?xml version="1.0" encoding="UTF-8" ?>']
    rss.append('<rss version="2.0"><channel>')
    rss.append('<title>ALHIKMAH RSS Feed</title>')
    rss.append(f'<link>{DOMAIN_URL}</link>')
    rss.append('<description>Warta, kajian Islam, dan tools Islami</description>')
    for art in DATABASE_ARTIKEL:
        rss.append(f'<item><title>{art["title"]}</title><link>{DOMAIN_URL}/article/{art["slug"]}</link><description>{art["content"][:100]}...</description><pubDate>{art["date"]}</pubDate></item>')
    rss.append('</channel></rss>')
    return "\n".join(rss), 200, {'Content-Type': 'application/xml; charset=utf-8'}

@app.route('/atom.xml')
def atom_feed():
    atom = ['<?xml version="1.0" encoding="utf-8"?>']
    atom.append('<feed xmlns="http://www.w3.org/2005/Atom">')
    atom.append('<title>ALHIKMAH Atom Feed</title>')
    atom.append(f'<link href="{DOMAIN_URL}/atom.xml" rel="self"/>')
    atom.append(f'<link href="{DOMAIN_URL}"/>')
    atom.append(f'<updated>{datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}</updated>')
    for art in DATABASE_ARTIKEL:
        atom.append(f'<entry><title>{art["title"]}</title><link href="{DOMAIN_URL}/article/{art["slug"]}"/><id>{DOMAIN_URL}/article/{art["slug"]}</id><updated>{art["date"]}T00:00:00Z</updated><summary>{art["content"][:100]}</summary></entry>')
    atom.append('</feed>')
    return "\n".join(atom), 200, {'Content-Type': 'application/xml; charset=utf-8'}

# ==================== ROUTING FOLDER & HALAMAN STATIS ====================
@app.route('/<folder_name>/')
@app.route('/<folder_name>')
def handle_project_folders(folder_name):
    if folder_name.lower() in PROJECT_FOLDERS:
        return render_template_string(f"""
        <!DOCTYPE html>
        <html lang="id">{META_HEAD}<body><header><h1>Direktori: {folder_name.upper()}</h1></header><div class="container"><div class="card"><h2>Modul Aktif</h2><a href="/">&larr; Kembali</a></div></div></body></html>
        """)
    abort(404)

@app.route('/<page_name>.html')
@app.route('/<page_name>')
def handle_static_pages(page_name):
    if page_name.lower() in STATIC_PAGES:
        return render_template_string(f"""
        <!DOCTYPE html>
        <html lang="id">{META_HEAD}<body><header><h1>Rubrik: {page_name.upper()}</h1></header><div class="container"><div class="card"><a href="/">&larr; Kembali</a></div></div></body></html>
        """)
    abort(404)

@app.route('/sitemap.xml')
def generate_sitemap():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.append(f'<url><loc>{DOMAIN_URL}/</loc></url>')
    for art in DATABASE_ARTIKEL:
        xml.append(f'<url><loc>{DOMAIN_URL}/article/{art["slug"]}</loc></url>')
    for f in PROJECT_FOLDERS:
        xml.append(f'<url><loc>{DOMAIN_URL}/{f}</loc></url>')
    xml.append('</urlset>')
    return "\n".join(xml), 200, {'Content-Type': 'application/xml; charset=utf-8'}

@app.errorhandler(404)
def page_not_found(e):
    return render_template_string(f"""<!DOCTYPE html><html><body style="text-align:center;padding:50px;"><h1>404</h1><p>Halaman tidak ditemukan.</p><a href="/">Beranda</a></body></html>"""), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
