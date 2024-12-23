import random
from faker import Faker
import mysql.connector

# Initializing Faker
def generate_data():
    fake = Faker()

    # Connecting to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="university"
    )

    cursor = connection.cursor()

    # Generating Departments
    departments = [
        ("Computer Science", "Science", "csdept@university.edu"),
        ("Business", "Management", "businessdept@university.edu"),
        ("Engineering", "Science", "engineeringdept@university.edu"),
    ]
    cursor.executemany("INSERT INTO Departments (name, faculty, contact_info) VALUES (%s, %s, %s)", departments)

    # Commiting departments insertions and retrieve department ids
    connection.commit()
    cursor.execute("SELECT department_id FROM Departments")
    department_ids = [row[0] for row in cursor.fetchall()]

    # Generating Students
    students = []

    
    #Since Email is the primary key we are ensuring that there is no duplicate emails generated from using Faker
    sunique_emails = set()
    while len(sunique_emails) < 20000:
        sunique_emails.add(fake.email())
        
    semail = list(sunique_emails)
    sid = list(range(1, 1001))

    for i in range(1000):
        students.append((
            sid[i],
            fake.name(),
            semail[i],
            random.choice(department_ids),  # Using a valid department_id from the inserted departments
            fake.job(),
            round(random.uniform(2.0, 4.0), 2),
            ", ".join(fake.words(nb=3)),
            random.choice(["Student", "Alumni"]),
        ))
    cursor.executemany("""
        INSERT INTO Students (student_id, name, email, department_id, major, gpa, interests, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, students)

    # Generating Recruiters

    #We are ensuring that there is no duplicate emails generated from using Faker
    runique_emails = set()
    while len(runique_emails) < 20000:
        runique_emails.add(fake.email())
        
    remail = list(runique_emails)
    rid = list(range(1, 101))  # Ensuring recruiter_id starts from 1 and has 100 recruiters

    recruiters = []
    for i in range(100):
        phone = fake.phone_number()
        phone_digits = ''.join(filter(str.isdigit, phone))
        phone = int(phone_digits[:15])
        recruiters.append((
            rid[i],
            fake.name(),
            fake.company(),
            remail[i],
            phone,
            random.choice([True, False])
        ))
    cursor.executemany("""
        INSERT INTO Recruiters (recruiter_id, name, company, email, phone, current_company)
        VALUES (%s,%s, %s, %s, %s, %s)
    """, recruiters)

    # Commiting recruiters insertions and retrieve recruiter ids
    connection.commit()
    cursor.execute("SELECT recruiter_id FROM Recruiters")
    recruiter_ids = [row[0] for row in cursor.fetchall()]

    # Generating Jobs
    jobs = []
    for i in range(1000):
        jobs.append((
            fake.job(),
            fake.text(max_nb_chars=200),
            random.choice(recruiter_ids),  # Using a valid recruiter_id from the inserted recruiters
            random.choice(department_ids),  # Using a valid department_id from the inserted departments
            random.choice(["Toronto", "Vancouver", "Montreal", "Calgary", "Remote"]),
            fake.date_between(start_date="-1y", end_date="today"),
            fake.date_between(start_date="today", end_date="+1y"),
        ))
    cursor.executemany("""
        INSERT INTO Jobs (job_title, job_description, recruiter_id, department_id, location, posting_date, closing_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, jobs)

    # Generating University Staff
    staff = []
    for _ in range(50):
        staff.append((
            fake.name(),
            random.choice(["Department Head", "Career Advisor", "System Administrator"]),
            random.choice(department_ids),  # Using a valid department_id from the inserted departments
            fake.email(),
            ", ".join(fake.words(nb=5))
        ))
    cursor.executemany("""
        INSERT INTO University_Staff (name, role, department_id, email, permissions)
        VALUES (%s, %s, %s, %s, %s)
    """, staff)

    # Commiting changes and closing the connection
    connection.commit()
    cursor.close()
    connection.close()

    print("Data generation complete!")

if __name__ == "__main__":
    generate_data()
