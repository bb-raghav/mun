# RNSIT MUN Society website

A responsive Flask and Jinja website for RNSIT MUNSoc, built with one shared stylesheet and vanilla JavaScript. It retains the approved navy, ivory and gold palette and the existing registration email workflow. There is no database or frontend build step.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -n .env.example .env
python main.py
```

Open <http://127.0.0.1:5000>. `.env` is private and excluded from version control. Keep SMTP credentials out of source files and commits.

## Project layout

```text
main.py                 Flask routes and registration mail workflow
data/content.py         Public society, conference, team, venue and resource content
templates/              Jinja pages
static/css/main.css     Shared responsive design
static/js/main.js       Navigation, resource and photo-viewer interactions
static/images/events/   Conference committee photograph
static/images/events/members/  Secretariat portraits
static/documents/       Local resource files, if supplied
```

Edit verified public-facing facts in `data/content.py`. The About page uses the Society timeline; the Team page holds the complete Secretariat, department and Executive Board rosters; the Conference page is the authoritative 2026 archive; Venue holds the address and transport information. `/committees` redirects to the committee section of the Conference archive.

## Images and documents

The RNS MUN 2026 organising committee photograph is `static/images/events/IMG_6131.JPG`. It appears as a homepage preview and in the conference archive. The Chief Guest portrait is `static/images/chief-guest.jpeg`. The four Secretariat portraits are in `static/images/events/members/`. Raghav’s photo is in `static/images/events/raghav.jpeg`. No award-winner images are included.

The original 15-page RNS MUN 2026 brochure is linked from the official conference site on the Resources and Conference pages. No background guides or sample resolutions are included in this repository.

## Email behaviour

The Contact form sends enquiries to `ADMIN_EMAIL` and uses the submitter's email as Reply-To. The registration page collects interest in future editions; on a valid submission, the app emails `ADMIN_EMAIL` and sends the applicant a confirmation. Configure SMTP values and `ADMIN_EMAIL` in `.env` using `.env.example` as a guide. SMTP route tests should mock the mail server; do not send test messages to real recipients.

The Contact page links to the Society's Instagram and sends form enquiries to the configured admin inbox. Contact submissions are not stored in a database.

## Verification

Run the app with `python main.py`. Check the routes `/`, `/about`, `/conferences`, `/events`, `/members`, `/resources`, `/venue`, `/registration` and `/contact`. Use a mocked SMTP server to exercise registration email handling without sending real mail.
