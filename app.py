from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ganti-secret-key-portal-dosen")

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "portal_data.json"
UPLOAD_ROOT = BASE_DIR / "uploads"

# Ganti password ini melalui environment variable ADMIN_PASSWORD bila web dipublikasikan.
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "PrismaGeologi2026")

ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx",
    "zip", "rar", "txt", "jpg", "jpeg", "png"
}

PROFILE = {
    "name": "Drs. Agus Santoso Budiharso, B.Sc., M.Sc.",
    "role": "Dosen Teknik Geologi",
    "role_en": "Lecturer in Geological Engineering",
    "university": "Universitas Prisma Manado",
    "email": "agus.budiharso@prisma.ac.id",
    "siakad": "https://siap.prisma.ac.id/",
    "tagline": "Geologi • GIS • Penginderaan Jauh • Pendidikan • Penelitian • Pengabdian",
    "tagline_en": "Geology • GIS • Remote Sensing • Education • Research • Community Service"
}

COURSES = [
    {
        "slug": "sig",
        "name": "Sistem Informasi Geografis (SIG)",
        "name_en": "Geographic Information Systems (GIS)",
        "icon": "🗺️",
        "desc": "Konsep dan penerapan GIS untuk pengelolaan, analisis, visualisasi, dan interpretasi data geologi.",
        "desc_en": "Concepts and applications of GIS for managing, analyzing, visualizing, and interpreting geological data."
    },
    {
        "slug": "geomorfologi",
        "name": "Geomorfologi",
        "name_en": "Geomorphology",
        "icon": "⛰️",
        "desc": "Kajian bentuklahan, proses geomorfik, morfometri, dan interpretasi bentang alam untuk kebutuhan geologi.",
        "desc_en": "Study of landforms, geomorphic processes, morphometry, and landscape interpretation for geological applications."
    },
    {
        "slug": "manajemen-proyek",
        "name": "Manajemen Proyek",
        "name_en": "Project Management",
        "icon": "📊",
        "desc": "Perencanaan, pelaksanaan, pengendalian, evaluasi, biaya, mutu, waktu, dan risiko proyek.",
        "desc_en": "Project planning, implementation, control, evaluation, cost, quality, schedule, and risk management."
    },
    {
        "slug": "geologi-indonesia",
        "name": "Geologi Indonesia",
        "name_en": "Geology of Indonesia",
        "icon": "🌋",
        "desc": "Tektonik, stratigrafi, vulkanisme, sumber daya geologi, dan evolusi geologi wilayah Indonesia.",
        "desc_en": "Tectonics, stratigraphy, volcanism, geological resources, and the geological evolution of Indonesia."
    },
    {
        "slug": "metode-penelitian-geologi",
        "name": "Metode Penelitian Geologi",
        "name_en": "Geological Research Methods",
        "icon": "🔬",
        "desc": "Penyusunan masalah, desain penelitian, pengumpulan data, analisis, interpretasi, dan penulisan ilmiah.",
        "desc_en": "Problem formulation, research design, data collection, analysis, interpretation, and scientific writing."
    },
    {
        "slug": "penginderaan-jauh",
        "name": "Penginderaan Jauh",
        "name_en": "Remote Sensing",
        "icon": "🛰️",
        "desc": "Pemanfaatan citra satelit, DEM, analisis spektral, dan interpretasi data penginderaan jauh untuk geologi.",
        "desc_en": "Use of satellite imagery, DEMs, spectral analysis, and remote-sensing data interpretation for geology."
    }
]

TRIDHARMA = [
    {"title": "Pendidikan & Pengajaran", "icon": "🎓",
     "desc": "Pembelajaran, RPS, bahan ajar, praktikum, evaluasi dan pengembangan materi kuliah."},
    {"title": "Penelitian", "icon": "🔎",
     "desc": "Kajian geologi, geomorfologi, kebencanaan, geospasial, penginderaan jauh, dan GeoAI."},
    {"title": "Pengabdian Masyarakat", "icon": "🤝",
     "desc": "Penerapan pengetahuan geologi dan geospasial untuk masyarakat, mitigasi bencana dan sumber daya."},
    {"title": "Kegiatan Penunjang", "icon": "🏅",
     "desc": "Seminar, pelatihan, organisasi profesi, kepanitiaan, publikasi, buku dan kegiatan akademik lain."}
]


TRIDHARMA_EN = [
    {"title": "Education & Teaching", "icon": "🎓", "desc": "Courses, semester learning plans, teaching materials, practical work, assessment, and curriculum development."},
    {"title": "Research", "icon": "🔎", "desc": "Research in geology, geomorphology, disasters, geospatial science, remote sensing, and GeoAI."},
    {"title": "Community Service", "icon": "🤝", "desc": "Application of geological and geospatial knowledge for communities, disaster risk reduction, and natural resources."},
    {"title": "Academic & Professional Activities", "icon": "🏅", "desc": "Seminars, training, professional organizations, committees, publications, books, and other academic activities."}
]

def current_lang():
    lang = request.args.get("lang") or session.get("lang", "id")
    return "en" if lang == "en" else "id"


def localized_courses(lang):
    if lang != "en":
        return COURSES
    return [dict(c, name=c.get("name_en", c["name"]), desc=c.get("desc_en", c["desc"])) for c in COURSES]


def default_data():
    return {
        "courses": {
            c["slug"]: {"rps": [], "materials": []}
            for c in COURSES
        },
        "writings": []
    }


def load_data():
    if not DATA_FILE.exists():
        data = default_data()
        save_data(data)
        return data
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = default_data()

    # Menjamin semua mata kuliah tersedia meski data lama digunakan
    data.setdefault("courses", {})
    for c in COURSES:
        data["courses"].setdefault(c["slug"], {"rps": [], "materials": []})
    data.setdefault("writings", [])
    return data


def save_data(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def course_by_slug(slug):
    return next((c for c in COURSES if c["slug"] == slug), None)


def is_admin():
    return session.get("admin") is True


def save_uploaded_file(file_obj, category, prefix=""):
    filename = secure_filename(file_obj.filename)
    if not filename:
        raise ValueError("Nama file tidak valid.")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stored_name = f"{prefix}_{timestamp}_{filename}" if prefix else f"{timestamp}_{filename}"
    target_dir = UPLOAD_ROOT / category
    target_dir.mkdir(parents=True, exist_ok=True)
    file_obj.save(target_dir / stored_name)
    return stored_name


@app.context_processor
def inject_globals():
    lang = current_lang()
    localized_profile = dict(PROFILE)
    if lang == "en":
        localized_profile["role"] = PROFILE["role_en"]
        localized_profile["tagline"] = PROFILE["tagline_en"]
    return {
        "profile": localized_profile,
        "admin_logged_in": is_admin(),
        "lang": lang
    }



@app.route("/language/<lang>")
def set_language(lang):
    session["lang"] = "en" if lang == "en" else "id"
    target = request.args.get("next") or request.referrer or url_for("home")
    return redirect(target)

@app.route("/")
def home():
    data = load_data()
    latest_writings = list(reversed(data["writings"]))[:3]
    return render_template(
        "index.html",
        courses=localized_courses(current_lang()),
        tridharma=TRIDHARMA_EN if current_lang() == "en" else TRIDHARMA,
        latest_writings=latest_writings
    )


@app.route("/mata-kuliah/<slug>")
def course_detail(slug):
    course = course_by_slug(slug)
    if course and current_lang() == "en":
        course = dict(course, name=course.get("name_en", course["name"]), desc=course.get("desc_en", course["desc"]))
    if not course:
        return "Mata kuliah tidak ditemukan", 404
    data = load_data()
    course_files = data["courses"][slug]
    return render_template(
        "course.html",
        course=course,
        rps_files=list(reversed(course_files["rps"])),
        materials=list(reversed(course_files["materials"]))
    )


@app.route("/tulisan")
def writings():
    data = load_data()
    return render_template(
        "writings.html",
        writings=list(reversed(data["writings"]))
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["admin"] = True
            flash("Login admin berhasil.", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("home"))
        flash("Password admin salah.", "error")
    return render_template("login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Anda telah keluar dari mode admin.", "success")
    return redirect(url_for("home"))


@app.route("/admin/upload/rps/<slug>", methods=["POST"])
def upload_rps(slug):
    if not is_admin():
        return redirect(url_for("admin_login", next=url_for("course_detail", slug=slug)))
    course = course_by_slug(slug)
    if not course:
        return "Mata kuliah tidak ditemukan", 404

    file_obj = request.files.get("file")
    title = request.form.get("title", "").strip()
    semester = request.form.get("semester", "").strip()

    if not file_obj or not file_obj.filename:
        flash("Pilih file RPS terlebih dahulu.", "error")
        return redirect(url_for("course_detail", slug=slug))
    if not allowed_file(file_obj.filename):
        flash("Format file tidak diperbolehkan.", "error")
        return redirect(url_for("course_detail", slug=slug))

    stored_name = save_uploaded_file(file_obj, "rps", slug)
    data = load_data()
    data["courses"][slug]["rps"].append({
        "title": title or "Rencana Pembelajaran Semester (RPS)",
        "semester": semester,
        "original_name": file_obj.filename,
        "stored_name": stored_name,
        "uploaded_at": datetime.now().strftime("%d-%m-%Y %H:%M")
    })
    save_data(data)
    flash("RPS berhasil diunggah.", "success")
    return redirect(url_for("course_detail", slug=slug))


@app.route("/admin/upload/material/<slug>", methods=["POST"])
def upload_material(slug):
    if not is_admin():
        return redirect(url_for("admin_login", next=url_for("course_detail", slug=slug)))
    course = course_by_slug(slug)
    if not course:
        return "Mata kuliah tidak ditemukan", 404

    file_obj = request.files.get("file")
    title = request.form.get("title", "").strip()
    meeting = request.form.get("meeting", "").strip()
    description = request.form.get("description", "").strip()

    if not file_obj or not file_obj.filename:
        flash("Pilih file bahan ajar terlebih dahulu.", "error")
        return redirect(url_for("course_detail", slug=slug))
    if not allowed_file(file_obj.filename):
        flash("Format file tidak diperbolehkan.", "error")
        return redirect(url_for("course_detail", slug=slug))

    stored_name = save_uploaded_file(file_obj, "materials", slug)
    data = load_data()
    data["courses"][slug]["materials"].append({
        "title": title or file_obj.filename,
        "meeting": meeting,
        "description": description,
        "original_name": file_obj.filename,
        "stored_name": stored_name,
        "uploaded_at": datetime.now().strftime("%d-%m-%Y %H:%M")
    })
    save_data(data)
    flash("Bahan ajar berhasil diunggah.", "success")
    return redirect(url_for("course_detail", slug=slug))


@app.route("/admin/upload/writing", methods=["POST"])
def upload_writing():
    if not is_admin():
        return redirect(url_for("admin_login", next=url_for("writings")))

    file_obj = request.files.get("file")
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    year = request.form.get("year", "").strip()
    description = request.form.get("description", "").strip()

    if not file_obj or not file_obj.filename:
        flash("Pilih file tulisan terlebih dahulu.", "error")
        return redirect(url_for("writings"))
    if not allowed_file(file_obj.filename):
        flash("Format file tidak diperbolehkan.", "error")
        return redirect(url_for("writings"))

    stored_name = save_uploaded_file(file_obj, "writings", "tulisan")
    data = load_data()
    data["writings"].append({
        "title": title or file_obj.filename,
        "category": category or "Tulisan",
        "year": year,
        "description": description,
        "original_name": file_obj.filename,
        "stored_name": stored_name,
        "uploaded_at": datetime.now().strftime("%d-%m-%Y %H:%M")
    })
    save_data(data)
    flash("Tulisan berhasil diunggah.", "success")
    return redirect(url_for("writings"))


@app.route("/download/<category>/<filename>")
def download_file(category, filename):
    if category not in {"rps", "materials", "writings"}:
        return "Kategori tidak valid", 404
    directory = UPLOAD_ROOT / category
    return send_from_directory(directory, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)