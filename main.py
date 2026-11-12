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
from data.content import (
    ACTIVITIES,
    CONFERENCE,
    EXECUTIVE_BOARD,
    HISTORY,
    ORGANISING_COMMITTEE,
    PAGE_META,
    RESOURCES,
    SECRETARIAT,
    SITE,
    VENUE,
)

app = Flask(__name__)
app.secret_key = "rnsit-mun-local-prototype"

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

COMMITTEES = CONFERENCE["committees"]


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
    """Raised when SMTP email settings are incomplete or disabled."""


def get_smtp_configuration(require_admin=False):
    if not REGISTRATION_EMAIL_ENABLED:
        raise EmailConfigurationError("Website email is disabled in server configuration.")

    names = ("SMTP_HOST", "SMTP_PORT", "SMTP_USE_TLS", "SMTP_USERNAME", "SMTP_PASSWORD", "SMTP_SENDER")
    settings = {name: os.getenv(name, "").strip() for name in names}
    missing = [name for name, value in settings.items() if not value]
    if require_admin:
        settings["ADMIN_EMAIL"] = os.getenv("ADMIN_EMAIL", "").strip()
        if not settings["ADMIN_EMAIL"]:
            missing.append("ADMIN_EMAIL")
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
    settings = get_smtp_configuration(require_admin=True)
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
    admin_message["Subject"] = f"New RNSIT MUN Interest – {values['full_name']}"
    admin_message["From"] = settings["SMTP_SENDER"]
    admin_message["To"] = settings["ADMIN_EMAIL"]
    admin_message.set_content(f"New RNSIT MUN future-edition interest\n\n{plain_rows}")
    admin_message.add_alternative(
        "<html><body style='font-family:Arial,sans-serif;color:#1d2732'>"
        "<h2 style='color:#101b2d'>New RNSIT MUN future-edition interest</h2>"
        f"<table style='border-collapse:collapse;width:100%;max-width:680px'>{html_rows}</table></body></html>",
        subtype="html",
    )

    applicant_name = values["full_name"]
    receipt_text = (
        f"Hello {applicant_name},\n\nThank you for registering your interest in future RNSIT MUN Society editions.\n\n"
        "Your interest form has been received and shared with the organising team. This is not a conference registration or confirmation of a place.\n\n"
        "Future announcements will be shared through the Society’s official communication channels.\n\n"
        "Regards,\nRNSIT MUN Society"
    )
    applicant_message = EmailMessage()
    applicant_message["Subject"] = "Interest Received – RNSIT MUN Society"
    applicant_message["From"] = settings["SMTP_SENDER"]
    applicant_message["To"] = values["email"]
    applicant_message.set_content(receipt_text)
    applicant_message.add_alternative(
        "<html><body style='font-family:Arial,sans-serif;color:#1d2732;line-height:1.6'>"
        f"<p>Hello {escape(applicant_name)},</p>"
        "<p>Thank you for registering your interest in future RNSIT MUN Society editions.</p>"
        "<p>Your interest form has been received and shared with the organising team. This is not a conference registration or confirmation of a place.</p>"
        "<p>Future announcements will be shared through the Society’s official communication channels.</p>"
        "<p>Regards,<br>RNSIT MUN Society</p></body></html>",
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


def send_contact_email(values):
    """Send a website enquiry to the configured admin inbox."""
    settings = get_smtp_configuration(require_admin=True)
    message = EmailMessage()
    message["Subject"] = f"RNSIT MUN website enquiry: {values['subject']}"
    message["From"] = settings["SMTP_SENDER"]
    message["To"] = settings["ADMIN_EMAIL"]
    message["Reply-To"] = values["email"]
    message.set_content(
        "A message was sent through the RNSIT MUN website contact form.\n\n"
        f"Name: {values['name']}\n"
        f"Email: {values['email']}\n"
        f"Subject: {values['subject']}\n\n"
        f"{values['message']}\n"
    )
    with smtplib.SMTP(settings["SMTP_HOST"], settings["SMTP_PORT"], timeout=SMTP_TIMEOUT_SECONDS) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(settings["SMTP_USERNAME"], settings["SMTP_PASSWORD"])
        smtp.send_message(message)


def new_registration_token():
    token = uuid.uuid4().hex
    session["registration_form_token"] = token
    return token


@app.context_processor
def inject_site_data():
    endpoint_pages = {
        "home": "Home", "about": "About", "conferences": "Conference", "events": "Events",
        "members": "Secretariat", "resources": "Resources", "registration": "Registration",
        "contact": "Contact", "venue": "Venue", "page_not_found": "Page not found",
    }
    page_key = endpoint_pages.get(request.endpoint, "Home")
    title, description = PAGE_META[page_key]
    return {
        "site_name": SITE["name"],
        "site": SITE,
        "venue_info": VENUE,
        "year": 2026,
        "page_title": title,
        "page_description": description,
    }


@app.get("/")
def home():
    return render_template(
        "index.html",
        leaders=SECRETARIAT[:2],
        conference=CONFERENCE,
        page="Home",
    )


@app.get("/about")
def about():
    return render_template("about.html", history=HISTORY, page="About")


@app.get("/committees")
def committees():
    return redirect(url_for("conferences") + "#committees", code=302)


@app.get("/conferences")
def conferences():
    photo = {
        "url": url_for("static", filename=CONFERENCE["image"]),
        "caption": "RNS MUN 2026 organising committee",
    }
    return render_template(
        "conference.html",
        conference=CONFERENCE,
        committees=CONFERENCE["committees"],
        photo=photo,
        page="Conference",
    )


@app.get("/events")
def events():
    return render_template("events.html", activities=ACTIVITIES, page="Events")


@app.get("/members")
def members():
    return render_template(
        "members.html", leaders=SECRETARIAT, departments=ORGANISING_COMMITTEE,
        boards=EXECUTIVE_BOARD, page="Secretariat",
    )


@app.get("/resources")
def resources():
    return render_template("resources.html", resources=RESOURCES, categories=sorted({item["category"] for item in RESOURCES}), page="Resources")


@app.get("/venue")
def venue():
    return render_template("venue.html", venue=VENUE, page="Venue")


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
        flash("Your interest was received. A confirmation email has been sent, and the organising team has been notified.", "success")
        return redirect(url_for("registration"))
    return render_template("registration.html", committees=COMMITTEES, errors=errors, values=values, form_error=form_error, form_token=new_registration_token(), page="Registration")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    errors = {}
    values = {}
    form_error = ""
    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in ("name", "email", "subject", "message")}
        for field, label in (("name", "name"), ("email", "email address"), ("subject", "subject"), ("message", "message")):
            if not values[field]:
                errors[field] = f"Please enter your {label}."
        if values["email"] and not validate_email(values["email"]):
            errors["email"] = "Enter a valid email address."
        for field, limit in (("name", 120), ("subject", 180), ("message", 5000)):
            if len(values[field]) > limit:
                errors[field] = f"Please keep this field under {limit} characters."
        if any(ord(character) < 32 for character in values["name"] + values["subject"]):
            errors["subject"] = "Please keep your name and subject on one line."
        if errors:
            return render_template("contact.html", errors=errors, values=values, form_error=form_error, page="Contact"), 400
        try:
            send_contact_email(values)
        except EmailConfigurationError as error:
            app.logger.error("Contact email configuration unavailable: %s", error)
            form_error = "Email is not configured right now. Please email the Society directly."
        except (smtplib.SMTPException, TimeoutError, OSError):
            app.logger.exception("Contact SMTP delivery failed")
            form_error = "Your message could not be sent. Please try again later or email the Society directly."
        except Exception:
            app.logger.exception("Contact email workflow failed")
            form_error = "Your message could not be sent. Please try again later or email the Society directly."
        if form_error:
            return render_template("contact.html", errors=errors, values=values, form_error=form_error, page="Contact"), 503
        flash("Your message was sent to RNSIT MUNSoc. The team can reply directly to your email address.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html", errors=errors, values=values, form_error=form_error, page="Contact")


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html", page="Page not found"), 404


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
