# RNSIT MUN website prototype

A responsive website for RNSIT Model United Nations. It uses Flask and Jinja templates with one CSS file and one vanilla JavaScript file. The approved navy, ivory and muted gold palette is shared across all routes. The homepage includes a CSS animated dotted globe and a 2026 conference feature; the globe falls back to its static SVG artwork and stops moving for reduced-motion preferences.

## Technology

- Python 3
- Flask
- python-dotenv
- HTML5 templates with Jinja2
- CSS3
- Vanilla JavaScript

There is no database, authentication, external API or frontend build step. Registration sends email with Python's standard `smtplib` and `EmailMessage`; SMTP credentials are read from the local `.env` file. The only externally hosted visual assets are the optional Google Fonts; system font fallbacks remain available.

## Folder structure

```text
.
├── main.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── committees.html
│   ├── events.html
│   ├── members.html
│   ├── resources.html
│   ├── registration.html
│   ├── contact.html
│   └── 404.html
└── static/
    ├── css/main.css
    ├── js/main.js
    ├── images/events/
    └── documents/
```

## Install and run

From the project folder, create and activate a virtual environment, then install the requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -n .env.example .env
python main.py
```

Open <http://127.0.0.1:5000>. Flask debug mode is enabled for local development only.

`.env.example` is a safe template containing placeholders. `.env` is your private local configuration file; replace its values with your own credentials. The `cp -n` command preserves an existing `.env` rather than replacing it. The `.gitignore` excludes `.env` and virtual-environment files. Never commit or share `.env` or an App Password.

## Add event photographs

The existing `IMG_6131.JPG` organising committee photograph is preserved and used in the homepage feature and 2026 archive entry. It keeps its original 3:2 proportions and is not cropped.

Copy additional conference photographs into `static/images/events/`. The app automatically picks up `.jpg`, `.jpeg`, `.png` and `.webp` files from that folder; no HTML change is needed for each new photo.

Use a useful filename for the caption. The first part of the filename also selects a section when it matches one of these prefixes:

- `opening-` — Opening Ceremony
- `committee-` — Committee Sessions
- `delegate-` — Delegate Discussions
- `executive-board-` — Executive Board
- `organising-team-` — Organising Team
- `closing-` — Closing Ceremony
- `award-` — Award Distribution

For example, `opening-ceremony-01.jpg` appears under “Opening Ceremony”. Files without a matching prefix appear under “Conference Moments”. Additional photos appear in the Past Conferences gallery with a keyboard-accessible lightbox. Add only photographs that are approved for publication. The project currently has one group photograph and no individual leadership portraits.

## Add PDFs

Put approved PDFs in `static/documents/`. Resource entries are defined in the `RESOURCES` list near the top of `main.py`. Set an entry's `file` value to its filename (for example, `rules-of-procedure.pdf`) to enable its download link. An entry with `file: None` remains marked “PDF to be added”; it never points to a fake download.

Committee study guide links are set in each committee dictionary's `study_guide` value. Leave it as `None` until a verified guide is available.

## Update the 2026 leadership profiles

Four identified members are listed in the `LEADERSHIP_2026` list in `main.py`: Nikhil Nayak (Secretary General), V. Koushik (Director General), Karthik Prasad M. (Head of Equity), and Vamshi Ganesh (Head of Equity). Edit each member's `name`, `role`, `image` and `portrait_label` there. Approved portrait paths should be relative to `static/`, for example `images/members/nikhil-nayak.jpg`. The same profiles appear on the homepage and Secretariat page.

The President's identity and designation are not confirmed and are intentionally not assigned to anyone. Individual portraits were not present in the supplied project assets, so each member currently has a labelled portrait placeholder. No biographies or social links have been invented.

## Update other team members

Edit the `MEMBERS` list in `main.py`. Each profile has `name`, `role`, `group` and `description` fields. The available groups are Secretariat, Executive Board, Organising Committee and Technical Team. Replace the placeholder information only with verified member details. The profile portrait area remains an explicit placeholder until real member photos are supplied.

## Update the MUN 2026 feature and archive

Edit the `EVENT` dictionary in `main.py` to update the conference title, date, subtitle, description, highlights, statistics, website and image filename. The current date and 2026 highlights are from the [official conference website](https://mun-gold.vercel.app/). The organising committee image is `static/images/events/IMG_6131.JPG`; keep that file unless replacing it with an approved higher-resolution version.

The Past Conferences page is rendered from the `CONFERENCES` list in `main.py`. Add future editions to that list with their confirmed details and approved photos.

## Update committee information

Edit the `COMMITTEES` list in `main.py`. Each committee entry includes its displayed name, short name, description, sample agenda, overview, delegate responsibilities and executive board information. The included agendas are illustrative examples and should be replaced with approved conference details.

## Update personal and contact details

The editable “Meet the Developer” copy is in `templates/about.html`. Official email, Instagram and campus-location placeholders are in `templates/contact.html` and `templates/base.html`. Replace them with confirmed contact details before presenting the site as official.

## Gmail registration email setup

The registration form sends an admin notification to `ADMIN_EMAIL` and a receipt-only confirmation to the applicant. It does not store registration data in a database. The contact form retains its existing demonstration behavior and does not send email.

### Create a Gmail App Password

This SMTP setup generally requires a Google App Password; a normal Gmail account password usually will not work. Enable Google 2-Step Verification on the Gmail account, then create an App Password in your Google Account security settings. Put that generated App Password in `SMTP_PASSWORD` in `.env`. Never share or commit it.

### Values to set in `.env`

- `SMTP_HOST=smtp.gmail.com`
- `SMTP_PORT=587`
- `SMTP_USE_TLS=True`
- `SMTP_USERNAME` — the Gmail address used to authenticate
- `SMTP_PASSWORD` — the generated Google App Password
- `SMTP_SENDER` — the Gmail address shown as the sender (usually the same address)
- `ADMIN_EMAIL` — the inbox that should receive new registrations
- `REGISTRATION_EMAIL_ENABLED=True`

Email delivery is enabled by default. If required settings are missing or invalid, the form displays a server-side configuration error and does not claim delivery succeeded. Set `REGISTRATION_EMAIL_ENABLED=False` to disable registration email sending.

### Test delivery

After configuring `.env`, run `python main.py`, open the registration page and submit a test using an email address you control. The site should show success only after both SMTP messages are sent. Automated route tests should mock SMTP and must not send test messages to real recipients.

If authentication fails, confirm that 2-Step Verification is enabled, that `SMTP_PASSWORD` is an App Password with spaces removed, and that `SMTP_USERNAME` and `SMTP_SENDER` are correct. Also check that Gmail SMTP access is permitted for the account. The page reports a generic error; technical SMTP details are written to the local Flask server log without printing the password.

## Contact form

The existing contact form remains a local demonstration form. It validates input and confirms receipt in the page but does not send email or persist the message.
