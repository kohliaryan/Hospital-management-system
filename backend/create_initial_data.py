from models import DoctorAvailability, DoctorProfile, PatientProfile, Role, Specialization, User, db
from flask_security.utils import hash_password
from datetime import datetime
roles = ["Admin", "Doctor", "Patient"]
basic_users = [
    {
        "email": "admin@test.com",
        "password": "password",
        "role": "Admin"
    },
    {
        "email": "patient@test.com",
        "password": "password",
        "role": "Patient"      
    },
    {
        "email": "doctor@test.com",
        "password": "password",
        "role": "Doctor"   
    }
]

specializations = [
    "General Medicine",
    "Cardiology",
    "Orthopedics",
    "Gynecology",
    "Pediatrics",
    "Dermatology",
    "Neurology",
    "Psychiatry",
    "Oncology",
    "ENT (Otorhinolaryngology)",
    "Ophthalmology",
    "Urology",
    "Gastroenterology",
    "Pulmonology",
    "Endocrinology"
]

doctors = [
    # --- General Medicine ---
    {
        "email": "mehar.brar@test.com",
        "name": "Dr. Mehar Kaur Brar",
        "password": "password",
        "description": "MBBS, MD in Internal Medicine. 5 years experience. Focuses on holistic family health and preventive care.",
        "role": "Doctor",
        "consultation_price": 800,
        "specializations": ["General Medicine", "Pediatrics"],
        # [SPLIT SHIFT]: Mon, Wed, Fri
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Monday", "start_time": "17:00", "end_time": "20:00"},
            {"day_of_week": "Tuesday", "start_time": "09:00", "end_time": "17:00"},
            {"day_of_week": "Wednesday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Wednesday", "start_time": "17:00", "end_time": "20:00"},
            {"day_of_week": "Thursday", "start_time": "09:00", "end_time": "17:00"},
            {"day_of_week": "Friday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Friday", "start_time": "17:00", "end_time": "20:00"}
        ]
    },
    {
        "email": "kavita.iyer@test.com",
        "name": "Dr. Kavita Iyer",
        "password": "password",
        "description": "MBBS, MD in General Medicine. Senior Consultant with 15 years experience in diabetes and hypertension management.",
        "role": "Doctor",
        "consultation_price": 1200,
        "specializations": ["General Medicine", "Endocrinology"],
        # [SPLIT SHIFT]: Mon, Wed
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "10:00", "end_time": "13:00"},
            {"day_of_week": "Monday", "start_time": "18:00", "end_time": "21:00"},
            {"day_of_week": "Wednesday", "start_time": "10:00", "end_time": "13:00"},
            {"day_of_week": "Wednesday", "start_time": "18:00", "end_time": "21:00"},
            {"day_of_week": "Friday", "start_time": "10:00", "end_time": "14:00"}
        ]
    },
    {
        "email": "fatima.sheikh@test.com",
        "name": "Dr. Fatima Sheikh",
        "password": "password",
        "description": "MBBS, MD. Specialist in infectious diseases, viral fevers, and adult immunization.",
        "role": "Doctor",
        "consultation_price": 700,
        "specializations": ["General Medicine"],
        "availabilities": [
            {"day_of_week": "Tuesday", "start_time": "09:00", "end_time": "15:00"},
            {"day_of_week": "Thursday", "start_time": "09:00", "end_time": "15:00"},
            {"day_of_week": "Saturday", "start_time": "09:00", "end_time": "15:00"}
        ]
    },
    {
        "email": "rahul.verma@test.com",
        "name": "Dr. Rahul Verma",
        "password": "password",
        "description": "MBBS, DNB Family Medicine. Expert in geriatric care and lifestyle disease management.",
        "role": "Doctor",
        "consultation_price": 600,
        "specializations": ["General Medicine"],
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "16:00", "end_time": "21:00"},
            {"day_of_week": "Wednesday", "start_time": "16:00", "end_time": "21:00"},
            {"day_of_week": "Friday", "start_time": "16:00", "end_time": "21:00"}
        ]
    },
    {
        "email": "amit.patel@test.com",
        "name": "Dr. Amit Patel",
        "password": "password",
        "description": "MBBS, MD. Focuses on respiratory infections and seasonal allergies.",
        "role": "Doctor",
        "consultation_price": 700,
        "specializations": ["General Medicine", "Pulmonology"],
        # [SPLIT SHIFT]: Sat
        "availabilities": [
            {"day_of_week": "Saturday", "start_time": "09:00", "end_time": "12:00"},
            {"day_of_week": "Saturday", "start_time": "16:00", "end_time": "19:00"},
            {"day_of_week": "Sunday", "start_time": "10:00", "end_time": "14:00"}
        ]
    },

    # --- Cardiology ---
    {
        "email": "arjun.singh@test.com",
        "name": "Dr. Arjun Singh",
        "password": "password",
        "description": "MBBS, DM Cardiology. Interventional cardiologist specializing in angiography and angioplasty.",
        "role": "Doctor",
        "consultation_price": 1500,
        "specializations": ["Cardiology"],
        # [SPLIT SHIFT]: Mon, Fri
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "08:00", "end_time": "11:00"},
            {"day_of_week": "Monday", "start_time": "16:00", "end_time": "19:00"},
            {"day_of_week": "Wednesday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Friday", "start_time": "08:00", "end_time": "11:00"},
            {"day_of_week": "Friday", "start_time": "16:00", "end_time": "19:00"}
        ]
    },
    {
        "email": "neha.reddy@test.com",
        "name": "Dr. Neha Reddy",
        "password": "password",
        "description": "MBBS, DNB Cardiology. Specialist in non-invasive cardiology, echocardiography, and preventive heart care.",
        "role": "Doctor",
        "consultation_price": 1000,
        "specializations": ["Cardiology"],
        "availabilities": [
            {"day_of_week": "Tuesday", "start_time": "14:00", "end_time": "19:00"},
            {"day_of_week": "Thursday", "start_time": "14:00", "end_time": "19:00"},
            {"day_of_week": "Saturday", "start_time": "10:00", "end_time": "14:00"}
        ]
    },
    {
        "email": "suresh.nair@test.com",
        "name": "Dr. Suresh Nair",
        "password": "password",
        "description": "MBBS, DM Cardiology. 20 years experience in heart failure management and pacemaker implantation.",
        "role": "Doctor",
        "consultation_price": 2000,
        "specializations": ["Cardiology"],
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "11:00", "end_time": "16:00"},
            {"day_of_week": "Tuesday", "start_time": "11:00", "end_time": "16:00"},
            {"day_of_week": "Thursday", "start_time": "11:00", "end_time": "16:00"},
            {"day_of_week": "Friday", "start_time": "11:00", "end_time": "16:00"}
        ]
    },
    {
        "email": "john.fernandez@test.com",
        "name": "Dr. John Fernandez",
        "password": "password",
        "description": "MBBS, MD. Pediatric cardiologist focusing on congenital heart defects.",
        "role": "Doctor",
        "consultation_price": 1200,
        "specializations": ["Cardiology", "Pediatrics"],
        "availabilities": [
            {"day_of_week": "Wednesday", "start_time": "08:00", "end_time": "12:00"},
            {"day_of_week": "Saturday", "start_time": "08:00", "end_time": "12:00"}
        ]
    },

    # --- Orthopedics ---
    {
        "email": "simran.grewal@test.com",
        "name": "Dr. Simran Grewal",
        "password": "password",
        "description": "MBBS, MS Orthopedics. Sports medicine expert and arthroscopy surgeon.",
        "role": "Doctor",
        "consultation_price": 1200,
        "specializations": ["Orthopedics"],
        # [SPLIT SHIFT]: Tue, Thu
        "availabilities": [
            {"day_of_week": "Tuesday", "start_time": "09:00", "end_time": "12:00"},
            {"day_of_week": "Tuesday", "start_time": "16:00", "end_time": "20:00"},
            {"day_of_week": "Thursday", "start_time": "09:00", "end_time": "12:00"},
            {"day_of_week": "Thursday", "start_time": "16:00", "end_time": "20:00"},
            {"day_of_week": "Saturday", "start_time": "10:00", "end_time": "16:00"}
        ]
    },
    {
        "email": "rohan.mehta@test.com",
        "name": "Dr. Rohan Mehta",
        "password": "password",
        "description": "MBBS, MS Orthopedics. Spine surgeon specializing in minimally invasive spine corrections.",
        "role": "Doctor",
        "consultation_price": 1500,
        "specializations": ["Orthopedics"],
        "availabilities": [
            {"day_of_week": "Friday", "start_time": "09:00", "end_time": "17:00"},
            {"day_of_week": "Saturday", "start_time": "09:00", "end_time": "17:00"},
            {"day_of_week": "Sunday", "start_time": "10:00", "end_time": "14:00"}
        ]
    },
    {
        "email": "manoj.kumar@test.com",
        "name": "Dr. Manoj Kumar",
        "password": "password",
        "description": "MBBS, D-Ortho. Specializes in fracture management and trauma care.",
        "role": "Doctor",
        "consultation_price": 800,
        "specializations": ["Orthopedics"],
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "08:00", "end_time": "14:00"},
            {"day_of_week": "Wednesday", "start_time": "08:00", "end_time": "14:00"},
            {"day_of_week": "Friday", "start_time": "08:00", "end_time": "14:00"}
        ]
    },
    {
        "email": "deepa.seth@test.com",
        "name": "Dr. Deepa Seth",
        "password": "password",
        "description": "MBBS, MS Orthopedics. Pediatric orthopedic surgeon focusing on bone deformities in children.",
        "role": "Doctor",
        "consultation_price": 1000,
        "specializations": ["Orthopedics", "Pediatrics"],
        "availabilities": [
            {"day_of_week": "Thursday", "start_time": "10:00", "end_time": "15:00"},
            {"day_of_week": "Saturday", "start_time": "10:00", "end_time": "15:00"}
        ]
    },

    # --- Gynecology ---
    {
        "email": "priya.sharma@test.com",
        "name": "Dr. Priya Sharma",
        "password": "password",
        "description": "MBBS, MD OBGYN. High-risk pregnancy specialist and infertility consultant.",
        "role": "Doctor",
        "consultation_price": 1000,
        "specializations": ["Gynecology"],
        # [SPLIT SHIFT]: Mon, Wed
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "09:00", "end_time": "12:00"},
            {"day_of_week": "Monday", "start_time": "16:00", "end_time": "19:00"},
            {"day_of_week": "Tuesday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Wednesday", "start_time": "09:00", "end_time": "12:00"},
            {"day_of_week": "Wednesday", "start_time": "16:00", "end_time": "19:00"},
            {"day_of_week": "Thursday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Friday", "start_time": "09:00", "end_time": "13:00"}
        ]
    },
    {
        "email": "ananya.gupta@test.com",
        "name": "Dr. Ananya Gupta",
        "password": "password",
        "description": "MBBS, DGO. Focus on adolescent health, PCOD/PCOS, and menopause management.",
        "role": "Doctor",
        "consultation_price": 700,
        "specializations": ["Gynecology"],
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "15:00", "end_time": "19:00"},
            {"day_of_week": "Wednesday", "start_time": "15:00", "end_time": "19:00"},
            {"day_of_week": "Friday", "start_time": "15:00", "end_time": "19:00"}
        ]
    },
    {
        "email": "sarah.thomas@test.com",
        "name": "Dr. Sarah Thomas",
        "password": "password",
        "description": "MBBS, MS OBGYN. Expert in laparoscopic hysterectomy and fibroid removal.",
        "role": "Doctor",
        "consultation_price": 1200,
        "specializations": ["Gynecology"],
        "availabilities": [
            {"day_of_week": "Tuesday", "start_time": "10:00", "end_time": "16:00"},
            {"day_of_week": "Thursday", "start_time": "10:00", "end_time": "16:00"}
        ]
    },
    {
        "email": "laxmi.patil@test.com",
        "name": "Dr. Laxmi Patil",
        "password": "password",
        "description": "MBBS, MD. IVF specialist and reproductive endocrinologist.",
        "role": "Doctor",
        "consultation_price": 2000,
        "specializations": ["Gynecology", "Endocrinology"],
        "availabilities": [
            {"day_of_week": "Saturday", "start_time": "09:00", "end_time": "15:00"},
            {"day_of_week": "Sunday", "start_time": "09:00", "end_time": "13:00"}
        ]
    },

    # --- Pediatrics ---
    {
        "email": "vikram.bajwa@test.com",
        "name": "Dr. Vikram Bajwa",
        "password": "password",
        "description": "MBBS, MD Pediatrics. Neonatologist and child nutrition expert.",
        "role": "Doctor",
        "consultation_price": 1000,
        "specializations": ["Pediatrics"],
        # [SPLIT SHIFT]: Mon, Fri
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "08:00", "end_time": "11:00"},
            {"day_of_week": "Monday", "start_time": "17:00", "end_time": "20:00"},
            {"day_of_week": "Wednesday", "start_time": "08:00", "end_time": "12:00"},
            {"day_of_week": "Friday", "start_time": "08:00", "end_time": "11:00"},
            {"day_of_week": "Friday", "start_time": "17:00", "end_time": "20:00"},
            {"day_of_week": "Saturday", "start_time": "09:00", "end_time": "13:00"}
        ]
    },
    {
        "email": "kabir.sandhu@test.com",
        "name": "Dr. Kabir Sandhu",
        "password": "password",
        "description": "MBBS, MD Pediatrics. Adolescent health specialist.",
        "role": "Doctor",
        "consultation_price": 800,
        "specializations": ["Pediatrics"],
        "availabilities": [
            {"day_of_week": "Thursday", "start_time": "12:00", "end_time": "18:00"},
            {"day_of_week": "Friday", "start_time": "12:00", "end_time": "18:00"},
            {"day_of_week": "Saturday", "start_time": "12:00", "end_time": "18:00"}
        ]
    },
    {
        "email": "pooja.malhotra@test.com",
        "name": "Dr. Pooja Malhotra",
        "password": "password",
        "description": "MBBS, DCH. General pediatrician with a friendly approach to vaccination and growth monitoring.",
        "role": "Doctor",
        "consultation_price": 600,
        "specializations": ["Pediatrics"],
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "16:00", "end_time": "20:00"},
            {"day_of_week": "Tuesday", "start_time": "16:00", "end_time": "20:00"},
            {"day_of_week": "Wednesday", "start_time": "16:00", "end_time": "20:00"}
        ]
    },

    # --- Dermatology ---
    {
        "email": "aisha.khan@test.com",
        "name": "Dr. Aisha Khan",
        "password": "password",
        "description": "MBBS, MD Dermatology. Clinical dermatologist specializing in acne, eczema, and psoriasis.",
        "role": "Doctor",
        "consultation_price": 900,
        "specializations": ["Dermatology"],
        # [SPLIT SHIFT]: Wed
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "10:00", "end_time": "14:00"},
            {"day_of_week": "Wednesday", "start_time": "10:00", "end_time": "13:00"},
            {"day_of_week": "Wednesday", "start_time": "17:00", "end_time": "20:00"},
            {"day_of_week": "Friday", "start_time": "10:00", "end_time": "14:00"}
        ]
    },
    {
        "email": "raj.kumar@test.com",
        "name": "Dr. Raj Kumar",
        "password": "password",
        "description": "MBBS, DDVL. Aesthetic dermatologist expert in laser treatments and anti-aging.",
        "role": "Doctor",
        "consultation_price": 1500,
        "specializations": ["Dermatology"],
        "availabilities": [
            {"day_of_week": "Tuesday", "start_time": "11:00", "end_time": "19:00"},
            {"day_of_week": "Thursday", "start_time": "11:00", "end_time": "19:00"}
        ]
    },
    {
        "email": "sara.lee@test.com",
        "name": "Dr. Sara Lee",
        "password": "password",
        "description": "MBBS, MD. Pediatric dermatologist.",
        "role": "Doctor",
        "consultation_price": 900,
        "specializations": ["Dermatology", "Pediatrics"],
        "availabilities": [
            {"day_of_week": "Saturday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Sunday", "start_time": "10:00", "end_time": "13:00"}
        ]
    },

    # --- Neurology ---
    {
        "email": "vikas.dubey@test.com",
        "name": "Dr. Vikas Dubey",
        "password": "password",
        "description": "MBBS, DM Neurology. Stroke specialist and expert in managing migraines and epilepsy.",
        "role": "Doctor",
        "consultation_price": 1500,
        "specializations": ["Neurology"],
        # [SPLIT SHIFT]: Mon
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "09:00", "end_time": "12:00"},
            {"day_of_week": "Monday", "start_time": "16:00", "end_time": "19:00"},
            {"day_of_week": "Wednesday", "start_time": "09:00", "end_time": "17:00"}
        ]
    },
    {
        "email": "anil.sharma@test.com",
        "name": "Dr. Anil Sharma",
        "password": "password",
        "description": "MBBS, MCh Neurosurgery. Spine and brain surgeon.",
        "role": "Doctor",
        "consultation_price": 2000,
        "specializations": ["Neurology", "Orthopedics"],
        "availabilities": [
            {"day_of_week": "Thursday", "start_time": "14:00", "end_time": "20:00"},
            {"day_of_week": "Friday", "start_time": "14:00", "end_time": "20:00"}
        ]
    },

    # --- Psychiatry ---
    {
        "email": "mira.desai@test.com",
        "name": "Dr. Mira Desai",
        "password": "password",
        "description": "MBBS, MD Psychiatry. Specializes in anxiety, depression, and cognitive behavioral therapy.",
        "role": "Doctor",
        "consultation_price": 1200,
        "specializations": ["Psychiatry"],
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "15:00", "end_time": "20:00"},
            {"day_of_week": "Wednesday", "start_time": "15:00", "end_time": "20:00"},
            {"day_of_week": "Friday", "start_time": "15:00", "end_time": "20:00"}
        ]
    },
    {
        "email": "karan.johar@test.com",
        "name": "Dr. Karan Johar",
        "password": "password",
        "description": "MBBS, DPM. Child psychiatrist focusing on ADHD and autism spectrum disorders.",
        "role": "Doctor",
        "consultation_price": 1500,
        "specializations": ["Psychiatry", "Pediatrics"],
        "availabilities": [
            {"day_of_week": "Saturday", "start_time": "10:00", "end_time": "16:00"},
            {"day_of_week": "Sunday", "start_time": "10:00", "end_time": "14:00"}
        ]
    },
    {
        "email": "reena.roy@test.com",
        "name": "Dr. Reena Roy",
        "password": "password",
        "description": "MBBS, MD. Addiction psychiatrist helping patients with de-addiction and rehabilitation.",
        "role": "Doctor",
        "consultation_price": 1000,
        "specializations": ["Psychiatry"],
        "availabilities": [
            {"day_of_week": "Tuesday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Thursday", "start_time": "09:00", "end_time": "13:00"}
        ]
    },

    # --- ENT ---
    {
        "email": "sumit.bose@test.com",
        "name": "Dr. Sumit Bose",
        "password": "password",
        "description": "MBBS, MS ENT. Specialist in endoscopic sinus surgery and hearing disorders.",
        "role": "Doctor",
        "consultation_price": 900,
        "specializations": ["ENT (Otorhinolaryngology)"],
        # [SPLIT SHIFT]: Mon, Wed
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "10:00", "end_time": "13:00"},
            {"day_of_week": "Monday", "start_time": "16:00", "end_time": "19:00"},
            {"day_of_week": "Wednesday", "start_time": "10:00", "end_time": "13:00"},
            {"day_of_week": "Wednesday", "start_time": "16:00", "end_time": "19:00"}
        ]
    },
    {
        "email": "tina.dutta@test.com",
        "name": "Dr. Tina Dutta",
        "password": "password",
        "description": "MBBS, DLO. Pediatric ENT specialist.",
        "role": "Doctor",
        "consultation_price": 800,
        "specializations": ["ENT (Otorhinolaryngology)", "Pediatrics"],
        "availabilities": [
            {"day_of_week": "Tuesday", "start_time": "15:00", "end_time": "19:00"},
            {"day_of_week": "Friday", "start_time": "15:00", "end_time": "19:00"}
        ]
    },
    {
        "email": "ravi.shastri@test.com",
        "name": "Dr. Ravi Shastri",
        "password": "password",
        "description": "MBBS, MS ENT. Head and neck surgeon.",
        "role": "Doctor",
        "consultation_price": 1200,
        "specializations": ["ENT (Otorhinolaryngology)"],
        "availabilities": [
            {"day_of_week": "Thursday", "start_time": "09:00", "end_time": "14:00"},
            {"day_of_week": "Saturday", "start_time": "09:00", "end_time": "14:00"}
        ]
    },

    # --- Ophthalmology ---
    {
        "email": "naina.sahni@test.com",
        "name": "Dr. Naina Sahni",
        "password": "password",
        "description": "MBBS, MS Ophthalmology. Cataract and Lasik surgeon.",
        "role": "Doctor",
        "consultation_price": 800,
        "specializations": ["Ophthalmology"],
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Tuesday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Wednesday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Thursday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Friday", "start_time": "09:00", "end_time": "13:00"}
        ]
    },
    {
        "email": "arun.rao@test.com",
        "name": "Dr. Arun Rao",
        "password": "password",
        "description": "MBBS, MD. Retina specialist.",
        "role": "Doctor",
        "consultation_price": 1200,
        "specializations": ["Ophthalmology"],
        "availabilities": [
            {"day_of_week": "Saturday", "start_time": "10:00", "end_time": "15:00"},
            {"day_of_week": "Sunday", "start_time": "10:00", "end_time": "13:00"}
        ]
    },

    # --- Gastroenterology ---
    {
        "email": "huma.qureshi@test.com",
        "name": "Dr. Huma Qureshi",
        "password": "password",
        "description": "MBBS, DM Gastroenterology. Expert in liver diseases and endoscopy.",
        "role": "Doctor",
        "consultation_price": 1500,
        "specializations": ["Gastroenterology"],
        # [SPLIT SHIFT]: Mon, Thu
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "11:00", "end_time": "14:00"},
            {"day_of_week": "Monday", "start_time": "17:00", "end_time": "20:00"},
            {"day_of_week": "Thursday", "start_time": "11:00", "end_time": "14:00"},
            {"day_of_week": "Thursday", "start_time": "17:00", "end_time": "20:00"}
        ]
    },
    {
        "email": "vijay.mallya@test.com",
        "name": "Dr. Vijay Mallya",
        "password": "password",
        "description": "MBBS, DNB Gastro. Specialist in digestive disorders and IBS.",
        "role": "Doctor",
        "consultation_price": 1000,
        "specializations": ["Gastroenterology"],
        "availabilities": [
            {"day_of_week": "Tuesday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Friday", "start_time": "09:00", "end_time": "13:00"}
        ]
    },

    # --- Pulmonology ---
    {
        "email": "ishaan.khattar@test.com",
        "name": "Dr. Ishaan Khattar",
        "password": "password",
        "description": "MBBS, MD Respiratory Medicine. Asthma and COPD specialist.",
        "role": "Doctor",
        "consultation_price": 1000,
        "specializations": ["Pulmonology"],
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "14:00", "end_time": "19:00"},
            {"day_of_week": "Wednesday", "start_time": "14:00", "end_time": "19:00"},
            {"day_of_week": "Friday", "start_time": "14:00", "end_time": "19:00"}
        ]
    },

    # --- Urology ---
    {
        "email": "sameer.khan@test.com",
        "name": "Dr. Sameer Khan",
        "password": "password",
        "description": "MBBS, MCh Urology. Kidney stone and prostate specialist.",
        "role": "Doctor",
        "consultation_price": 1500,
        "specializations": ["Urology"],
        # [SPLIT SHIFT]: Tue, Thu
        "availabilities": [
            {"day_of_week": "Tuesday", "start_time": "10:00", "end_time": "13:00"},
            {"day_of_week": "Tuesday", "start_time": "16:00", "end_time": "19:00"},
            {"day_of_week": "Thursday", "start_time": "10:00", "end_time": "13:00"},
            {"day_of_week": "Thursday", "start_time": "16:00", "end_time": "19:00"}
        ]
    },
    {
        "email": "kartik.aryan@test.com",
        "name": "Dr. Kartik Aryan",
        "password": "password",
        "description": "MBBS, DNB Urology. Male infertility specialist.",
        "role": "Doctor",
        "consultation_price": 1200,
        "specializations": ["Urology"],
        "availabilities": [
            {"day_of_week": "Saturday", "start_time": "09:00", "end_time": "14:00"}
        ]
    },

    # --- Endocrinology ---
    {
        "email": "sonam.kapoor@test.com",
        "name": "Dr. Sonam Kapoor",
        "password": "password",
        "description": "MBBS, DM Endocrinology. Thyroid and Diabetes expert.",
        "role": "Doctor",
        "consultation_price": 1500,
        "specializations": ["Endocrinology"],
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Wednesday", "start_time": "09:00", "end_time": "13:00"},
            {"day_of_week": "Friday", "start_time": "09:00", "end_time": "13:00"}
        ]
    },
    {
        "email": "deepak.chopra@test.com",
        "name": "Dr. Deepak Chopra",
        "password": "password",
        "description": "MBBS, MD. Hormonal imbalance specialist.",
        "role": "Doctor",
        "consultation_price": 1000,
        "specializations": ["Endocrinology"],
        "availabilities": [
            {"day_of_week": "Tuesday", "start_time": "15:00", "end_time": "19:00"},
            {"day_of_week": "Thursday", "start_time": "15:00", "end_time": "19:00"}
        ]
    },

    # --- Oncology ---
    {
        "email": "anand.ahuja@test.com",
        "name": "Dr. Anand Ahuja",
        "password": "password",
        "description": "MBBS, DM Medical Oncology. Chemotherapy specialist.",
        "role": "Doctor",
        "consultation_price": 1800,
        "specializations": ["Oncology"],
        "availabilities": [
            {"day_of_week": "Monday", "start_time": "10:00", "end_time": "16:00"},
            {"day_of_week": "Thursday", "start_time": "10:00", "end_time": "16:00"}
        ]
    },
    {
        "email": "lisa.ray@test.com",
        "name": "Dr. Lisa Ray",
        "password": "password",
        "description": "MBBS, MCh Surgical Oncology. Cancer surgeon.",
        "role": "Doctor",
        "consultation_price": 2000,
        "specializations": ["Oncology"],
        "availabilities": [
            {"day_of_week": "Tuesday", "start_time": "09:00", "end_time": "15:00"},
            {"day_of_week": "Friday", "start_time": "09:00", "end_time": "15:00"}
        ]
    }
]

patients = [
    {
        "name": "Parth Garg",
        "gender": "male",
        "email": "parth.garg@test.com",
        "age": 35,
        "password": "password"
    },
    {
        "name": "Aarav Sharma",
        "gender": "male",
        "email": "aarav.sharma@test.com",
        "age": 28,
        "password": "password"
    },
    {
        "name": "Diya Patel",
        "gender": "female",
        "email": "diya.patel@test.com",
        "age": 42,
        "password": "password"
    },
    {
        "name": "Vihaan Singh",
        "gender": "male",
        "email": "vihaan.singh@test.com",
        "age": 8,
        "password": "password"
    },
    {
        "name": "Ananya Roy",
        "gender": "female",
        "email": "ananya.roy@test.com",
        "age": 25,
        "password": "password"
    },
    {
        "name": "Ishaan Gupta",
        "gender": "male",
        "email": "ishaan.gupta@test.com",
        "age": 50,
        "password": "password"
    },
    {
        "name": "Saanvi Kumar",
        "gender": "female",
        "email": "saanvi.kumar@test.com",
        "age": 65,
        "password": "password"
    },
    {
        "name": "Reyansh Malhotra",
        "gender": "male",
        "email": "reyansh.malhotra@test.com",
        "age": 32,
        "password": "password"
    },
    {
        "name": "Zara Khan",
        "gender": "female",
        "email": "zara.khan@test.com",
        "age": 19,
        "password": "password"
    },
    {
        "name": "Kabir Joshi",
        "gender": "male",
        "email": "kabir.joshi@test.com",
        "age": 45,
        "password": "password"
    },
    {
        "name": "Myra Singh",
        "gender": "female",
        "email": "myra.singh@test.com",
        "age": 5,
        "password": "password"
    },
    {
        "name": "Arjun Verma",
        "gender": "male",
        "email": "arjun.verma@test.com",
        "age": 29,
        "password": "password"
    },
    {
        "name": "Priya Reddy",
        "gender": "female",
        "email": "priya.reddy@test.com",
        "age": 38,
        "password": "password"
    },
    {
        "name": "Vivaan Mehta",
        "gender": "male",
        "email": "vivaan.mehta@test.com",
        "age": 12,
        "password": "password"
    },
    {
        "name": "Aadhya Nair",
        "gender": "female",
        "email": "aadhya.nair@test.com",
        "age": 55,
        "password": "password"
    },
    {
        "name": "Mohammed Ali",
        "gender": "male",
        "email": "mohammed.ali@test.com",
        "age": 40,
        "password": "password"
    },
    {
        "name": "Riya Kapoor",
        "gender": "female",
        "email": "riya.kapoor@test.com",
        "age": 27,
        "password": "password"
    },
    {
        "name": "Advait Chopra",
        "gender": "male",
        "email": "advait.chopra@test.com",
        "age": 70,
        "password": "password"
    },
    {
        "name": "Kiara Agarwal",
        "gender": "female",
        "email": "kiara.agarwal@test.com",
        "age": 31,
        "password": "password"
    },
    {
        "name": "Dhruv Saxena",
        "gender": "male",
        "email": "dhruv.saxena@test.com",
        "age": 22,
        "password": "password"
    },
    {
        "name": "Fatima Khan",
        "gender": "female",
        "email": "fatima.khan@test.com",
        "age": 48,
        "password": "password"
    },
    {
        "name": "Aryan Mishra",
        "gender": "male",
        "email": "aryan.mishra@test.com",
        "age": 36,
        "password": "password"
    },
    {
        "name": "Siya Kaur",
        "gender": "female",
        "email": "siya.kaur@test.com",
        "age": 60,
        "password": "password"
    },
    {
        "name": "Ayaan Bhat",
        "gender": "male",
        "email": "ayaan.bhat@test.com",
        "age": 9,
        "password": "password"
    },
    {
        "name": "Neha Das",
        "gender": "female",
        "email": "neha.das@test.com",
        "age": 33,
        "password": "password"
    },
    {
        "name": "Rohan Yadav",
        "gender": "male",
        "email": "rohan.yadav@test.com",
        "age": 26,
        "password": "password"
    },
    {
        "name": "Isha Jain",
        "gender": "female",
        "email": "isha.jain@test.com",
        "age": 24,
        "password": "password"
    },
    {
        "name": "Krishna Iyer",
        "gender": "male",
        "email": "krishna.iyer@test.com",
        "age": 52,
        "password": "password"
    },
    {
        "name": "Meera Rao",
        "gender": "female",
        "email": "meera.rao@test.com",
        "age": 29,
        "password": "password"
    },
    {
        "name": "Rahul Choudhury",
        "gender": "male",
        "email": "rahul.choudhury@test.com",
        "age": 41,
        "password": "password"
    }
]

def create_initial_data():
    # Create roles
    for name in roles:
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name))
    db.session.commit()

    # Create users
    for user_data in basic_users:
        if User.query.filter_by(email=user_data["email"]).first():
            continue

        user = User(
            email=user_data["email"],
            password=hash_password(user_data["password"])
        )

        role = Role.query.filter_by(name=user_data["role"]).first()
        user.roles.append(role)

        db.session.add(user)

    db.session.commit()

    # Create specializations
    for s in specializations:
        if not Specialization.query.filter_by(name=s).first():
            specialization = Specialization(name=s)
            db.session.add(specialization)
    db.session.commit()

    for d in doctors:
        if User.query.filter_by(email=d["email"]).first():
            continue

        user = User(email=d["email"], password=hash_password(d["password"]))
        doctor_role = Role.query.filter_by(name="Doctor").first()
        user.roles.append(doctor_role)
        doctor = DoctorProfile(name=d["name"], description=d["description"], consultation_price=d["consultation_price"], user=user)
        for s in d["specializations"]:
            doctor.specializations.append(Specialization.query.filter_by(name=s).first())
        for a in d["availabilities"]:
            s_time = datetime.strptime(a["start_time"], "%H:%M").time()
            e_time = datetime.strptime(a["end_time"], "%H:%M").time()
            availability = DoctorAvailability(doctor=doctor, day_of_week=a["day_of_week"], start_time=s_time, end_time=e_time)
            doctor.availabilities.append(availability)
        db.session.add_all([user, doctor])
    
    for p in patients:
        if User.query.filter_by(email=p["email"]).first():
            continue
        p_user = User(email=p["email"], password=hash_password(p["password"]))
        patient = PatientProfile(name=p["name"], gender=p["gender"], age=p["age"], user=p_user)
        p_user.roles.append(Role.query.filter_by(name="Patient").first())
        db.session.add_all([p_user, patient])
    db.session.commit()