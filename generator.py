import json
import datetime
from pathlib import Path
from PIL import Image

DOMAIN = "https://alhikmah.my.id"
SITE_NAME = "ALHIKMAH"
SITE_DESC = "ALHIKMAH: warta, kajian Islam, artikel budaya, dan tools Islami gratis (Al-Qur'an, jadwal sholat, kiblat, zakat)."
GA_PUB_ID = "ca-pub-6718454554209533"
GOOGLE_VERIFICATION_1 = "QT96Rd0InOuqkb4s1Wu5BlgGD_pCNOy8CsCtveF1zEA"
GOOGLE_VERIFICATION_2 = "SumuNvHw_nB3fsevMIU9N_0Oi7YWb9ykHovu0gjAbso"
THEME_COLOR = "#0b6b4f"

EMAIL = "hello@alhikmah.my.id"
PHONE = "+62 812-3456-7890"
ADDRESS = "Indonesia"
WHATSAPP = "https://wa.me/6281234567890"

SOCIAL_LINKS = [
    ("Facebook", "https://facebook.com/alhikmah"),
    ("Instagram", "https://instagram.com/alhikmah"),
    ("X / Twitter", "https://twitter.com/alhikmah"),
    ("YouTube", "https://youtube.com/@alhikmah"),
]

TOOLS_LIST = [
    "Al-Qur'an", "Wirid & Do'a", "Jadwal Sholat", "Kalender Hijriyah", "Kalender Masehi",
    "Kiblat", "Khutbah", "Yasin", "Tahlil", "Maulid", "Hizib", "Tafsir", "Hadist Bukhori",
    "Hadist Muslim", "Fiqih", "Tasawuf", "Kisah Hikmah", "Maps Location", "Maps Ziarah",
    "Haji Umroh", "Qurban", "Kalkulator Zakat", "Ramadhan", "Alhikmah Pedia",
    "Arabic Keyboard", "Caligrafi Tools", "JSON Beautifier & Minifier",
    "Base64 Encode/Decode", "Random Password Generator", "Morse Code Translator",
    "HEX to RGB Converter"
]

ARTICLES = [
    {
        "title": "Panduan Sholat Sunnah di Bulan Ramadan",
        "slug": "panduan-sholat-sunnah-bulan-ramadan",
        "category": "Ramadhan",
        "label": "Ramadan",
        "year": 2026,
        "date": "2026-11-01",
        "read_time": "5 menit",
        "excerpt": "Sholat sunnah di bulan Ramadan memiliki banyak keutamaan dan membantu memperkuat ibadah harian.",
        "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80"
    },
    {
        "title": "Makna Syukur Dalam Kehidupan Sehari-hari",
        "slug": "makna-syukur-dalam-kehidupan-sehari-hari",
        "category": "Kajian",
        "label": "Akhlak",
        "year": 2026,
        "date": "2026-10-20",
        "read_time": "6 menit",
        "excerpt": "Syukur dan kesadaran spiritual menjadi fondasi untuk membangun kehidupan yang lebih damai.",
        "image": "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=900&q=80"
    },
    {
        "title": "Kaligrafi Islam dan Nilai Estetika dalam Iman",
        "slug": "kaligrafi-islam-dan-nilai-estetika-dalam-iman",
        "category": "Seni",
        "label": "Seni",
        "year": 2025,
        "date": "2025-12-15",
        "read_time": "5 menit",
        "excerpt": "Kaligrafi bukan hanya seni visual, tetapi juga ekspresi spiritual yang mengajak jiwa kepada ketenangan.",
        "image": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=900&q=80"
    },
    {
        "title": "Panduan Praktis Menghafal Al-Qur'an",
        "slug": "panduan-praktis-menghafal-al-quran",
        "category": "Pustaka",
        "label": "Al-Qur'an",
        "year": 2025,
        "date": "2025-11-11",
        "read_time": "7 menit",
        "excerpt": "Belajar menghafal Al-Qur'an memerlukan niat yang kuat, kedisiplinan, dan metode yang konsisten.",
        "image": "https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=900&q=80"
    }
]

ASSET_DIR = Path("assets")
LOGO_CANDIDATES = [
    ASSET_DIR / "logo.png",
    ASSET_DIR / "logo.jpg",
    ASSET_DIR / "logo.jpeg",
    Path("logo.png"),
    Path("logo.jpg"),
    Path("logo.jpeg"),
]
LOGO_URL = f"{DOMAIN}/images.jpg"
FAVICON_URL = f"{DOMAIN}/favicon.png"


def find_logo_source():
    for p in LOGO_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError("Logo tidak ditemukan. Simpan logo di assets/logo.png")


def prepare_assets():
    ASSET_DIR.mkdir(exist_ok=True)
    source = find_logo_source()

    with Image.open(source) as img:
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
        img.save("images.jpg", "JPEG", quality=95)

    with Image.open(source) as img:
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
        img.thumbnail((256, 256))
        img.save("favicon.png", "PNG")


def get_meta_tags(title, description, path="/"):
    return f"""<!DOCTYPE html>
<html lang=\"id\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{title}</title>
    <meta name=\"description\" content=\"{description}\">
    <link rel=\"icon\" href=\"{FAVICON_URL}\" type=\"image/png\">
    <link rel=\"apple-touch-icon\" href=\"{LOGO_URL}\">
    <link rel=\"manifest\" href=\"/manifest.json\">
    <meta name=\"theme-color\" content=\"{THEME_COLOR}\">
    <meta name=\"google-site-verification\" content=\"{GOOGLE_VERIFICATION_1}\">
    <meta name=\"google-site-verification\" content=\"{GOOGLE_VERIFICATION_2}\">
    <meta name=\"google-adsense-account\" content=\"{GA_PUB_ID}\">
    <meta property=\"og:type\" content=\"website\">
    <meta property=\"og:site_name\" content=\"{SITE_NAME}\">
    <meta property=\"og:title\" content=\"{title}\">
    <meta property=\"og:description\" content=\"{description}\">
    <meta property=\"og:url\" content=\"{DOMAIN}{path}\">
    <meta property=\"og:image\" content=\"{LOGO_URL}\">
    <meta name=\"twitter:card\" content=\"summary_large_image\">
    <meta name=\"twitter:title\" content=\"{title}\">
    <meta name=\"twitter:description\" content=\"{description}\">
    <meta name=\"twitter:image\" content=\"{LOGO_URL}\">
    <script async src=\"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={GA_PUB_ID}\" crossorigin=\"anonymous\"></script>
    <link rel=\"stylesheet\" href=\"/css/style.css\">
</head>
<body>
"""


def header_html():
    nav_links = (
        "<a href='/'>Home</a>"
        "<a href='/articles'>Artikel</a>"
        "<a href='/warta'>Warta</a>"
        "<a href='/nasional'>Nasional</a>"
        "<a href='/daerah'>Daerah</a>"
        "<a href='/internasional'>Internasional</a>"
        "<a href='/risalah'>Risalah</a>"
        "<a href='/redaksi'>Redaksi</a>"
        "<a href='/tokoh'>Tokoh</a>"
        "<a href='/hikmah'>Hikmah</a>"
        "<a href='/kesehatan'>Kesehatan</a>"
        "<a href='/cerpen'>Cerpen</a>"
        "<a href='/puisi'>Puisi</a>"
        "<a href='/pidato'>Pidato</a>"
        "<a href='/khutbah'>Khutbah</a>"
        "<a href='/seni'>Seni</a>"
        "<a href='/budaya'>Budaya</a>"
        "<a href='/ramadhan'>Ramadhan</a>"
        "<a href='/pustaka'>Pustaka</a>"
        "<a href='/humor'>Humor</a>"
        "<a href='/tools'>Tools Islami</a>"
        "<a href='/archive'>Archive</a>"
        "<a href='/about'>About</a>"
        "<a href='/contact'>Contact</a>"
    )
    return f"""
    <header class=\"topbar\">
        <div class=\"container topbar-inner\">
            <div class=\"brand\">
                <div class=\"brand-mark\"><img src=\"{LOGO_URL}\" alt=\"{SITE_NAME}\"></div>
                <span>{SITE_NAME}</span>
            </div>
            <nav class=\"nav\">
                {nav_links}
            </nav>
        </div>
    </header>
    """


def footer_html():
    return f"""
    <footer>
        <div class=\"container\">
            <div class=\"footer-grid\">
                <div>
                    <div class=\"brand\" style=\"margin-bottom: 12px;\">
                        <div class=\"brand-mark\"><img src=\"{LOGO_URL}\" alt=\"{SITE_NAME}\"></div>
                        <span>{SITE_NAME}</span>
                    </div>
                    <p>{SITE_DESC}</p>
                    <div class=\"share-box\" style=\"margin-top: 14px;\">
                        <a href=\"https://facebook.com/sharer/sharer.php?u={DOMAIN}\" target=\"_blank\" rel=\"noreferrer\">Facebook</a>
                        <a href=\"https://twitter.com/intent/tweet?url={DOMAIN}\" target=\"_blank\" rel=\"noreferrer\">Twitter</a>
                        <a href=\"https://wa.me/?text={DOMAIN}\" target=\"_blank\" rel=\"noreferrer\">WhatsApp</a>
                    </div>
                </div>

                <div>
                    <h4>Navigasi</h4>
                    <ul>
                        <li><a href=\"/\">Beranda</a></li>
                        <li><a href=\"/articles\">Artikel</a></li>
                        <li><a href=\"/warta\">Warta</a></li>
                        <li><a href=\"/khutbah\">Khutbah</a></li>
                        <li><a href=\"/tools\">Tools</a></li>
                    </ul>
                </div>

                <div>
                    <h4>Kategori</h4>
                    <ul>
                        <li><a href=\"/nasional\">Nasional</a></li>
                        <li><a href=\"/daerah\">Daerah</a></li>
                        <li><a href=\"/internasional\">Internasional</a></li>
                        <li><a href=\"/budaya\">Budaya</a></li>
                        <li><a href=\"/ramadhan\">Ramadhan</a></li>
                    </ul>
                </div>

                <div>
                    <h4>Kontak</h4>
                    <ul>
                        <li>Email: <a href=\"mailto:{EMAIL}\">{EMAIL}</a></li>
                        <li>WhatsApp: <a href=\"{WHATSAPP}\" target=\"_blank\" rel=\"noreferrer\">{PHONE}</a></li>
                        <li>Alamat: {ADDRESS}</li>
                    </ul>
                </div>
            </div>

            <div class=\"footer-bottom\">
                <span>© <span data-current-year>2026</span> {SITE_NAME}. All rights reserved.</span>
                <span><a href=\"/privacy\">Privacy</a> · <a href=\"/terms\">Terms</a> · <a href=\"/contact\">Kontak</a></span>
            </div>
        </div>
    </footer>
    <script src=\"/js/app.js\" defer></script>
    """


def slugify(value):
    value = value.lower()
    value = value.replace("&", "")
    value = value.replace("(", "")
    value = value.replace(")", "")
    value = value.replace(" ", "-")
    return value


def render_article_card(article):
    return f"""
    <article class=\"article-card\">
        <img src=\"{article['image']}\" alt=\"{article['title']}\">
        <div class=\"article-card-body\">
            <div class=\"meta-row\">
                <span class=\"pill\">{article['category']}</span>
                <span>{article['date']}</span>
                <span>{article['read_time']}</span>
            </div>
            <h3>{article['title']}</h3>
            <p>{article['excerpt']}</p>
            <a href=\"/articles/{article['slug']}.html\">Baca selengkapnya →</a>
        </div>
    </article>
    """


def render_popular_item(article):
    return f"""
    <div class=\"mini-post\">
        <img src=\"{article['image']}\" alt=\"{article['title']}\">
        <div>
            <h4>{article['title']}</h4>
            <span>{article['date']}</span>
        </div>
    </div>
    """


def build_homepage():
    cards = "".join(render_article_card(a) for a in ARTICLES)
    popular = "".join(render_popular_item(a) for a in ARTICLES[:3])
    tags = "".join(f'<span class="tag">{tag}</span>' for tag in ["Ramadan", "Akhlak", "Al-Qur'an", "Seni", "Jumat", "Zakat"])
    tool_links = "".join(f'<li><a href="/tools/{slugify(tool)}.html">{tool}</a></li>' for tool in TOOLS_LIST)

    return f"""{get_meta_tags(f\"{SITE_NAME} - Warta, Kajian, dan Tools Islami\", SITE_DESC, \"/\")}
{header_html()}
<section class=\"hero\">
    <div class=\"container hero-inner\">
        <div>
            <div class=\"hero-badge\">Media Islam Terpadu</div>
            <h1>Warta, kajian, dan inspirasi islami untuk kehidupan modern.</h1>
            <p>{SITE_DESC}</p>
            <div class=\"cta-row\">
                <a href=\"/articles\" class=\"btn btn-primary\">Baca Artikel</a>
                <a href=\"/tools\" class=\"btn btn-secondary\">Lihat Tools</a>
            </div>
        </div>
        <div class=\"hero-card\">
            <img src=\"{ARTICLES[0]['image']}\" alt=\"{ARTICLES[0]['title']}\">
        </div>
    </div>
</section>

<main class=\"container\">
    <div class=\"main-layout\">
        <section class=\"content-section\">
            <div>
                <div class=\"section-header\">
                    <h2>Artikel Terbaru</h2>
                    <a href=\"/articles\" class=\"more-link\">Lihat semua →</a>
                </div>
                <div class=\"card-grid\">
                    {cards}
                </div>
            </div>

            <div>
                <div class=\"section-header\">
                    <h2>Artikel Terkait</h2>
                    <a href=\"/articles\" class=\"more-link\">Semua artikel →</a>
                </div>
                <div class=\"card-grid\">
                    {cards}
                </div>
            </div>
        </section>

        <aside class=\"sidebar\">
            <div class=\"panel\">
                <h3>Popular Post</h3>
                <div class=\"popular-list\">
                    {popular}
                </div>
            </div>

            <div class=\"panel\">
                <h3>Kategori</h3>
                <ul class=\"list-links\">
                    <li><a href=\"/nasional\">Nasional</a></li>
                    <li><a href=\"/daerah\">Daerah</a></li>
                    <li><a href=\"/internasional\">Internasional</a></li>
                    <li><a href=\"/risalah\">Risalah</a></li>
                    <li><a href=\"/redaksi\">Redaksi</a></li>
                    <li><a href=\"/tokoh\">Tokoh</a></li>
                </ul>
            </div>

            <div class=\"panel\">
                <h3>Label</h3>
                <div class=\"tag-list\">
                    {tags}
                </div>
            </div>

            <div class=\"panel\">
                <h3>Tools Islami</h3>
                <ul class=\"list-links\">
                    {tool_links}
                </ul>
            </div>
        </aside>
    </div>
</main>

{footer_html()}
</body>
</html>
"""


def build_article_page(article):
    return f"""{get_meta_tags(article['title'], article['excerpt'], f\"/articles/{article['slug']}.html\")}
{header_html()}
<main class=\"container\" style=\"padding:40px 0 60px;\">
    <div class=\"main-layout\">
        <article class=\"content-section\">
            <div class=\"panel\">
                <img src=\"{article['image']}\" alt=\"{article['title']}\" style=\"width:100%; height:420px; object-fit:cover;\">
                <div style=\"padding:22px;\">
                    <div class=\"meta-row\">
                        <span class=\"pill\">{article['category']}</span>
                        <span>{article['date']}</span>
                        <span>{article['read_time']}</span>
                    </div>
                    <h1 style=\"font-size: clamp(2rem, 3vw, 2.8rem); margin: 10px 0 18px;\">{article['title']}</h1>
                    <p>{article['excerpt']}</p>
                    <div style=\"font-size:1rem; line-height:1.9; color:#33463f;\">
                        <p>Setiap manusia membutuhkan ruang untuk menenangkan hati dan memperbaiki diri. Dalam konteks Islam, rutinitas ibadah, refleksi, dan akhlak yang baik menjadi pilar utama dalam membangun kehidupan yang lebih bermakna.</p>
                        <p>Islam mengajarkan agar setiap tindakan dilakukan dengan niat yang lurus dan tujuan yang jelas. Kesadaran spiritual yang dibangun secara konsisten akan membentuk karakter yang lebih baik dan lebih tenang.</p>
                        <p>Dengan menjaga kebersihan hati, memperbanyak dzikir, dan menghormati sesama, kita dapat meraih kehidupan yang lebih seimbang, lebih damai, dan lebih bermanfaat.</p>
                    </div>
                </div>
            </div>
        </article>

        <aside class=\"sidebar\">
            <div class=\"panel\">
                <h3>Popular Post</h3>
                <div class=\"popular-list\">
                    {''.join(render_popular_item(a) for a in ARTICLES[:3])}
                </div>
            </div>

            <div class=\"panel\">
                <h3>Bagikan</h3>
                <div class=\"share-box\">
                    <a href=\"https://facebook.com/sharer/sharer.php?u={DOMAIN}/articles/{article['slug']}.html\" target=\"_blank\" rel=\"noreferrer\">Facebook</a>
                    <a href=\"https://twitter.com/intent/tweet?url={DOMAIN}/articles/{article['slug']}.html\" target=\"_blank\" rel=\"noreferrer\">Twitter</a>
                    <a href=\"https://wa.me/?text={DOMAIN}/articles/{article['slug']}.html\" target=\"_blank\" rel=\"noreferrer\">WhatsApp</a>
                </div>
            </div>
        </aside>
    </div>
</main>

{footer_html()}
</body>
</html>
"""


def build_tools_page(title, description, script_name=""):
    scripts = f'<script src="/js/{script_name}" defer></script>' if script_name else ""
    return f"""{get_meta_tags(title, description, \"/tools\")}
{header_html()}
<main class=\"container\" style=\"padding:40px 0 60px;\">
    <div class=\"panel\">
        <h1>{title}</h1>
        <p>{description}</p>
        {render_tool_content(title, script_name)}
    </div>
</main>
{footer_html()}
{scripts}
</body>
</html>
"""


def render_tool_content(title, script_name):
    if title == "Al-Qur'an":
        return """
        <div id=\"quran-app\">
            <input id=\"quran-search\" type=\"text\" placeholder=\"Cari surah...\" style=\"width:100%; padding:12px 14px; border:1px solid #dfe7e1; border-radius:10px; margin-bottom:12px;\">
            <div id=\"selected-surah-title\" style=\"font-weight:700; margin-bottom:10px;\"></div>
            <div id=\"surah-list\" class=\"tool-grid\"></div>
            <div id=\"verse-output\" style=\"margin-top: 20px;\"></div>
        </div>
        """
    if title == "Jadwal Sholat":
        return """
        <div id=\"prayer-app\">
            <select id=\"city-select\" style=\"width:100%; padding:12px 14px; border:1px solid #dfe7e1; border-radius:10px; margin-bottom:12px;\"></select>
            <div id=\"prayer-results\"></div>
        </div>
        """
    if title == "Kalender Hijriyah":
        return """
        <div id=\"hijri-app\">
            <label for=\"hijri-month\">Bulan</label>
            <select id=\"hijri-month\" style=\"width:100%; padding:12px 14px; border:1px solid #dfe7e1; border-radius:10px; margin-bottom:12px;\"></select>
            <label for=\"hijri-year\">Tahun</label>
            <input id=\"hijri-year\" type=\"number\" value=\"1446\" style=\"width:100%; padding:12px 14px; border:1px solid #dfe7e1; border-radius:10px; margin-bottom:12px;\">
            <label for=\"hijri-city\">Kota</label>
            <select id=\"hijri-city\" style=\"width:100%; padding:12px 14px; border:1px solid #dfe7e1; border-radius:10px; margin-bottom:12px;\"></select>
            <div id=\"hijri-output\"></div>
        </div>
        """
    if title == "Kalkulator Zakat":
        return """
        <div id=\"zakat-app\">
            <form id=\"zakat-form\" class=\"form-box\">
                <label for=\"income\">Penghasilan</label>
                <input id=\"income\" type=\"number\" value=\"0\">
                <label for=\"savings\">Tabungan</label>
                <input id=\"savings\" type=\"number\" value=\"0\">
                <label for=\"gold\">Emas / Perhiasan</label>
                <input id=\"gold\" type=\"number\" value=\"0\">
                <label for=\"debt\">Utang</label>
                <input id=\"debt\" type=\"number\" value=\"0\">
                <label for=\"family\">Kewajiban Keluarga</label>
                <input id=\"family\" type=\"number\" value=\"0\">
                <button type=\"submit\">Hitung Zakat</button>
            </form>
            <div id=\"zakat-result\"></div>
        </div>
        """
    return """
    <div class=\"tool-card\">
        <h3>Tool ini sedang dikembangkan</h3>
        <p>Versi lengkap untuk tools ini akan ditambahkan di tahap berikutnya.</p>
    </div>
    """


def generate_pages():
    Path("index.html").write_text(build_homepage(), encoding="utf-8")

    articles_dir = Path("articles")
    articles_dir.mkdir(exist_ok=True)
    for article in ARTICLES:
        Path(articles_dir / f"{article['slug']}.html").write_text(build_article_page(article), encoding="utf-8")

    for category in ["warta", "nasional", "daerah", "internasional", "risalah", "redaksi", "obituari", "tokoh", "hikmah", "kesehatan", "cerpen", "puisi", "pidato", "khutbah", "seni", "budaya", "ramadhan", "pustaka", "humor"]:
        folder = Path(category)
        folder.mkdir(exist_ok=True)
        page = folder / "index.html"
        page.write_text(
            f"""{get_meta_tags(f\"{category.title()} - {SITE_NAME}\", f\"{category.title()} {SITE_NAME}\", f\"/{category}/\")}
{header_html()}
<main class=\"container\" style=\"padding:40px 0 60px;\">
    <div class=\"panel\">
        <h1>{category.title()}</h1>
        <p>Halaman {category.title()} sedang dikembangkan.</p>
    </div>
</main>
{footer_html()}
</body></html>""",
            encoding="utf-8"
        )

    tools_dir = Path("tools")
    tools_dir.mkdir(exist_ok=True)
    tool_map = {
        "Al-Qur'an": ("Al-Qur'an", "Akses surah dan ayat Al-Qur'an dalam format sederhana.", "quran.js"),
        "Jadwal Sholat": ("Jadwal Sholat", "Jadwal sholat berdasarkan kota pilihan Anda.", "prayer.js"),
        "Kalender Hijriyah": ("Kalender Hijriyah", "Lihat kalender Hijriah dan tanggal umum.", "hijri.js"),
        "Kalkulator Zakat": ("Kalkulator Zakat", "Hitung zakat berdasarkan penghasilan, tabungan, emas, dan kewajiban.", "zakat.js"),
    }

    for tool_name, (title, desc, script_name) in tool_map.items():
        slug = slugify(tool_name)
        tool_path = tools_dir / f"{slug}.html"
        tool_path.write_text(build_tools_page(title, desc, script_name), encoding="utf-8")

    for tool_name in TOOLS_LIST:
        slug = slugify(tool_name)
        tool_path = tools_dir / f"{slug}.html"
        if not tool_path.exists():
            tool_path.write_text(build_tools_page(tool_name, f"Halaman {tool_name} untuk {SITE_NAME}.", ""), encoding="utf-8")

    contact_dir = Path("contact")
    contact_dir.mkdir(exist_ok=True)
    Path(contact_dir / "index.html").write_text(
        f"""{get_meta_tags("Kontak - ALHIKMAH", "Kontak ALHIKMAH untuk kerja sama dan pertanyaan.", "/contact/")}
{header_html()}
<main class=\"container\" style=\"padding:40px 0 60px;\">
    <div class=\"panel\">
        <h1>Kontak</h1>
        <p>Email: <a href=\"mailto:{EMAIL}\">{EMAIL}</a></p>
        <p>WhatsApp: <a href=\"{WHATSAPP}\" target=\"_blank\" rel=\"noreferrer\">{PHONE}</a></p>
        <p>Alamat: {ADDRESS}</p>
        <ul>
            {''.join(f'<li><a href="{url}" target="_blank" rel="noreferrer">{name}</a></li>' for name, url in SOCIAL_LINKS)}
        </ul>
    </div>
</main>
{footer_html()}
</body></html>""",
        encoding="utf-8"
    )

    about_dir = Path("about")
    about_dir.mkdir(exist_ok=True)
    Path(about_dir / "index.html").write_text(
        f"""{get_meta_tags("About - ALHIKMAH", "Tentang ALHIKMAH", "/about/")}
{header_html()}
<main class=\"container\" style=\"padding:40px 0 60px;\">
    <div class=\"panel\">
        <h1>Tentang ALHIKMAH</h1>
        <p>ALHIKMAH adalah platform ulama, kajian, media, dan tools Islami yang dibuat untuk membantu umat dalam mempelajari Islam secara praktis dan bermanfaat.</p>
    </div>
</main>
{footer_html()}
</body></html>""",
        encoding="utf-8"
    )

    archive_dir = Path("archive")
    archive_dir.mkdir(exist_ok=True)
    for year in [2023, 2024, 2025, 2026]:
        page = archive_dir / f"{year}.html"
        page.write_text(
            f"""{get_meta_tags(f\"Arsip {year} - {SITE_NAME}\", f\"Arsip {year} {SITE_NAME}\", f\"/archive/{year}.html\")}
{header_html()}
<main class=\"container\" style=\"padding:40px 0 60px;\">
    <div class=\"panel\">
        <h1>Arsip {year}</h1>
        <ul>
            {''.join(f'<li><a href="/articles/{a["slug"]}.html">{a["title"]}</a></li>' for a in ARTICLES if a["year"] == year)}
        </ul>
    </div>
</main>
{footer_html()}
</body></html>""",
            encoding="utf-8"
        )

    Path("404.html").write_text(
        f"""{get_meta_tags("404 - Not Found", "Halaman tidak ditemukan.", "/404.html")}
{header_html()}
<main class=\"container\" style=\"padding:40px 0 60px;\">
    <div class=\"panel\">
        <h1>404 - Tidak Ditemukan</h1>
        <p>Halaman yang Anda cari tidak tersedia. Kembali ke <a href=\"/\">Beranda</a>.</p>
    </div>
</main>
{footer_html()}
</body></html>""",
        encoding="utf-8"
    )

    Path("manifest.json").write_text(json.dumps({
        "name": SITE_NAME,
        "short_name": SITE_NAME,
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": THEME_COLOR,
        "icons": [{"src": LOGO_URL, "sizes": "200x200", "type": "image/jpeg"}]
    }, indent=4), encoding="utf-8")

    Path("robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://alhikmah.my.id/sitemap.xml", encoding="utf-8")
    Path("sitemap.xml").write_text(
        """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <url><loc>https://alhikmah.my.id/</loc><lastmod>2026-11-01</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>
</urlset>""",
        encoding="utf-8"
    )
    Path("rss.xml").write_text(
        f"""<?xml version=\"1.0\" encoding=\"UTF-8\" ?>
<rss version=\"2.0\">
<channel>
    <title>{SITE_NAME}</title>
    <link>{DOMAIN}</link>
    <description>{SITE_DESC}</description>
    <language>id-id</language>
    {''.join(f'<item><title>{a["title"]}</title><link>{DOMAIN}/articles/{a["slug"]}.html</link><description>{a["excerpt"]}</description></item>' for a in ARTICLES)}
</channel>
</rss>""",
        encoding="utf-8"
    )
    Path("atom.xml").write_text(
        f"""<?xml version=\"1.0\" encoding=\"utf-8\"?>
<feed xmlns=\"http://www.w3.org/2005/Atom\">
  <title>{SITE_NAME}</title>
  <link href=\"{DOMAIN}/atom.xml\" rel=\"self\" />
  <link href=\"{DOMAIN}\" />
  <updated>{datetime.datetime.now().isoformat()}</updated>
  <id>{DOMAIN}/</id>
  {''.join(f'<entry><title>{a["title"]}</title><link href="{DOMAIN}/articles/{a["slug"]}.html" /><id>{DOMAIN}/articles/{a["slug"]}.html</id><summary>{a["excerpt"]}</summary></entry>' for a in ARTICLES)}
</feed>""",
        encoding="utf-8"
    )
    Path("ads.txt").write_text(f"google.com, {GA_PUB_ID}, DIRECT, f08c47fec0942fa0", encoding="utf-8")
    Path("app-ads.txt").write_text(f"google.com, {GA_PUB_ID}, DIRECT, f08c47fec0942fa0", encoding="utf-8")
    Path("README.md").write_text("# ALHIKMAH\n\nPortal Islami dengan blog dan tools Islami.\n", encoding="utf-8")
    Path("LICENSE").write_text("MIT License\n\nCopyright (c) 2026 Alhikmah", encoding="utf-8")


if __name__ == "__main__":
    prepare_assets()
    generate_pages()
    print("ALHIKMAH static portal created successfully.")
