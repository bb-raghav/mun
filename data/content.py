"""Verified RNSIT MUN site content. Keep public-facing facts in this module."""

SITE = {
    "name": "RNSIT MUN Society",
    "short_name": "RNSIT MUNSoc",
    "institution": "RNS Institute of Technology",
    "city": "Bengaluru, Karnataka",
    "email": "mun@rnsit.ac.in",
    "instagram": "@rnsit.mun",
    "instagram_url": "https://www.instagram.com/rnsit.mun/",
    "conference_url": "https://mun-gold.vercel.app/",
}

VENUE = {
    "name": "RNS Institute of Technology",
    "address": "Dr. Vishnuvardhan Road, Channasandra, RR Nagar, Bengaluru, Karnataka – 560098",
    "railway": "Kengeri Railway Station",
    "railway_distance": "Approximately 6 km",
    "metro": "Rajarajeshwari Nagar Metro Station",
    "metro_distance": "Approximately 5.1 km",
    "bus_stop": "Channasandra bus stop",
    "bus_distance": "Approximately 400 metres",
    "coordinates": "12.9014° N, 77.5178° E",
    "coordinates_url": "https://www.google.com/maps/search/?api=1&query=12.9014%2C77.5178",
    "map_url": "https://maps.google.com/?q=RNS+Institute+of+Technology,+Dr.+Vishnuvardhan+Road,+Bengaluru+560098",
    "map_embed_url": "https://maps.google.com/maps?q=RNS+Institute+of+Technology,+Dr.+Vishnuvardhan+Road,+Bengaluru+560098&output=embed",
}

CONFERENCE = {
    "name": "RNS MUN 2026",
    "year": "2026",
    "dates": "6–7 October 2026",
    "format": "Two-day, in-person Model United Nations conference",
    "venue": VENUE["name"],
    "home_summary": "A two-day, in-person gathering at RNSIT, with six committees, moderated debate and collaborative activities.",
    "description": "RNS MUN 2026 was the first flagship conference organised by RNSIT MUNSoc. It brought delegates together for two days of committee debate, negotiation and collaboration.",
    "image": "images/events/IMG_6131.JPG",
    "website": SITE["conference_url"],
    "brochure": "https://mun-gold.vercel.app/assets/brochure/RNS%20MUN%202026-%20ConferenceBrochure.pdf",
    "advertised_stats": [
        {"value": "6", "label": "Committees"},
        {"value": "150+", "label": "Delegates advertised"},
        {"value": "₹1,00,000+", "label": "Advertised prize pool"},
        {"value": "2 days", "label": "In-person conference"},
    ],
    "highlights": [
        "Six committees with distinct international, national and media agendas.",
        "Delegate kits and committee background guides.",
        "Committee sessions, moderated debate and collaborative activities.",
        "A Chief Guest feature, awards and recognition.",
    ],
    "committees": [
        {
            "short_name": "UNSC",
            "name": "United Nations Security Council",
            "agenda": "Addressing parallel governments and de facto authorities in civil wars, focusing on sovereignty, territorial control and international recognition.",
            "description": "Delegates considered questions of legitimacy and international engagement where competing authorities govern during civil conflict.",
            "symbol": "01",
        },
        {
            "short_name": "UNHRC",
            "name": "United Nations Human Rights Council",
            "agenda": "Safeguarding freedom of expression and the safety of journalists in conflict and post-conflict zones.",
            "description": "The committee examined protections for journalists and the role of expression in areas affected by conflict.",
            "symbol": "02",
        },
        {
            "short_name": "DISEC",
            "name": "Disarmament and International Security",
            "agenda": "Regulating the militarisation of outer space and the development of Anti-Satellite (ASAT) weapons.",
            "description": "Delegates addressed security, arms control and the growing risks associated with anti-satellite capabilities.",
            "symbol": "03",
        },
        {
            "short_name": "LOK SABHA",
            "name": "Lok Sabha",
            "agenda": "Post-census delimitation and fiscal redistribution, addressing regional representation and inter-state fiscal equity.",
            "description": "The parliamentary simulation focused on representation and the distribution of fiscal resources between states.",
            "symbol": "04",
        },
        {
            "short_name": "UNODC",
            "name": "United Nations Office on Drugs and Crime",
            "agenda": "Combating technology-facilitated human trafficking, online child exploitation and illicit financial flows.",
            "description": "The committee considered how technology and financial systems are used to facilitate trafficking and exploitation.",
            "symbol": "05",
        },
        {
            "short_name": "IPC",
            "name": "International Press Corps",
            "agenda": "Investigative journalism, real-time crisis coverage, press conferences and daily report publications.",
            "description": "Press Corps members reported on committee developments through journalism and daily coverage.",
            "symbol": "06",
        },
    ],
    "guest": {
        "name": "Donovan Müller",
        "role": "Innovation Associate, Swissnex in India, Consulate General of Switzerland",
        "title": "Chief Guest",
        "summary": "His remarks at the conference highlighted the value of developing one’s voice, confidence and ability to make an impact.",
        "image": "images/chief-guest.jpeg",
    },
    "awards": [
        {"name": "Best Delegate", "amount": "₹8,000"},
        {"name": "High Commendation", "amount": "₹5,000"},
        {"name": "Special Mention", "amount": "₹3,000"},
        {"name": "IPC Best Reporter", "amount": "₹6,000"},
        {"name": "IPC High Commendation", "amount": "₹4,000"},
        {"name": "Best Delegation", "amount": "₹10,000 + trophy"},
    ],
    "prize_pool": "₹1,00,000+",
}

HISTORY = [
    {"date": "2023", "title": "RNSIT MUNSoc established", "description": "The society began creating opportunities for students to explore global affairs, public speaking and diplomacy."},
    {"date": "2024", "title": "Nexus and introductory MUN", "description": "The Society began moving from introductory sessions toward recurring committee simulations."},
    {"date": "2024–2025", "title": "Atlas World Affairs Quiz", "description": "The 2024 and 2025 editions together drew 170 students from more than 15 colleges."},
    {"date": "2025", "title": "Training and student activities", "description": "Member programmes and student activities continued through the year."},
    {"date": "May 2026", "title": "Third Nexus IntraMUN", "description": "Nexus returned for its third edition as an intra-college MUN activity."},
    {"date": "2026", "title": "Qlue Quiz Club", "description": "The society established Qlue Quiz Club to bring students together through quizzes and shared curiosity."},
    {"date": "October 2026", "title": "RNS MUN 2026", "description": "The society hosted its first flagship RNS MUN conference at RNS Institute of Technology."},
]

ACTIVITIES = [
    {"date": "2024 · 2026", "name": "Nexus IntraMUN", "description": "Introductory MUN activities that grew into a recurring intra-college conference. The third edition took place in May 2026."},
    {"date": "2024 · 2025", "name": "Atlas World Affairs Quiz", "description": "Intercollegiate quiz editions invited students to test their knowledge of current affairs and global issues."},
    {"date": "Ongoing", "name": "Training and discussions", "description": "Training programmes and discussions help members explore diplomacy, international affairs and structured debate."},
    {"date": "2026", "name": "Qlue Quiz Club", "description": "A quiz initiative established to connect students through curiosity and knowledge across subjects."},
]

SECRETARIAT = [
    {"name": "Nikhil Nayak", "role": "Secretary General", "image": "images/events/members/nikhil-nayak.JPG", "alt": "Nikhil Nayak"},
    {"name": "V. Koushik", "role": "Director General", "image": "images/events/members/v-koushik.JPG", "alt": "V. Koushik"},
    {"name": "Karthik Prasad M.", "role": "Head – Technical", "image": "images/events/members/karthik-prasad.JPG", "alt": "Karthik Prasad M."},
    {"name": "Vamshi Ganesh B.", "role": "Head – Media & Design", "image": "images/events/members/vamshi-ganesh.jpg", "alt": "Vamshi Ganesh B."},
]

ORGANISING_COMMITTEE = [
    {"department": "Technical", "members": ["Karthik Prasad M.", "Shriyanshu Kumar Kapsime"]},
    {"department": "Delegate Affairs", "members": ["Zeyan Shahid Khan", "Adith D H"]},
    {"department": "EB Affairs", "members": ["Vachan B Hindiskere", "Tanmay P Shetty"]},
    {"department": "Finance", "members": ["Poorvika Nagaraj"]},
    {"department": "Media & Design", "members": ["Vamshi Ganesh B."]},
    {"department": "Operations", "members": ["Manu T.", "R J Varsha"]},
    {"department": "Creatives & Décor", "members": ["Nuha Alishba", "Divya Sharma"]},
    {"department": "Outreach & Marketing", "members": ["Rudra Chakraborty", "Kapil Pal"]},
    {"department": "Partnerships & Sponsorship", "members": ["Anantha Narayan Prabhu"]},
    {"department": "Content", "members": ["Dhatri V A"]},
]

EXECUTIVE_BOARD = [
    {"committee": "UNSC", "members": ["Shishir Simha — Chair", "Sathya Shiva — Vice Chair", "Kapil Pal — Moderator"]},
    {"committee": "UNHRC", "members": ["Kshitij Saha — Co-Chair", "Sahit Bangre — Co-Chair", "Tanmay P. Shetty — Vice Chair"]},
    {"committee": "DISEC", "members": ["Sumit Shingare — Co-Chair", "Sanchya Prathish — Co-Chair", "Vachan B. Hindiskere — Vice Chair"]},
    {"committee": "Lok Sabha", "members": ["Anshuman Pandey — Chair", "Rajath R — Vice Chair", "Jayanth N — Moderator"]},
    {"committee": "UNODC", "members": ["Phani Sreevatsa — Chair", "Pranathi Naik — Vice Chair", "Divya Sharma — Moderator"]},
    {"committee": "IPC", "members": ["Pranav Sivakumar — Head", "Nuha Alishba — Deputy Head"]},
]

RESOURCES = [
    {
        "title": "RNS MUN 2026 Conference Brochure",
        "category": "Conference",
        "description": "The original 15-page brochure with conference information, committees and award details.",
        "url": CONFERENCE["brochure"],
        "external": True,
    },
]

PAGE_META = {
    "Home": ("RNSIT MUN Society | Bengaluru", "The student society for Model United Nations at RNS Institute of Technology, Bengaluru."),
    "About": ("About RNSIT MUNSoc", "Learn about RNSIT MUNSoc, its history since 2023, activities and student community."),
    "Conference": ("RNS MUN 2026 | Conference Archive", "Explore the RNS MUN 2026 conference, its six committees, Chief Guest, awards and photographs."),
    "Events": ("Society Events and Activities | RNSIT MUN", "Explore Nexus IntraMUN, the Atlas World Affairs Quiz, training programmes and Qlue Quiz Club."),
    "Secretariat": ("Secretariat and Team | RNSIT MUN", "Meet the RNSIT MUNSoc Secretariat, organising committee departments and RNS MUN 2026 Executive Board."),
    "Resources": ("MUN Resources | RNSIT MUN", "Access the official RNS MUN 2026 conference brochure and delegate resources."),
    "Registration": ("Future Edition Interest | RNSIT MUN", "Register your interest in future RNSIT MUN Society conference announcements."),
    "Contact": ("Contact RNSIT MUNSoc", "Send an enquiry to the RNSIT MUNSoc organising team or follow the Society on Instagram."),
    "Venue": ("Venue and Directions | RNSIT MUN", "Find RNS Institute of Technology in Bengaluru and nearby public transport connections."),
    "Page not found": ("Page not found | RNSIT MUN", "The requested RNSIT MUN page could not be found."),
}
