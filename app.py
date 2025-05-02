# app.py
from flask import Flask, render_template, abort, url_for
from werkzeug.utils import safe_join
from datetime import datetime
import re
import os

app = Flask(__name__)
CONTENT_DIR = os.path.join(app.root_path, 'content')

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text) # Remove non-alphanumeric characters except space/hyphen
    text = re.sub(r'[\s-]+', '-', text).strip('-') # Replace spaces/multiple hyphens with single hyphen
    return text if text else "subtopic" # Basic fallback

# --- Data for Grade 3 Topics (Bahasa Indonesia) ---
grade_3_topics = [
    {
        "topic": "Bilangan Cacah", "slug": "bilangan-cacah", "icon": "fa-calculator",
        "subtopics": [
            {"name": "Bilangan hingga 10.000", "slug": slugify("Bilangan hingga 10000")},
            {"name": "Angka ke Kata hingga 10.000", "slug": slugify("Angka ke Kata hingga 10000")},
            {"name": "Kata ke Angka hingga 10.000", "slug": slugify("Kata ke Angka hingga 10000")},
            {"name": "Pola Bilangan", "slug": slugify("Pola Bilangan")},
            {"name": "Membandingkan dan Mengurutkan", "slug": slugify("Membandingkan dan Mengurutkan")},
            {"name": "Penjumlahan", "slug": slugify("Penjumlahan Bilangan")}, # Added context for uniqueness
            {"name": "Pengurangan", "slug": slugify("Pengurangan Bilangan")}, # Added context
            {"name": "Tabel Perkalian 6, 7, 8, dan 9", "slug": slugify("Tabel Perkalian 6 7 8 9")},
            {"name": "Perkalian", "slug": slugify("Perkalian Bilangan")}, # Added context
            {"name": "Pembagian", "slug": slugify("Pembagian Bilangan")}, # Added context
            {"name": "Soal Cerita 2 Langkah (Penjumlahan, Pengurangan, Perkalian, Pembagian)", "slug": slugify("Soal Cerita 2 Langkah Bilangan")}
        ]
    },
    {
        "topic": "Uang", "slug": "uang", "icon": "fa-coins",
        "subtopics": [
            {"name": "Penjumlahan", "slug": slugify("Penjumlahan Uang")}, # Unique slug
            {"name": "Pengurangan", "slug": slugify("Pengurangan Uang")}, # Unique slug
            {"name": "Soal Cerita", "slug": slugify("Soal Cerita Uang")}  # Unique slug
        ]
    },
    {
        "topic": "Waktu", "slug": "waktu", "icon": "fa-clock",
        "subtopics": [
            {"name": "Menyatakan Waktu", "slug": slugify("Menyatakan Waktu")},
            {"name": "Konversi Waktu (Jam dan Menit)", "slug": slugify("Konversi Waktu Jam Menit")},
            {"name": "Penjumlahan (Waktu)", "slug": slugify("Penjumlahan Waktu")},
            {"name": "Pengurangan (Waktu)", "slug": slugify("Pengurangan Waktu")},
            {"name": "Mencari Durasi, Waktu Mulai dan Selesai", "slug": slugify("Mencari Durasi Waktu")},
            {"name": "Soal Cerita (Waktu)", "slug": slugify("Soal Cerita Waktu")}
        ]
    },
    {
        "topic": "Panjang, Massa, Volume", "slug": "panjang-massa-volume", "icon": "fa-ruler-combined",
        "subtopics": [
            {"name": "Meter dan Sentimeter", "slug": slugify("Meter dan Sentimeter")},
            {"name": "Kilometer dan Meter", "slug": slugify("Kilometer dan Meter")},
            {"name": "Kilogram dan Gram", "slug": slugify("Kilogram dan Gram")},
            {"name": "Liter dan Mililiter", "slug": slugify("Liter dan Mililiter")},
            {"name": "Soal Cerita 1 Langkah", "slug": slugify("Soal Cerita 1 Langkah Ukuran")}, # Unique slug
            {"name": "Soal Cerita 2 Langkah", "slug": slugify("Soal Cerita 2 Langkah Ukuran")}  # Unique slug
        ]
    },
    {
        "topic": "Pecahan", "slug": "pecahan", "icon": "fa-chart-pie",
        "subtopics": [
            {"name": "Apa itu Pecahan?", "slug": slugify("Apa itu Pecahan")},
            {"name": "Pecahan Senilai", "slug": slugify("Pecahan Senilai")},
            {"name": "Menyederhanakan Pecahan", "slug": slugify("Menyederhanakan Pecahan")},
            {"name": "Membandingkan dan Mengurutkan Pecahan", "slug": slugify("Membandingkan Mengurutkan Pecahan")},
            {"name": "Menjumlahkan Pecahan", "slug": slugify("Menjumlahkan Pecahan")},
            {"name": "Mengurangkan Pecahan", "slug": slugify("Mengurangkan Pecahan")}
        ]
    },
    {
        "topic": "Luas dan Keliling", "slug": "luas-dan-keliling", "icon": "fa-vector-square",
        "subtopics": [
            {"name": "Satuan Persegi", "slug": slugify("Satuan Persegi")},
            {"name": "Sentimeter Persegi (cm²) dan Meter Persegi (m²)", "slug": slugify("Sentimeter Meter Persegi")}, # Simpler slug
            {"name": "Luas Persegi dan Persegi Panjang", "slug": slugify("Luas Persegi Persegi Panjang")},
            {"name": "Keliling Persegi dan Persegi Panjang", "slug": slugify("Keliling Persegi Persegi Panjang")},
            {"name": "Soal Cerita (Luas dan Keliling)", "slug": slugify("Soal Cerita Luas Keliling")}
        ]
    },
    {
        "topic": "Sudut", "slug": "sudut", "icon": "fa-drafting-compass",
        "subtopics": [
            {"name": "Mengidentifikasi Sudut pada Bangun", "slug": slugify("Mengidentifikasi Sudut")},
            {"name": "Sudut Siku-siku", "slug": slugify("Sudut Siku siku")}
        ]
    },
    {
        "topic": "Diagram Batang", "slug": "diagram-batang", "icon": "fa-chart-bar",
        "subtopics": [
            {"name": "Membaca dan Menafsirkan Diagram Batang", "slug": slugify("Membaca Menafsirkan Diagram Batang")},
            {"name": "Soal Cerita (Diagram Batang) - (Akan datang)", "slug": "soal-cerita-diagram-batang"} # Manual slug for placeholder
        ]
    },
    {
        "topic": "Garis Tegak Lurus dan Sejajar", "slug": "garis-tegak-lurus-sejajar", "icon": "fa-grip-lines",
        "subtopics": [
            {"name": "Mengidentifikasi Garis Tegak Lurus", "slug": slugify("Mengidentifikasi Garis Tegak Lurus")},
            {"name": "Mengidentifikasi Garis Sejajar", "slug": slugify("Mengidentifikasi Garis Sejajar")},
            {"name": "Menggambar Garis Tegak Lurus dan Sejajar", "slug": slugify("Menggambar Garis Tegak Lurus Sejajar")}
        ]
    }
]
# --- End Grade 3 Data ---


@app.route('/')
def home():
    """Renders the homepage template."""
    current_year = datetime.now().year
    return render_template('index.html', current_year=current_year)

# --- New Route for Grade Learn Page ---
@app.route('/kelas/<int:grade_level>')
def learn_grade(grade_level):
    topics_data = None
    current_year = datetime.now().year
    if grade_level == 3:
        topics_data = grade_3_topics
        page_title = "Kelas 3"
    else:
        abort(404, description=f"Materi untuk Kelas {grade_level} belum tersedia.")

    return render_template('grade_learn.html',
                           grade_level_title=page_title, # Renamed for clarity
                           grade_level_num=grade_level, # Pass number too
                           topics=topics_data,
                           current_year=current_year)

@app.route('/kelas/<int:grade_level>/<topic_slug>/<subtopic_slug>')
def learn_subtopic(grade_level, topic_slug, subtopic_slug):
    """Renders the page for a specific subtopic by loading its content file."""
    current_year = datetime.now().year
    topic_info = None
    subtopic_info = None
    subtopic_content_html = "" # Initialize content variable
    content_loaded_successfully = False

    # --- Find Topic/Subtopic Info ---
    if grade_level == 3: # Assuming only Grade 3 exists for now
        for topic in grade_3_topics:
            if topic['slug'] == topic_slug:
                topic_info = topic
                for subtopic in topic['subtopics']:
                    if subtopic['slug'] == subtopic_slug:
                        subtopic_info = subtopic
                        break
                break

    if not topic_info or not subtopic_info:
         app.logger.warning(f"Topic/Subtopic not found for slugs: {topic_slug}/{subtopic_slug}")
         abort(404, description="Topik atau sub-topik tidak ditemukan.")
    # --- End Lookup ---

    # --- Load Content from Specific File ---
    try:
        # Construct the relative path for the content snippet file
        relative_path = os.path.join(f"grade-{grade_level}", topic_slug, f"{subtopic_slug}.html")
        # Securely join with the base content directory
        content_path = safe_join(CONTENT_DIR, relative_path)

        app.logger.info(f"Attempting to load content from: {content_path}") # Log path for debugging

        if os.path.exists(content_path) and os.path.isfile(content_path):
            with open(content_path, 'r', encoding='utf-8') as f:
                subtopic_content_html = f.read()
                content_loaded_successfully = True # Mark as success
                # Check if it's just placeholder content (simple check)
                if "konten untuk sub-topik ini akan segera hadir" in subtopic_content_html.lower():
                     content_loaded_successfully = False # Treat placeholder as not 'real' content yet
        else:
            app.logger.warning(f"Content file not found: {content_path}")
            # File doesn't exist, content remains empty, handled below

    except FileNotFoundError:
         app.logger.warning(f"FileNotFoundError for: {content_path}")
         # Handled below
    except Exception as e:
        app.logger.error(f"Error loading content file {content_path}: {e}")
        # Generic error message, could abort(500)
        subtopic_content_html = "<p class='text-danger'>Terjadi kesalahan saat memuat konten.</p>"
        content_loaded_successfully = False
    # --- End Load Content ---

    # --- Prepare Placeholder if Content Wasn't Loaded Successfully ---
    if not content_loaded_successfully:
        # Generate standard placeholder HTML
         subtopic_content_html = f"""
        <div class='placeholder-content-snippet text-center p-5 bg-light rounded border'>
            <i class='fas fa-pencil-alt fa-3x text-muted mb-3'></i>
            <p class='lead'>Konten untuk "{subtopic_info['name']}" akan segera hadir!</p>
            <p class='small text-muted'>(Konten belum tersedia)</p>
        </div>"""

    # --- Render the Generic Subtopic Template ---
    return render_template('subtopic_page.html',
                           grade_level_num=grade_level,
                           topic_name=topic_info['topic'],
                           subtopic_name=subtopic_info['name'],
                           # Pass the loaded HTML (or placeholder)
                           subtopic_content_html=subtopic_content_html,
                           current_year=current_year)


# This block allows running the app locally using `python app.py`
if __name__ == '__main__':
    # debug=True enables auto-reloading when code changes and provides detailed error pages.
    # host='0.0.0.0' makes the server accessible from other devices on your network (optional).
    # port=8080 is a common port for local development.
    app.run(host='0.0.0.0', port=8080, debug=True)