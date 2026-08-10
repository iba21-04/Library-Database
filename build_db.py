# build_db.py

import sqlite3
import os

DB_PATH = "library.db"
SCHEMA_PATH = "schema.sql"

# SETUP
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

con = sqlite3.connect(DB_PATH)
con.execute("PRAGMA foreign_keys = ON;")
con.executescript(open(SCHEMA_PATH).read())
cur = con.cursor()

# PUBLISHER
publishers = [
    ("Penguin Random House", "1745 Broadway, New York, NY", "212-555-0100"),
    ("HarperCollins", "195 Broadway, New York, NY", "212-555-0101"),
    ("Simon & Schuster", "1230 Ave of Americas, NY", "212-555-0102"),
    ("Macmillan Publishers", "120 Broadway, New York, NY", "646-555-0103"),
    ("Oxford University Press", "198 Madison Ave, NY", "212-555-0104"),
    ("Elsevier", "1600 John F Kennedy Blvd, Philadelphia, PA", "215-555-0105"),
    ("Conde Nast", "1 World Trade Center, NY", "212-555-0106"),
    ("Nature Publishing Group", "1 New York Plaza, NY", "212-555-0107"),
    ("Blue Note Records", "902 Broadway, New York, NY", "212-555-0108"),
    ("Vertigo Press", "44 King St, Toronto, ON", "416-555-0109"),
]
cur.executemany(
    "INSERT INTO PUBLISHER (Name, Address, Phone) VALUES (?, ?, ?)", publishers
)
con.commit()

# AUTHOR
authors = [
    ("Haruki", "Murakami", "Japanese novelist known for surrealist fiction."),
    ("Isabel", "Allende", "Chilean-American writer of magical realism."),
    ("Yuval Noah", "Harari", "Historian and author of Sapiens."),
    ("Andy", "Weir", "Science fiction author known for The Martian."),
    ("Chimamanda Ngozi", "Adichie", "Nigerian novelist and essayist."),
    ("Malcolm", "Gladwell", "Journalist and non-fiction author."),
    ("Ursula K.", "Le Guin", "Author of speculative fiction."),
    ("Neil", "deGrasse Tyson", "Astrophysicist and science communicator."),
    ("Delia", "Owens", "Author of Where the Crawdads Sing."),
    ("Kazuo", "Ishiguro", "Nobel laureate novelist."),
    ("Brene", "Brown", "Researcher and author on vulnerability."),
    ("Liu", "Cixin", "Chinese science fiction author."),
]
cur.executemany(
    "INSERT INTO AUTHOR (FirstName, LastName, Bio) VALUES (?, ?, ?)", authors
)
con.commit()

# ITEM
# (Title, ItemType, PublisherID, PublicationYear, Genre, Language)
items = [
    ("Kafka on the Shore", "PRINT_BOOK", 1, 2002, "Fiction", "English"),
    ("The House of the Spirits", "PRINT_BOOK", 2, 1982, "Fiction", "English"),
    ("Sapiens: A Brief History of Humankind", "ONLINE_BOOK", 3, 2011, "Non-fiction", "English"),
    ("Project Hail Mary", "PRINT_BOOK", 4, 2021, "Science Fiction", "English"),
    ("Americanah", "ONLINE_BOOK", 1, 2013, "Fiction", "English"),
    ("Outliers", "PRINT_BOOK", 2, 2008, "Non-fiction", "English"),
    ("Educated: A Memoir", "PRINT_BOOK", 3, 2018, "Memoir", "English"),
    ("Becoming", "PRINT_BOOK", 2, 2018, "Memoir", "English"),
    ("The Night Circus", "PRINT_BOOK", 4, 2011, "Fantasy", "English"),
    ("The Anthropocene Reviewed", "ONLINE_BOOK", 10, 2021, "Essays", "English"),
    ("Braiding Sweetgrass", "ONLINE_BOOK", 5, 2013, "Nature", "English"),
    ("Atomic Habits", "ONLINE_BOOK", 1, 2018, "Self-help", "English"),
    ("Thinking, Fast and Slow", "ONLINE_BOOK", 4, 2011, "Psychology", "English"),
    ("A Brief History of Time", "ONLINE_BOOK", 2, 1988, "Science", "English"),
    ("National Geographic", "MAGAZINE", 7, 2026, "Science", "English"),
    ("TIME Magazine", "MAGAZINE", 7, 2026, "News", "English"),
    ("Wired", "MAGAZINE", 7, 2026, "Technology", "English"),
    ("The Economist", "MAGAZINE", 4, 2026, "News", "English"),
    ("Scientific American", "MAGAZINE", 8, 2026, "Science", "English"),
    ("Rolling Stone", "MAGAZINE", 9, 2026, "Music", "English"),
    ("National Geographic - May", "MAGAZINE", 7, 2026, "Science", "English"),
    ("TIME Magazine - May", "MAGAZINE", 7, 2026, "News", "English"),
    ("Nature", "JOURNAL", 8, 2026, "Science", "English"),
    ("The Lancet", "JOURNAL", 6, 2026, "Medicine", "English"),
    ("Cell", "JOURNAL", 6, 2026, "Biology", "English"),
    ("Journal of the ACM", "JOURNAL", 5, 2026, "Computer Science", "English"),
    ("The New England Journal of Medicine", "JOURNAL", 6, 2026, "Medicine", "English"),
    ("Journal of Applied Psychology", "JOURNAL", 5, 2026, "Psychology", "English"),
    ("Physical Review Letters", "JOURNAL", 8, 2026, "Physics", "English"),
    ("Journal of Financial Economics", "JOURNAL", 6, 2026, "Economics", "English"),
    ("Kind of Blue", "RECORD", 9, 1959, "Jazz", "Instrumental"),
    ("A Love Supreme", "RECORD", 9, 1965, "Jazz", "Instrumental"),
    ("Blue Train", "RECORD", 9, 1957, "Jazz", "Instrumental"),
    ("Random Access Memories", "RECORD", 9, 2013, "Electronic", "Instrumental"),
    ("Rumours", "RECORD", 9, 1977, "Rock", "English"),
    ("Abbey Road", "RECORD", 9, 1969, "Rock", "English"),
    ("Time Out", "RECORD", 9, 1959, "Jazz", "Instrumental"),
    ("Songs in the Key of Life", "RECORD", 9, 1976, "Soul", "English"),
    ("Nevermind", "RECORD", 9, 1991, "Rock", "English"),
    ("Thriller", "RECORD", 9, 1982, "Pop", "English"),
    # --- additional PRINT_BOOK items ---
    ("The Remains of the Day", "PRINT_BOOK", 2, 1989, "Fiction", "English"),
    ("Where the Crawdads Sing", "PRINT_BOOK", 1, 2018, "Fiction", "English"),
    ("The Left Hand of Darkness", "PRINT_BOOK", 5, 1969, "Science Fiction", "English"),
    # --- additional ONLINE_BOOK items ---
    ("The Midnight Library", "ONLINE_BOOK", 4, 2020, "Fiction", "English"),
    ("Cosmos", "ONLINE_BOOK", 5, 1980, "Science", "English"),
    ("Man's Search for Meaning", "ONLINE_BOOK", 3, 1946, "Psychology", "English"),
    # --- additional MAGAZINE items ---
    ("Wired - May", "MAGAZINE", 7, 2026, "Technology", "English"),
    ("National Geographic - April", "MAGAZINE", 7, 2026, "Science", "English"),
    # --- additional JOURNAL items ---
    ("Journal of Marketing Research", "JOURNAL", 5, 2026, "Business", "English"),
    ("IEEE Transactions on Software Engineering", "JOURNAL", 5, 2026, "Computer Science", "English"),
]
cur.executemany(
    "INSERT INTO ITEM (Title, ItemType, PublisherID, PublicationYear, Genre, Language) "
    "VALUES (?, ?, ?, ?, ?, ?)",
    items,
)
con.commit()

# Look up ItemIDs by title so subclass/copy inserts always line up correctly
item_id = {}
for row in cur.execute("SELECT ItemID, Title FROM ITEM").fetchall():
    item_id.setdefault(row[1], row[0])  # first match if titles repeat

# ISA subclasses
print_books = [
    ("Kafka on the Shore", 480, "Fiction-M"),
    ("The House of the Spirits", 448, "Fiction-A"),
    ("Project Hail Mary", 496, "SciFi-W"),
    ("Outliers", 320, "NonFic-G"),
    ("Educated: A Memoir", 352, "NonFic-E"),
    ("Becoming", 448, "NonFic-B"),
    ("The Night Circus", 400, "Fantasy-N"),
    ("The Remains of the Day", 245, "Fiction-I"),
    ("Where the Crawdads Sing", 384, "Fiction-O"),
    ("The Left Hand of Darkness", 304, "SciFi-L"),
]
cur.executemany(
    "INSERT INTO PRINT_BOOK (ItemID, PageCount, ShelfCategory) VALUES (?, ?, ?)",
    [(item_id[t], p, s) for (t, p, s) in print_books],
)

online_books = [
    ("Sapiens: A Brief History of Humankind", "EPUB", 4.2, 3),
    ("Americanah", "EPUB", 3.8, 2),
    ("The Anthropocene Reviewed", "EPUB", 2.9, 2),
    ("Braiding Sweetgrass", "EPUB", 5.1, 2),
    ("Atomic Habits", "EPUB", 3.3, 3),
    ("Thinking, Fast and Slow", "EPUB", 4.6, 2),
    ("A Brief History of Time", "PDF", 6.2, 2),
    ("The Midnight Library", "EPUB", 3.1, 3),
    ("Cosmos", "PDF", 12.5, 2),
    ("Man's Search for Meaning", "EPUB", 2.4, 3),
]
cur.executemany(
    "INSERT INTO ONLINE_BOOK (ItemID, FileFormat, FileSizeMB, ConcurrentLicenses) VALUES (?, ?, ?, ?)",
    [(item_id[t], f, s, c) for (t, f, s, c) in online_books],
)

magazines = [
    ("National Geographic", "Vol 249 No 6", "MONTHLY"),
    ("TIME Magazine", "Vol 207 No 22", "WEEKLY"),
    ("Wired", "Vol 34 No 6", "MONTHLY"),
    ("The Economist", "Vol 449 No 6", "WEEKLY"),
    ("Scientific American", "Vol 335 No 6", "MONTHLY"),
    ("Rolling Stone", "Issue 1420", "MONTHLY"),
    ("National Geographic - May", "Vol 249 No 5", "MONTHLY"),
    ("TIME Magazine - May", "Vol 207 No 21", "WEEKLY"),
    ("Wired - May", "Vol 34 No 5", "MONTHLY"),
    ("National Geographic - April", "Vol 249 No 4", "MONTHLY"),
]
cur.executemany(
    "INSERT INTO MAGAZINE (ItemID, IssueNumber, Frequency) VALUES (?, ?, ?)",
    [(item_id[t], i, f) for (t, i, f) in magazines],
)

journals = [
    ("Nature", 612, 7955, 1),
    ("The Lancet", 405, 10480, 1),
    ("Cell", 187, 940, 1),
    ("Journal of the ACM", 73, 4, 1),
    ("The New England Journal of Medicine", 394, 26, 1),
    ("Journal of Applied Psychology", 111, 6, 1),
    ("Physical Review Letters", 136, 24, 1),
    ("Journal of Financial Economics", 150, 3, 1),
    ("Journal of Marketing Research", 63, 2, 1),
    ("IEEE Transactions on Software Engineering", 52, 6, 1),
]
cur.executemany(
    "INSERT INTO JOURNAL (ItemID, Volume, IssueNumber, PeerReviewed) VALUES (?, ?, ?, ?)",
    [(item_id[t], v, i, p) for (t, v, i, p) in journals],
)

records = [
    ("Kind of Blue", "VINYL", 45),
    ("A Love Supreme", "VINYL", 33),
    ("Blue Train", "VINYL", 42),
    ("Random Access Memories", "CD", 74),
    ("Rumours", "VINYL", 39),
    ("Abbey Road", "VINYL", 47),
    ("Time Out", "VINYL", 42),
    ("Songs in the Key of Life", "VINYL", 85),
    ("Nevermind", "CD", 49),
    ("Thriller", "VINYL", 42),
]
cur.executemany(
    "INSERT INTO RECORD (ItemID, MediaFormat, DurationMinutes) VALUES (?, ?, ?)",
    [(item_id[t], f, d) for (t, f, d) in records],
)
con.commit()

# ITEM_AUTHOR
item_author_pairs = [
    ("Kafka on the Shore", "Murakami"), ("The House of the Spirits", "Allende"),
    ("Sapiens: A Brief History of Humankind", "Harari"), ("Project Hail Mary", "Weir"),
    ("Americanah", "Adichie"), ("Outliers", "Gladwell"),
    ("Kind of Blue", "Le Guin"),  # (fictional crossover credit for demo variety)
    ("A Brief History of Time", "deGrasse Tyson"), ("The Night Circus", "Ishiguro"),
    ("Educated: A Memoir", "Owens"), ("Sapiens: A Brief History of Humankind", "Brown"),
    ("Project Hail Mary", "Cixin"),
]
author_id = {}
for row in cur.execute("SELECT AuthorID, LastName FROM AUTHOR").fetchall():
    author_id[row[1]] = row[0]

cur.executemany(
    "INSERT INTO ITEM_AUTHOR (ItemID, AuthorID) VALUES (?, ?)",
    [(item_id[t], author_id[a]) for (t, a) in item_author_pairs],
)
con.commit()

# ITEM_COPY
# Weak entity: (ItemID, CopyNumber). Give most items 1-2 copies.
copy_rows = []
copy_plan = [
    ("Kafka on the Shore", 2), ("The House of the Spirits", 1),
    ("Sapiens: A Brief History of Humankind", 2), ("Project Hail Mary", 1),
    ("Americanah", 1), ("Outliers", 1), ("Educated: A Memoir", 1),
    ("Becoming", 1), ("The Night Circus", 1), ("National Geographic", 1),
    ("TIME Magazine", 1), ("Nature", 1), ("The Lancet", 1),
    ("Kind of Blue", 1), ("A Love Supreme", 1), ("Blue Train", 1),
    ("Project Hail Mary", 1),  # second copy handled via CopyNumber below
    ("The Remains of the Day", 1), ("Where the Crawdads Sing", 1),
    ("The Midnight Library", 1), ("Cosmos", 1),
]
shelf_counter = {}
for title, n_copies in copy_plan:
    start = shelf_counter.get(title, 0)
    for i in range(n_copies):
        copy_num = start + i + 1
        copy_rows.append((item_id[title], copy_num, "2022-01-01", f"SHELF-{item_id[title]}-{copy_num}"))
    shelf_counter[title] = start + n_copies

cur.executemany(
    "INSERT INTO ITEM_COPY (ItemID, CopyNumber, AcquisitionDate, ShelfLocation) VALUES (?, ?, ?, ?)",
    copy_rows,
)
con.commit()

# MEMBER
members = [
    ("Alice", "Nguyen", "alice.nguyen@example.com", "604-555-0111", "12 Maple St, Burnaby, BC", "1988-04-12", "2021-01-15"),
    ("Ben", "Carter", "family.carter@example.com", "604-555-0112", "45 Oak Ave, Burnaby, BC", "2016-09-01", "2022-03-22"),
    ("Chloe", "Martin", "chloe.martin@example.com", "604-555-0113", "89 Pine Rd, Vancouver, BC", "1975-07-01", "2020-07-01"),
    ("David", "Carter", "family.carter@example.com", "604-555-0114", "45 Oak Ave, Burnaby, BC", "2013-02-10", "2023-02-10"),
    ("Emma", "Wilson", "emma.wilson@example.com", "604-555-0115", "67 Cedar Ct, Vancouver, BC", "1955-11-05", "2019-11-05"),
    ("Frank", "Lopez", "frank.lopez@example.com", "604-555-0116", "34 Elm St, Burnaby, BC", "1990-09-18", "2021-09-18"),
    ("Grace", "Chen", "grace.chen@example.com", "604-555-0117", "56 Willow Way, Burnaby, BC", "1998-05-30", "2022-05-30"),
    ("Henry", "Patel", "henry.patel@example.com", "604-555-0118", "78 Aspen Dr, Vancouver, BC", "1958-01-12", "2020-01-12"),
    ("Ivy", "Robinson", "ivy.robinson@example.com", "604-555-0119", "90 Spruce St, Burnaby, BC", "2001-08-08", "2023-08-08"),
    ("Jack", "Thompson", "jack.thompson@example.com", "604-555-0120", "11 Fir Ave, Vancouver, BC", "1985-04-04", "2021-04-04"),
    ("Karen", "Davis", "karen.davis@example.com", "604-555-0121", "22 Poplar Rd, Burnaby, BC", "1979-12-01", "2022-12-01"),
    ("Liam", "Garcia", "liam.garcia@example.com", "604-555-0122", "33 Chestnut Ln, Vancouver, BC", "1992-10-10", "2020-10-10"),
]
cur.executemany(
    "INSERT INTO MEMBER (FirstName, LastName, Email, Phone, Address, DOB, MembershipDate) "
    "VALUES (?, ?, ?, ?, ?, ?, ?)",
    members,
)
con.commit()

# ROOM
rooms = [
    ("Reading Nook A", 20), ("Reading Nook B", 20), ("Community Hall", 80),
    ("Innovation Lab", 15), ("Gallery Room", 40), ("Story Time Corner", 25),
    ("Conference Room 1", 12), ("Conference Room 2", 12),
    ("Media Screening Room", 35), ("Rooftop Terrace", 50),
]
cur.executemany("INSERT INTO ROOM (RoomName, Capacity) VALUES (?, ?)", rooms)
con.commit()

# EVENT
events = [
    ("Murakami Book Club", "BOOK_CLUB", "Discussing Kafka on the Shore.", "2026-08-20", "18:00", "19:30", 1, "ADULTS"),
    ("Teen Manga Club", "BOOK_CLUB", "Monthly teen manga discussion.", "2026-08-21", "16:00", "17:00", 2, "TEENS"),
    ("Local Watercolor Art Show", "ART_SHOW", "Community watercolor exhibition.", "2026-08-25", "10:00", "16:00", 5, "ALL_AGES"),
    ("Classic Film Night: Casablanca", "FILM_SCREENING", "35mm screening of Casablanca.", "2026-08-26", "19:00", "21:15", 9, "ADULTS"),
    ("Kids Story Time", "WORKSHOP", "Weekly picture-book story time.", "2026-08-18", "10:30", "11:15", 6, "CHILDREN"),
    ("Intro to 3D Printing", "WORKSHOP", "Hands-on 3D printer basics.", "2026-08-22", "17:00", "18:30", 4, "TEENS"),
    ("Author Talk: Local Sci-Fi Writers", "AUTHOR_TALK", "Panel with three local authors.", "2026-09-02", "18:30", "20:00", 3, "ADULTS"),
    ("Documentary Screening Night", "FILM_SCREENING", "Nature documentary double feature.", "2026-09-05", "19:00", "21:00", 9, "ALL_AGES"),
    ("Photography Exhibit Opening", "ART_SHOW", "Opening reception for photo exhibit.", "2026-09-09", "17:00", "20:00", 5, "ALL_AGES"),
    ("Senior Book Club", "BOOK_CLUB", "Discussing a classic novel.", "2026-09-12", "14:00", "15:30", 7, "ADULTS"),
]
cur.executemany(
    "INSERT INTO EVENT (Name, EventType, Description, EventDate, StartTime, EndTime, RoomID, TargetAudience) "
    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    events,
)
con.commit()

# ATTENDANCE
attendance = [
    (1, 1, "2026-08-10"), (2, 5, "2026-08-11"), (3, 1, "2026-08-11"),
    (4, 6, "2026-08-12"), (5, 10, "2026-08-12"), (6, 3, "2026-08-13"),
    (7, 4, "2026-08-14"), (8, 10, "2026-08-14"), (9, 9, "2026-08-15"),
    (10, 7, "2026-08-15"), (11, 8, "2026-08-16"), (12, 9, "2026-08-16"),
]
cur.executemany(
    "INSERT INTO ATTENDANCE (MemberID, EventID, RegistrationDate) VALUES (?, ?, ?)",
    attendance,
)
con.commit()

# STAFF
staff = [
    ("Susan", "Moore", "Library Director", 98000, "604-555-0201", "susan.moore@library.org", "2010-06-01"),
    ("Tom", "Baker", "Head Librarian", 72000, "604-555-0202", "tom.baker@library.org", "2012-02-15"),
    ("Nina", "Foster", "Events Coordinator", 58000, "604-555-0203", "nina.foster@library.org", "2015-09-01"),
    ("Omar", "Farouk", "Reference Librarian", 61000, "604-555-0204", "omar.farouk@library.org", "2016-04-11"),
    ("Paula", "Diaz", "Reference Librarian", 59000, "604-555-0205", "paula.diaz@library.org", "2018-01-20"),
    ("Quentin", "Ross", "Circulation Assistant", 45000, "604-555-0206", "quentin.ross@library.org", "2019-07-08"),
    ("Rita", "Alvarez", "Cataloguing Specialist", 55000, "604-555-0207", "rita.alvarez@library.org", "2017-03-03"),
    ("Sam", "Wu", "IT Support Specialist", 62000, "604-555-0208", "sam.wu@library.org", "2020-10-12"),
    ("Tara", "Singh", "Children's Librarian", 57000, "604-555-0209", "tara.singh@library.org", "2014-05-19"),
    ("Victor", "Hughes", "Volunteer Coordinator", 50000, "604-555-0210", "victor.hughes@library.org", "2021-02-01"),
]
cur.executemany(
    "INSERT INTO STAFF (FirstName, LastName, Position, Salary, Phone, Email, HireDate) "
    "VALUES (?, ?, ?, ?, ?, ?, ?)",
    staff,
)
con.commit()

# FUTURE_ACQUISITION
acquisitions = [
    ("Fourth Wing", "PRINT_BOOK", 1, "2026-06-01", "HIGH", "ORDERED", 22.99),
    ("The Creative Act", "ONLINE_BOOK", 3, "2026-06-02", "MEDIUM", "CONSIDERING", 15.99),
    ("Wired Magazine Subscription", "MAGAZINE", None, "2026-06-03", "LOW", "CONSIDERING", 60.00),
    ("Cell Press Journal Subscription", "JOURNAL", None, "2026-06-04", "HIGH", "ORDERED", 450.00),
    ("Random Access Memories (Vinyl Reissue)", "RECORD", 7, "2026-06-05", "LOW", "CONSIDERING", 35.00),
    ("Tomorrow, and Tomorrow, and Tomorrow", "PRINT_BOOK", 9, "2026-06-06", "MEDIUM", "RECEIVED", 19.99),
    ("The Midnight Library", "ONLINE_BOOK", 10, "2026-06-07", "MEDIUM", "CONSIDERING", 12.99),
    ("Scientific American Archive Access", "MAGAZINE", None, "2026-06-08", "MEDIUM", "CONSIDERING", 80.00),
    ("The Lancet Oncology Subscription", "JOURNAL", None, "2026-06-09", "HIGH", "CONSIDERING", 500.00),
    ("Blue Train (Vinyl)", "RECORD", 11, "2026-06-10", "LOW", "RECEIVED", 28.00),
]
cur.executemany(
    "INSERT INTO FUTURE_ACQUISITION (Title, ItemType, RequestedByMemberID, RequestDate, Priority, Status, EstimatedCost) "
    "VALUES (?, ?, ?, ?, ?, ?, ?)",
    acquisitions,
)
con.commit()

# VOLUNTEER
volunteers = [
    (2, "2023-01-01", "Shelving", "ACTIVE"), (4, "2023-03-15", "Event Setup", "ACTIVE"),
    (6, "2022-11-01", "Story Time Assistant", "ACTIVE"), (7, "2023-05-20", "Tech Help Desk", "ACTIVE"),
    (9, "2024-01-10", "Shelving", "ACTIVE"), (11, "2022-08-08", "Book Sorting", "INACTIVE"),
    (1, "2024-02-14", "Front Desk Support", "ACTIVE"), (3, "2023-09-09", "Book Sorting", "ACTIVE"),
    (5, "2022-06-06", "Event Setup", "INACTIVE"), (8, "2024-04-04", "Front Desk Support", "ACTIVE"),
]
cur.executemany(
    "INSERT INTO VOLUNTEER (MemberID, StartDate, SkillArea, Status) VALUES (?, ?, ?, ?)",
    volunteers,
)
con.commit()

# DONATION
donations = [
    (1, "The Night Circus", "PRINT_BOOK", "2026-06-01", "PENDING"),
    (3, "Old Jazz Vinyl Collection (5 records)", "RECORD", "2026-06-03", "PENDING"),
    (None, "National Geographic back issues 2018-2020", "MAGAZINE", "2026-06-05", "ACCEPTED"),
    (5, "Educated: A Memoir", "PRINT_BOOK", "2026-06-08", "PENDING"),
    (6, "Assorted Science Journals", "JOURNAL", "2026-06-10", "REJECTED"),
    (8, "Becoming by Michelle Obama", "PRINT_BOOK", "2026-06-12", "PENDING"),
    (9, "Miles Davis Vinyl Set", "RECORD", "2026-06-14", "ACCEPTED"),
    (10, "Old Encyclopedia Set", "PRINT_BOOK", "2026-06-16", "REJECTED"),
    (2, "Digital Photography Magazine Bundle", "MAGAZINE", "2026-06-18", "PENDING"),
    (12, "Local History Journal Archive", "JOURNAL", "2026-06-20", "PENDING"),
]
cur.executemany(
    "INSERT INTO DONATION (MemberID, ItemTitle, ItemType, DonationDate, Status) VALUES (?, ?, ?, ?, ?)",
    donations,
)
con.commit()

# HELP_REQUEST
help_requests = [
    (1, 4, "2026-07-01", "Finding sources for a research paper", "RESOLVED", "Pointed to JSTOR access."),
    (2, 5, "2026-07-02", "How to renew a loan online", "RESOLVED", "Walked through the portal."),
    (3, None, "2026-07-03", "Looking for large-print books", "OPEN", None),
    (4, 4, "2026-07-04", "Need help with database access for thesis", "IN_PROGRESS", "Scheduled follow-up."),
    (5, 6, "2026-07-05", "Interested in donating old journals", "RESOLVED", "Forwarded to donations desk."),
    (6, None, "2026-07-06", "Question about magazine holds", "OPEN", None),
    (7, 5, "2026-07-07", "Help locating a rare vinyl record", "IN_PROGRESS", "Checking special collections."),
    (8, 4, "2026-07-08", "Citation formatting help (APA)", "RESOLVED", "Provided citation guide."),
    (9, 6, "2026-07-09", "Request for children's reading list", "RESOLVED", "Emailed a curated list."),
    (10, None, "2026-07-10", "How to become a volunteer", "OPEN", None),
]
cur.executemany(
    "INSERT INTO HELP_REQUEST (MemberID, EmployeeID, RequestDate, Topic, Status, Notes) VALUES (?, ?, ?, ?, ?, ?)",
    help_requests,
)
con.commit()

# LOAN + FINE
loans_plan = [
    # (ItemID, CopyNumber, MemberID, CheckoutDate, DueDate, ReturnDate or None)
    (item_id["Kafka on the Shore"], 1, 1, "2026-06-20", "2026-07-04", "2026-07-03"),   # on time
    (item_id["Kafka on the Shore"], 2, 2, "2026-06-22", "2026-07-06", "2026-07-10"),   # LATE
    (item_id["Sapiens: A Brief History of Humankind"], 1, 4, "2026-06-25", "2026-07-09", "2026-07-08"),  # on time
    (item_id["Project Hail Mary"], 1, 6, "2026-06-28", "2026-07-12", "2026-07-18"),    # LATE
    (item_id["Americanah"], 1, 7, "2026-07-01", "2026-07-15", "2026-07-14"),           # on time
    (item_id["Outliers"], 1, 9, "2026-07-02", "2026-07-16", None),                     # still out
    (item_id["Kind of Blue"], 1, 11, "2026-06-15", "2026-06-29", "2026-07-05"),        # LATE
    (item_id["Nature"], 1, 12, "2026-06-18", "2026-07-02", "2026-07-01"),              # on time
    (item_id["The House of the Spirits"], 1, 3, "2026-06-10", "2026-06-24", "2026-06-23"),  # on time
    (item_id["A Love Supreme"], 1, 5, "2026-06-12", "2026-06-26", "2026-06-25"),       # on time
    (item_id["Sapiens: A Brief History of Humankind"], 2, 10, "2026-07-03", "2026-07-17", None),  # still out
    (item_id["Blue Train"], 1, 8, "2026-05-01", "2026-05-15", "2026-05-20"),           # LATE
    (item_id["The Lancet"], 1, 1, "2026-05-02", "2026-05-16", "2026-05-16"),           # on time
    (item_id["Educated: A Memoir"], 1, 2, "2026-05-03", "2026-05-17", "2026-05-25"),   # LATE
    (item_id["Becoming"], 1, 3, "2026-05-04", "2026-05-18", "2026-05-19"),             # LATE
    (item_id["The Night Circus"], 1, 4, "2026-05-05", "2026-05-19", "2026-05-30"),     # LATE
    (item_id["National Geographic"], 1, 5, "2026-05-06", "2026-05-20", "2026-05-20"),  # on time
    (item_id["TIME Magazine"], 1, 6, "2026-05-07", "2026-05-21", "2026-05-28"),        # LATE
    (item_id["Project Hail Mary"], 2, 7, "2026-05-09", "2026-05-23", "2026-05-27"),    # LATE (2nd copy of this item)
    (item_id["The Remains of the Day"], 1, 9, "2026-05-10", "2026-05-24", "2026-05-29"),  # LATE
]

loan_ids = []
for (iid, cn, mid, checkout, due, ret) in loans_plan:
    cur.execute(
        "INSERT INTO LOAN (ItemID, CopyNumber, MemberID, CheckoutDate, DueDate) VALUES (?, ?, ?, ?, ?)",
        (iid, cn, mid, checkout, due),
    )
    loan_ids.append((cur.lastrowid, ret))
con.commit()

# Now apply returns via UPDATE so the checkout/return/late-fine triggers fire
for loan_id, ret in loan_ids:
    if ret is not None:
        cur.execute("UPDATE LOAN SET ReturnDate = ? WHERE LoanID = ?", (ret, loan_id))
con.commit()

# Give a few fines realistic paid/waived statuses instead of leaving all UNPAID
cur.execute("UPDATE FINE SET Status = 'PAID', PaidDate = '2026-07-12' WHERE FineID IN (1, 3)")
cur.execute("UPDATE FINE SET Status = 'WAIVED' WHERE FineID = 5")
con.commit()

# REPORT
print("Rows per table:")
tables = [r[0] for r in cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name <> 'sqlite_sequence' ORDER BY name"
).fetchall()]
for table in tables:
    n = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table:<20} {n}")

print("\nFINE rows (auto-generated by trigger on late returns):")
for row in cur.execute("SELECT * FROM FINE").fetchall():
    print(" ", row)

print("\nSample of MEMBER_WITH_TYPE view (derived age bracket):")
for row in cur.execute("SELECT MemberID, FirstName, DOB, MembershipType FROM MEMBER_WITH_TYPE LIMIT 5").fetchall():
    print(" ", row)

con.close()
print("\nDone. Database written to", DB_PATH)