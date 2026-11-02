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
    <meta property="og:description" content="ALHIKMAH: warta, kajian Islam, artikel budaya, dan tools Islami gratis (Al-Qur'an, jadwal sholat, kiblat, zakat).">
    <meta property="og:url" content="https://alhikmah.my.id/">
    <meta property="og:image" content="https://alhikmah.my.id/images.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6718454554209533" crossorigin="anonymous"></script>
    <meta name="google-adsense-account" content="ca-pub-6718454554209533">
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

# Daftar 15 Direktori / Folder Proyek Utama
PROJECT_FOLDERS = [
    "aplikasi", "calligraphy", "code", "collor", "eq", 
    "finder", "img", "kodepost", "maps", "qr", 
    "quran", "seo", "source", "tools", "vidio"
]

# Daftar Halaman Statis & Rubrik Arsip
STATIC_PAGES = [
    "about", "academy", "advertise", "archive", "articles", "assets", "budaya", 
    "cerpen", "choices", "contact", "daerah", "disclaimer", "e-course", "editorial", 
    "forum", "hikmah", "humor", "internasional", "join", "kesehatan", "khutbah", 
    "license", "nasional", "news-update", "obituari", "partner", "pidato", 
    "privacy", "private", "puisi", "pustaka", "ramadhan", "redaksi", "risalah", 
    "seni", "sitemap", "terms", "tokoh", "tools", "training", "warta", "komunitas"
]

# Database Sementara Artikel Otomatis
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

# ==================== HOMEPAGE ====================
@app.route('/')
def index():
    articles_html = "".join([f'<li><a href="/article/{art["slug"]}"><b>{art["title"]}</b></a> <small>({art["category"].upper()})</small></li>' for art in DATABASE_ARTIKEL])
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
                <h2>⚡ Navigasi & Fitur Utama Ekosistem</h2>
                <ul>
                    <li>✍️ <b>Arabic Pegon</b> – Sistem penulisan dan konversi aksara Arab Pegon.</li>
                    <li>✒️ <b>Arabic Calligraphy Pro</b> – Generator & editor kaligrafi berbasis vektor.</li>
                    <li>📅 <b>Kalender Multi-Konversi</b> – Masehi, Hijriah, dan Jawa.</li>
                    <li>⏱️ <b>Timer Jadwal Sholat</b> – Pengingat waktu salat fardu real-time.</li>
                    <li>🎧 <b>Murotal 30 Juz & Al-Qur'an Digital</b>.</li>
                    <li>💼 <b>WebOffice Suite & Khazanah Kitab Klasik</b>.</li>
                </ul>
                <hr>
                <p>⚙️ <b>Panel Kontrol:</b> <a href="/admin/generator" class="btn" style="color:white;">Jalankan Generator Sistem</a> | <a href="/admin/buat-artikel" class="btn" style="background:#e67e22; color:white;">➕ Buat Artikel Baru</a></p>
            </div>

            <div class="card">
                <h2>📝 Kajian & Artikel Terbaru</h2>
                <ul>
                    {articles_html}
                </ul>
                <p><a href="/rss.xml">📡 RSS Feed</a> | <a href="/atom.xml">⚛️ Atom Feed</a></p>
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

# ==================== ROUTING ARTIKEL & AMP ====================
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
                <p><a href="/article/{article["slug"]}/amp" class="badge">⚡ Buka Versi AMP</a></p>
                <br><a href="/">&larr; Kembali ke Beranda</a>
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
                    <input type="text" name="title" required placeholder="Judul kajian...">
                    <label>Kategori:</label>
                    <select name="category">
                        <option value="hikmah">Hikmah</option>
                        <option value="ramadhan">Ramadhan</option>
                        <option value="khutbah">Khutbah</option>
                        <option value="warta">Warta</option>
                    </select>
                    <label>Isi Konten:</label>
                    <textarea name="content" rows="6" required placeholder="Tulis isi kajian..."></textarea>
                    <button type="submit" class="btn">Publikasikan</button>
                </form>
                <br><a href="/">&larr; Batal</a>
            </div>
        </div>
    </body>
    </html>
    """)

# ==================== BACKEND GENERATOR & GIT MANAGER ====================
@app.route('/admin/generator')
def run_generator_script():
    try:
        blog_sitemap_path = os.path.join(BASE_DIR, "sitemap-blog.xml")
        with open(blog_sitemap_path, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            for art in DATABASE_ARTIKEL:
                f.write(f'  <url><loc>{DOMAIN_URL}/article/{art["slug"]}</loc><lastmod>{art["date"]}</lastmod></url>\n')
            f.write('</urlset>')
        status_msg = "Sukses meregenerasi sitemap, RSS feed, dan file AMP secara otomatis!"
    except Exception as e:
        status_msg = f"Gagal menjalankan generator: {str(e)}"

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="id">
    {META_HEAD}
    <body>
        <header>
            <h1>System Generator & Automation</h1>
        </header>
        <div class="container">
            <div class="card">
                <h2>Log Eksekusi:</h2>
                <p style="background: #e8f8f5; padding: 1rem; border-left: 4px solid #0b6b4f;">{status_msg}</p>
                <br><a href="/" class="btn">&larr; Kembali ke Beranda</a>
            </div>
        </div>
    </body>
    </html>
    """)

# ==================== ROUTING FOLDER PROYEK (15 FOLDER) ====================
@app.route('/<folder_name>/')
@app.route('/<folder_name>')
def handle_project_folders(folder_name):
    if folder_name.lower() in PROJECT_FOLDERS:
        return render_template_string(f"""
        <!DOCTYPE html>
        <html lang="id">
        {META_HEAD}
        <body>
            <header>
                <h1>Direktori: {folder_name.upper()}</h1>
                <p>Platform ALHIKMAH Live Section</p>
            </header>
            <div class="container">
                <div class="card">
                    <span class="badge">Live Application Active</span>
                    <h2>Modul: {folder_name.capitalize()}</h2>
                    <p>Anda sedang mengakses direktori interaktif <b>{folder_name}</b>.</p>
                    <hr><a href="/">&larr; Kembali ke Beranda Utama</a>
                </div>
            </div>
        </body>
        </html>
        """)
    abort(404)

# ==================== ROUTING HALAMAN STATIS ====================
@app.route('/<page_name>.html')
@app.route('/<page_name>')
def handle_static_pages(page_name):
    if page_name.lower() in STATIC_PAGES:
        return render_template_string(f"""
        <!DOCTYPE html>
        <html lang="id">
        {META_HEAD}
        <body>
            <header>
                <h1>ALHIKMAH - {page_name.replace('-', ' ').title()}</h1>
            </header>
            <div class="container">
                <div class="card">
                    <h2>Rubrik: {page_name.upper()}</h2>
                    <p>Halaman resmi portal informasi dan arsip <b>{page_name}</b>.</p>
                    <hr><a href="/">&larr; Kembali ke Beranda Utama</a>
                </div>
            </div>
        </body>
        </html>
        """)
    abort(404)

# ==================== FEED & SITEMAP XML ====================
@app.route('/sitemap.xml')
def generate_sitemap():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.append(f'  <url><loc>{DOMAIN_URL}/</loc></url>')
    for art in DATABASE_ARTIKEL:
        xml.append(f'  <url><loc>{DOMAIN_URL}/article/{art["slug"]}</loc></url>')
    for f in PROJECT_FOLDERS:
        xml.append(f'  <url><loc>{DOMAIN_URL}/{f}</loc></url>')
    for p in set(STATIC_PAGES):
        xml.append(f'  <url><loc>{DOMAIN_URL}/{p}</loc></url>')
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

@app.route('/atom.xml')
def atom_feed():
    atom = ['<?xml version="1.0" encoding="utf-8"?>', '<feed xmlns="http://www.w3.org/2005/Atom">']
    atom.append('<title>ALHIKMAH Atom Feed</title>')
    atom.append(f'<link href="{DOMAIN_URL}/atom.xml" rel="self"/>')
    atom.append(f'<link href="{DOMAIN_URL}"/>')
    for art in DATABASE_ARTIKEL:
        atom.append(f'<entry><title>{art["title"]}</title><link href="{DOMAIN_URL}/article/{art["slug"]}"/><id>{DOMAIN_URL}/article/{art["slug"]}</id><updated>{art["date"]}T00:00:00Z</updated></entry>')
    atom.append('</feed>')
    return "\n".join(atom), 200, {'Content-Type': 'application/xml; charset=utf-8'}

@app.route('/search.json')
def search_json():
    data = [{"title": f.capitalize(), "url": f"/{f}", "type": "application"} for f in PROJECT_FOLDERS]
    data += [{"title": p.replace('-', ' ').title(), "url": f"/{p}", "type": "rubrik"} for p in set(STATIC_PAGES)]
    return jsonify(data)

# ==================== FILE ROOT & ERROR HANDLER ====================
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
            <p>Maaf, tautan yang Anda tuju tidak tersedia di platform ALHIKMAH.</p>
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
