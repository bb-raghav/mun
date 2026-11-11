"""Lightweight Flask prototype for the RNSIT MUN website."""

from pathlib import Path
from datetime import datetime, timezone
from email.message import EmailMessage
from html import escape
import os
import re
import smtplib
import threading
import uuid

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "rnsit-mun-local-prototype"

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
EVENTS_DIR = BASE_DIR / "static" / "images" / "events"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
CONFERENCE_2026_URL = "https://mun-gold.vercel.app/"
CONFERENCE_2026_IMAGE = "IMG_6131.JPG"

COMMITTEES = [
    {
        "name": "United Nations Security Council",
        "short_name": "UNSC",
        "type": "United Nations",
        "description": "A forum for delegates to examine questions of international peace and security through negotiation and resolution writing.",
        "agenda": "Illustrative agenda: strengthening international cooperation in conflict prevention.",
        "overview": "The UNSC simulation introduces delegates to multilateral diplomacy, crisis response and the work of the United Nations Security Council.",
        "responsibilities": "Research your assigned country, speak from its policy perspective, negotiate with other delegates and contribute to draft resolutions.",
        "executive_board": "Executive Board details to be confirmed.",
        "study_guide": None,
        "symbol": "01",
    },
    {
        "name": "United Nations Human Rights Council",
        "short_name": "UNHRC",
        "type": "United Nations",
        "description": "A committee focused on human rights, international standards and constructive dialogue between states.",
        "agenda": "Illustrative agenda: advancing access to education in humanitarian emergencies.",
        "overview": "The UNHRC simulation invites delegates to consider human rights concerns through research, moderated debate and consensus building.",
        "responsibilities": "Represent your country, support claims with research, engage respectfully in debate and help develop practical recommendations.",
        "executive_board": "Executive Board details to be confirmed.",
        "study_guide": None,
        "symbol": "02",
    },
    {
        "name": "United Nations General Assembly",
        "short_name": "UNGA",
        "type": "United Nations",
        "description": "A broad multilateral forum where delegates discuss global challenges and work toward shared proposals.",
        "agenda": "Illustrative agenda: responsible international cooperation on climate resilience.",
        "overview": "The UNGA simulation gives delegates a platform to explore global issues and practice collaborative decision making.",
        "responsibilities": "Understand your country's position, participate in formal and informal debate, and collaborate on working papers and resolutions.",
        "executive_board": "Executive Board details to be confirmed.",
        "study_guide": None,
        "symbol": "03",
    },
    {
        "name": "All India Political Parties Meet",
        "short_name": "AIPPM",
        "type": "Indian parliamentary simulation",
        "description": "A political simulation for examining public policy, parliamentary procedure and competing viewpoints.",
        "agenda": "Illustrative agenda: evaluating pathways for inclusive digital access.",
        "overview": "The AIPPM simulation introduces delegates to parliamentary discussion and policy debate in an Indian political context.",
        "responsibilities": "Research the assigned role and party perspective, make clear arguments, follow the committee procedure and negotiate policy proposals.",
        "executive_board": "Executive Board details to be confirmed.",
        "study_guide": None,
        "symbol": "04",
    },
]

RESOURCES = [
    {
        "title": "Rules of Procedure",
        "category": "Conference Essentials",
        "description": "A guide to motions, points and the flow of committee debate.",
        "file": None,
    },
    {
        "title": "Position Paper Guidelines",
        "category": "Writing Guides",
        "description": "A starting point for structuring a country policy paper.",
        "file": None,
    },
    {
        "title": "Research Guide for Delegates",
        "category": "Research Guides",
        "description": "Practical prompts for researching a country, agenda and policy options.",
        "file": None,
    },
    {
        "title": "Sample Position Paper",
        "category": "Writing Guides",
        "description": "A sample resource will be added after review by the organising team.",
        "file": None,
    },
    {
        "title": "Committee Background Guides",
        "category": "Committee Guides",
        "description": "Committee-specific background material will be published when confirmed.",
        "file": None,
    },
]

# Placeholder profiles intentionally contain no assumed personal identities.
MEMBERS = [
    {"name": "Name to be added", "role": "Secretariat designation to be confirmed", "group": "Secretariat", "description": "Profile details will be added with verified information.", "initials": "—"},
    {"name": "Name to be added", "role": "Executive Board role to be confirmed", "group": "Executive Board", "description": "Profile details will be added with verified information.", "initials": "—"},
    {"name": "Name to be added", "role": "Organising Committee role to be confirmed", "group": "Organising Committee", "description": "Profile details will be added with verified information.", "initials": "—"},
    {"name": "Name to be added", "role": "Technical Team role to be confirmed", "group": "Technical Team", "description": "Profile details will be added with verified information.", "initials": "—"},
]

# Leadership photos and biographies can be added once the organising team supplies them.
LEADERSHIP_2026 = [
    {
        "name": "Nikhil Nayak",
        "role": "Secretary General",
        "introduction": "",
        "image": None,
        "portrait_label": "Nikhil Nayak portrait to be added",
    },
    {
        "name": "V. Koushik",
        "role": "Director General",
        "introduction": "",
        "image": None,
        "portrait_label": "V. Koushik portrait to be added",
    },
    {
        "name": "Karthik Prasad M.",
        "role": "Head of Equity",
        "introduction": "",
        "image": None,
        "portrait_label": "Karthik Prasad M. portrait to be added",
    },
    {
        "name": "Vamshi Ganesh",
        "role": "Head of Equity",
        "introduction": "",
        "image": None,
        "portrait_label": "Vamshi Ganesh portrait to be added",
    },
]

EVENT = {
    "name": "RNSIT MUN 2026",
    "year": "2026",
    "date": "06–07 October 2026",
    "subtitle": "An Assembly of Ideas. A Dialogue of Nations.",
    "description": "Two days of active debate, policy making and diplomacy at RNSIT.",
    "purpose": "RNSIT MUN 2026 brought delegates together to debate, negotiate and explore policy through diplomacy.",
    "status": "Completed",
    "image_filename": CONFERENCE_2026_IMAGE,
    "website": CONFERENCE_2026_URL,
    "highlights": [
        "150+ delegates from across colleges.",
        "Six committees with diverse agendas and specialized councils.",
        "Two days of debate, policy making and diplomacy.",
        "₹1,00,000+ prize pool.",
    ],
    "statistics": [
        {"value": "150+", "label": "Delegates"},
        {"value": "6", "label": "Committees"},
        {"value": "2", "label": "Conference days"},
        {"value": "₹1,00,000+", "label": "Prize pool"},
    ],
}

CONFERENCES = [EVENT]

PHOTO_CATEGORIES = [
    ("opening", "Opening Ceremony"),
    ("committee", "Committee Sessions"),
    ("delegate", "Delegate Discussions"),
    ("executive-board", "Executive Board"),
    ("organising-team", "Organising Team"),
    ("closing", "Closing Ceremony"),
    ("award", "Award Distribution"),
]


def get_event_gallery():
    """Build a gallery from local event photos without editing templates."""
    if not EVENTS_DIR.exists():
        return []

    photos = []
    for image_path in sorted(EVENTS_DIR.iterdir(), key=lambda item: item.name.lower()):
        if image_path.is_file() and image_path.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS:
            stem = image_path.stem.replace("_", " ").replace("-", " ").strip()
            caption = " ".join(stem.split()).title() or "Conference moment"
            category = "Conference Moments"
            if image_path.name == CONFERENCE_2026_IMAGE:
                caption = "RNSIT MUN 2026 organising committee"
                category = "Organising Team"
            lowered = image_path.stem.lower().replace("_", "-")
            if category == "Conference Moments":
                for prefix, label in PHOTO_CATEGORIES:
                    if lowered.startswith(prefix):
                        category = label
                        break
            photos.append({
                "url": url_for("static", filename=f"images/events/{image_path.name}"),
                "caption": caption,
                "category": category,
                "filename": image_path.name,
            })
    return photos


def validate_email(value):
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value.strip()))


def validate_phone(value):
    digits = re.sub(r"\D", "", value)
    return 7 <= len(digits) <= 15


SMTP_TIMEOUT_SECONDS = 12
REGISTRATION_EMAIL_ENABLED = os.getenv("REGISTRATION_EMAIL_ENABLED", "True").strip().lower() in {"true", "1", "yes"}
USED_REGISTRATION_TOKENS = set()
REGISTRATION_TOKEN_LOCK = threading.Lock()


class EmailConfigurationError(Exception):
    """Raised when registration email settings are incomplete or disabled."""


def get_smtp_configuration():
    if not REGISTRATION_EMAIL_ENABLED:
        raise EmailConfigurationError("Registration email is disabled in server configuration.")

    names = ("SMTP_HOST", "SMTP_PORT", "SMTP_USE_TLS", "SMTP_USERNAME", "SMTP_PASSWORD", "SMTP_SENDER", "ADMIN_EMAIL")
    settings = {name: os.getenv(name, "").strip() for name in names}
    missing = [name for name, value in settings.items() if not value]
    if missing:
        raise EmailConfigurationError("Missing required email settings: " + ", ".join(missing))
    try:
        settings["SMTP_PORT"] = int(settings["SMTP_PORT"])
    except ValueError as error:
        raise EmailConfigurationError("SMTP_PORT must be a valid port number.") from error
    settings["SMTP_USE_TLS"] = settings["SMTP_USE_TLS"].lower() in {"true", "1", "yes"}
    if not settings["SMTP_HOST"] or not 1 <= settings["SMTP_PORT"] <= 65535 or not settings["SMTP_USE_TLS"]:
        raise EmailConfigurationError("SMTP host, port, and STARTTLS settings are invalid.")
    return settings


def build_registration_messages(values, submitted_at):
    """Create the admin notification and receipt-only applicant confirmation."""
    settings = get_smtp_configuration()
    rows = [
        ("Full name", values["full_name"]),
        ("Email", values["email"]),
        ("Phone number", values["phone"]),
        ("College / institution", values["institution"]),
        ("Year of study", values["year"]),
        ("Previous MUN experience", values["experience"] or "Not provided"),
        ("Committee preference", values["committee"]),
        ("Additional message", values["message"] or "Not provided"),
        ("Submitted at (UTC)", submitted_at),
    ]
    plain_rows = "\n".join(f"{label}: {value}" for label, value in rows)
    html_rows = "".join(
        f"<tr><th style='padding:10px 12px;text-align:left;border-bottom:1px solid #e5e0d7'>{escape(label)}</th>"
        f"<td style='padding:10px 12px;border-bottom:1px solid #e5e0d7'>{escape(value).replace(chr(10), '<br>')}</td></tr>"
        for label, value in rows
    )

    admin_message = EmailMessage()
    admin_message["Subject"] = f"New RNSIT MUN Registration – {values['full_name']}"
    admin_message["From"] = settings["SMTP_SENDER"]
    admin_message["To"] = settings["ADMIN_EMAIL"]
    admin_message.set_content(f"New RNSIT MUN registration\n\n{plain_rows}")
    admin_message.add_alternative(
        "<html><body style='font-family:Arial,sans-serif;color:#1d2732'>"
        "<h2 style='color:#101b2d'>New RNSIT MUN registration</h2>"
        f"<table style='border-collapse:collapse;width:100%;max-width:680px'>{html_rows}</table></body></html>",
        subtype="html",
    )

    applicant_name = values["full_name"]
    receipt_text = (
        f"Hello {applicant_name},\n\nThank you for submitting your registration for RNSIT MUN.\n\n"
        "We have successfully received your registration details. Your information has been submitted to the organising team for review.\n\n"
        "Further communication regarding your application will be shared through the official communication channels.\n\n"
        "Thank you for your interest in RNSIT MUN.\n\nRegards,\nRNSIT MUN Organising Team"
    )
    applicant_message = EmailMessage()
    applicant_message["Subject"] = "Registration Received – RNSIT MUN"
    applicant_message["From"] = settings["SMTP_SENDER"]
    applicant_message["To"] = values["email"]
    applicant_message.set_content(receipt_text)
    applicant_message.add_alternative(
        "<html><body style='font-family:Arial,sans-serif;color:#1d2732;line-height:1.6'>"
        f"<p>Hello {escape(applicant_name)},</p>"
        "<p>Thank you for submitting your registration for RNSIT MUN.</p>"
        "<p>We have successfully received your registration details. Your information has been submitted to the organising team for review.</p>"
        "<p>Further communication regarding your application will be shared through the official communication channels.</p>"
        "<p>Thank you for your interest in RNSIT MUN.</p><p>Regards,<br>RNSIT MUN Organising Team</p></body></html>",
        subtype="html",
    )
    return settings, (admin_message, applicant_message)


def send_registration_emails(values, submitted_at):
    settings, messages = build_registration_messages(values, submitted_at)
    with smtplib.SMTP(settings["SMTP_HOST"], settings["SMTP_PORT"], timeout=SMTP_TIMEOUT_SECONDS) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(settings["SMTP_USERNAME"], settings["SMTP_PASSWORD"])
        for message in messages:
            smtp.send_message(message)


def new_registration_token():
    token = uuid.uuid4().hex
    session["registration_form_token"] = token
    return token


@app.context_processor
def inject_site_data():
    return {"site_name": "RNSIT MUN", "year": 2026}


@app.get("/")
def home():
    photos = get_event_gallery()
    featured_photo = next((photo for photo in photos if photo["filename"] == CONFERENCE_2026_IMAGE), None)
    return render_template(
        "index.html",
        committees=COMMITTEES[:4],
        photos=photos,
        featured_photo=featured_photo,
        leaders=LEADERSHIP_2026,
        event=EVENT,
        conference_url=CONFERENCE_2026_URL,
        page="Home",
    )


@app.get("/about")
def about():
    return render_template("about.html", page="About")


@app.get("/committees")
def committees():
    return render_template("committees.html", committees=COMMITTEES, page="Committees")


@app.get("/events")
def events():
    photos = get_event_gallery()
    archive_entries = []
    featured_filenames = set()
    for conference in CONFERENCES:
        featured_filename = conference.get("image_filename")
        featured_photo = next((photo for photo in photos if photo["filename"] == featured_filename), None)
        if featured_filename:
            featured_filenames.add(featured_filename)
        archive_entries.append({"conference": conference, "photo": featured_photo})
    gallery_photos = [photo for photo in photos if photo["filename"] not in featured_filenames]
    photo_groups = []
    for photo in gallery_photos:
        group = next((item for item in photo_groups if item["name"] == photo["category"]), None)
        if group is None:
            group = {"name": photo["category"], "photos": []}
            photo_groups.append(group)
        group["photos"].append(photo)
    return render_template(
        "events.html",
        photos=photos,
        archive_entries=archive_entries,
        photo_groups=photo_groups,
        page="Events",
    )


@app.get("/members")
def members():
    groups = ["Secretariat", "Executive Board", "Organising Committee", "Technical Team"]
    return render_template("members.html", members=MEMBERS, groups=groups, leaders=LEADERSHIP_2026, page="Secretariat")


@app.get("/resources")
def resources():
    categories = sorted({item["category"] for item in RESOURCES})
    return render_template("resources.html", resources=RESOURCES, categories=categories, page="Resources")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    errors = {}
    values = {}
    form_error = ""
    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in (
            "full_name", "email", "phone", "institution", "year", "experience", "committee", "message"
        )}
        required = {
            "full_name": "Please enter your full name.",
            "email": "Please enter your email address.",
            "phone": "Please enter your phone number.",
            "institution": "Please enter your college or institution.",
            "year": "Please select your year of study.",
            "committee": "Please select a committee preference.",
        }
        errors.update({field: message for field, message in required.items() if not values[field]})
        field_limits = {"full_name": 120, "email": 254, "phone": 32, "institution": 180, "experience": 2000, "message": 2000}
        for field, limit in field_limits.items():
            if len(values[field]) > limit:
                errors[field] = f"Please keep this field under {limit} characters."
        if any(ord(character) < 32 for character in values["full_name"]):
            errors["full_name"] = "Please enter your name on one line."
        if values["year"] and values["year"] not in {"1st year", "2nd year", "3rd year", "4th year", "Other"}:
            errors["year"] = "Choose one of the listed study years."
        if values["email"] and not validate_email(values["email"]):
            errors["email"] = "Enter a valid email address."
        if values["phone"] and not validate_phone(values["phone"]):
            errors["phone"] = "Enter a phone number with 7 to 15 digits."
        valid_committees = {item["short_name"] for item in COMMITTEES}
        if values["committee"] and values["committee"] not in valid_committees:
            errors["committee"] = "Choose one of the listed committee preferences."
        form_token = request.form.get("form_token", "")
        honeypot_filled = bool(request.form.get("website", "").strip())
        if honeypot_filled or not form_token or form_token != session.get("registration_form_token"):
            form_error = "This form could not be verified. Please refresh the page and try again."
        if errors:
            return render_template("registration.html", committees=COMMITTEES, errors=errors, values=values, form_error=form_error, form_token=form_token, page="Registration"), 400
        if form_error:
            return render_template("registration.html", committees=COMMITTEES, errors=errors, values=values, form_error=form_error, form_token=new_registration_token(), page="Registration"), 400

        with REGISTRATION_TOKEN_LOCK:
            if form_token in USED_REGISTRATION_TOKENS:
                form_error = "This registration was already submitted. Refresh the page before sending another."
            else:
                USED_REGISTRATION_TOKENS.add(form_token)
                session.pop("registration_form_token", None)
        if form_error:
            return render_template("registration.html", committees=COMMITTEES, errors=errors, values=values, form_error=form_error, form_token=new_registration_token(), page="Registration"), 400

        submitted_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        try:
            send_registration_emails(values, submitted_at)
        except EmailConfigurationError as error:
            app.logger.error("Registration email configuration unavailable: %s", error)
            form_error = "Registration email is not configured yet. Please contact the organising team. Your entries are still here."
        except (smtplib.SMTPException, TimeoutError, OSError):
            app.logger.exception("Registration SMTP delivery failed")
            form_error = "We could not send the registration emails. Please try again later; your entries are still here."
        except Exception:
            app.logger.exception("Registration email workflow failed")
            form_error = "We could not send the registration emails. Please try again later; your entries are still here."
        if form_error:
            return render_template("registration.html", committees=COMMITTEES, errors=errors, values=values, form_error=form_error, form_token=new_registration_token(), page="Registration"), 503
        flash("Your registration was received. A confirmation email has been sent, and the organising team has been notified.", "success")
        return redirect(url_for("registration"))
    return render_template("registration.html", committees=COMMITTEES, errors=errors, values=values, form_error=form_error, form_token=new_registration_token(), page="Registration")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    errors = {}
    values = {}
    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in ("name", "email", "subject", "message")}
        for field, label in (("name", "name"), ("email", "email address"), ("subject", "subject"), ("message", "message")):
            if not values[field]:
                errors[field] = f"Please enter your {label}."
        if values["email"] and not validate_email(values["email"]):
            errors["email"] = "Enter a valid email address."
        if errors:
            return render_template("contact.html", errors=errors, values=values, page="Contact"), 400
        flash("Thanks for your message. This is a demonstration form; no message was sent or saved.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html", errors=errors, values=values, page="Contact")


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html", page="Page not found"), 404


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
