"""
app.py — Library Database Application (Step 6)

A single-tier CLI application that lets a library user:
  1. Find an item
  2. Borrow an item
  3. Return a borrowed item
  4. Donate an item
  5. Find an event
  6. Register for an event
  7. Volunteer for the library
  8. Ask a librarian for help

"""
import sqlite3
from datetime import date, timedelta

DB_PATH = "library.db"


def get_connection():
    """Open a connection with foreign key enforcement turned on."""
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON;")
    return con


# =====================================================================
# 1. FIND AN ITEM
# =====================================================================
def find_item(con, keyword):
    """
    Search the catalog by (partial, case-insensitive) title or genre.
    Returns a list of rows: (ItemID, Title, ItemType, Genre, PublisherName,
    AvailableCopies, TotalCopies).
    """
    cur = con.cursor()
    cur.execute(
        """
        SELECT i.ItemID, i.Title, i.ItemType, i.Genre, p.Name,
               SUM(CASE WHEN c.Status = 'AVAILABLE' THEN 1 ELSE 0 END) AS AvailableCopies,
               COUNT(c.CopyNumber) AS TotalCopies
        FROM ITEM i
        JOIN PUBLISHER p ON i.PublisherID = p.PublisherID
        LEFT JOIN ITEM_COPY c ON c.ItemID = i.ItemID
        WHERE i.Title LIKE ? OR i.Genre LIKE ?
        GROUP BY i.ItemID
        ORDER BY i.Title
        """,
        (f"%{keyword}%", f"%{keyword}%"),
    )
    return cur.fetchall()


def list_copies(con, item_id):
    """Return every copy of an item with its status, for choosing one to borrow."""
    cur = con.cursor()
    cur.execute(
        "SELECT CopyNumber, Status, ShelfLocation FROM ITEM_COPY WHERE ItemID = ? ORDER BY CopyNumber",
        (item_id,),
    )
    return cur.fetchall()


# =====================================================================
# 2. BORROW AN ITEM
# =====================================================================
def borrow_item(con, item_id, copy_number, member_id, loan_days=14):
    """
    Create a loan for the given (item, copy) and member. Relies on
    trg_loan_copy_available to reject the borrow if the copy isn't
    AVAILABLE, and trg_loan_mark_borrowed to flip the copy's status.
    Returns the new LoanID on success, or raises sqlite3.IntegrityError.
    """
    cur = con.cursor()
    checkout = date.today().isoformat()
    due = (date.today() + timedelta(days=loan_days)).isoformat()
    cur.execute(
        "INSERT INTO LOAN (ItemID, CopyNumber, MemberID, CheckoutDate, DueDate) "
        "VALUES (?, ?, ?, ?, ?)",
        (item_id, copy_number, member_id, checkout, due),
    )
    con.commit()
    return cur.lastrowid


# =====================================================================
# 3. RETURN A BORROWED ITEM
# =====================================================================
def return_item(con, loan_id, return_date=None):
    """
    Mark a loan as returned. trg_loan_mark_returned frees the copy;
    trg_loan_late_fine automatically inserts a FINE row if returned late.
    Returns True if a fine was generated, False otherwise.
    """
    cur = con.cursor()
    ret = return_date or date.today().isoformat()
    cur.execute("SELECT ReturnDate FROM LOAN WHERE LoanID = ?", (loan_id,))
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"No loan found with LoanID {loan_id}")
    if row[0] is not None:
        raise ValueError(f"Loan {loan_id} was already returned on {row[0]}")

    cur.execute("UPDATE LOAN SET ReturnDate = ? WHERE LoanID = ?", (ret, loan_id))
    con.commit()

    cur.execute("SELECT 1 FROM FINE WHERE LoanID = ?", (loan_id,))
    return cur.fetchone() is not None


def get_open_loans_for_member(con, member_id):
    """List a member's currently un-returned loans, for choosing one to return."""
    cur = con.cursor()
    cur.execute(
        """
        SELECT l.LoanID, i.Title, l.CopyNumber, l.CheckoutDate, l.DueDate
        FROM LOAN l
        JOIN ITEM i ON i.ItemID = l.ItemID
        WHERE l.MemberID = ? AND l.ReturnDate IS NULL
        ORDER BY l.DueDate
        """,
        (member_id,),
    )
    return cur.fetchall()


# =====================================================================
# 4. DONATE AN ITEM
# =====================================================================
def donate_item(con, item_title, item_type, member_id=None, donation_date=None):
    """
    Record a donation offer. member_id may be None for an anonymous donor.
    Status starts PENDING; staff decide ACCEPTED/REJECTED later.
    """
    cur = con.cursor()
    d_date = donation_date or date.today().isoformat()
    cur.execute(
        "INSERT INTO DONATION (MemberID, ItemTitle, ItemType, DonationDate, Status) "
        "VALUES (?, ?, ?, ?, 'PENDING')",
        (member_id, item_title, item_type, d_date),
    )
    con.commit()
    return cur.lastrowid


# =====================================================================
# 5. FIND AN EVENT
# =====================================================================
def find_event(con, keyword=None, audience=None):
    """
    Search upcoming events by keyword (name/description) and/or target
    audience. Also reports remaining seats (room capacity - registrations).
    """
    cur = con.cursor()
    sql = """
        SELECT e.EventID, e.Name, e.EventType, e.EventDate, e.StartTime, e.EndTime,
               r.RoomName, e.TargetAudience,
               r.Capacity - COUNT(a.MemberID) AS SeatsLeft
        FROM EVENT e
        JOIN ROOM r ON r.RoomID = e.RoomID
        LEFT JOIN ATTENDANCE a ON a.EventID = e.EventID
        WHERE 1=1
    """
    params = []
    if keyword:
        sql += " AND (e.Name LIKE ? OR e.Description LIKE ?)"
        params += [f"%{keyword}%", f"%{keyword}%"]
    if audience:
        sql += " AND e.TargetAudience = ?"
        params.append(audience)
    sql += " GROUP BY e.EventID ORDER BY e.EventDate, e.StartTime"
    cur.execute(sql, params)
    return cur.fetchall()


# =====================================================================
# 6. REGISTER FOR AN EVENT
# =====================================================================
def register_for_event(con, member_id, event_id, registration_date=None):
    """
    Register a member for an event. trg_event_capacity rejects the
    registration if the room is already full; the ATTENDANCE PRIMARY KEY
    (MemberID, EventID) rejects a duplicate registration by the same member.
    """
    cur = con.cursor()
    r_date = registration_date or date.today().isoformat()
    cur.execute(
        "INSERT INTO ATTENDANCE (MemberID, EventID, RegistrationDate) VALUES (?, ?, ?)",
        (member_id, event_id, r_date),
    )
    con.commit()


# =====================================================================
# 7. VOLUNTEER FOR THE LIBRARY
# =====================================================================
def volunteer_signup(con, member_id, skill_area=None, start_date=None):
    """
    Register an existing member as a volunteer. trg_volunteer_no_duplicate
    (backed by the UNIQUE(MemberID) constraint) rejects a member who is
    already a volunteer.
    """
    cur = con.cursor()
    s_date = start_date or date.today().isoformat()
    cur.execute(
        "INSERT INTO VOLUNTEER (MemberID, StartDate, SkillArea, Status) "
        "VALUES (?, ?, ?, 'ACTIVE')",
        (member_id, s_date, skill_area),
    )
    con.commit()
    return cur.lastrowid


# =====================================================================
# 8. ASK FOR HELP FROM A LIBRARIAN
# =====================================================================
def ask_for_help(con, member_id, topic, notes=None, request_date=None):
    """Submit a help request. Unassigned (EmployeeID NULL) until staff pick it up."""
    cur = con.cursor()
    r_date = request_date or date.today().isoformat()
    cur.execute(
        "INSERT INTO HELP_REQUEST (MemberID, EmployeeID, RequestDate, Topic, Status, Notes) "
        "VALUES (?, NULL, ?, ?, 'OPEN', ?)",
        (member_id, r_date, topic, notes),
    )
    con.commit()
    return cur.lastrowid


# =====================================================================
# CLI MENU
# =====================================================================
def prompt_int(msg):
    while True:
        raw = input(msg).strip()
        if raw.isdigit():
            return int(raw)
        print("  Please enter a whole number.")


def menu_find_item(con):
    keyword = input("Search by title or genre (leave blank to see everything): ").strip()
    results = find_item(con, keyword)   # empty string matches everything via LIKE '%%'
    if not results:
        print("No items matched.")
        return
    print(f"\n{'ItemID':<7}{'Title':<40}{'Type':<14}{'Genre':<12}{'Publisher':<20}{'Avail/Total'}")
    for r in results:
        item_id, title, itype, genre, pub, avail, total = r
        print(f"{item_id:<7}{title[:38]:<40}{itype:<14}{(genre or ''):<12}{pub[:18]:<20}{avail}/{total}")


def menu_borrow_item(con):
    item_id = prompt_int("Item ID (use 'Find an item' first): ")
    copies = list_copies(con, item_id)
    if not copies:
        print("That item has no copies on file.")
        return
    print("\nCopies:")
    for cn, status, shelf in copies:
        print(f"  Copy {cn}: {status} ({shelf})")
    copy_number = prompt_int("Which copy number would you like to borrow? ")
    member_id = prompt_int("Your Member ID: ")
    try:
        loan_id = borrow_item(con, item_id, copy_number, member_id)
        print(f"Borrowed! Loan ID {loan_id}. Please return it within 14 days.")
    except sqlite3.IntegrityError as e:
        print(f"Could not complete the loan: {e}")


def menu_return_item(con):
    member_id = prompt_int("Your Member ID: ")
    open_loans = get_open_loans_for_member(con, member_id)
    if not open_loans:
        print("You have no items currently checked out.")
        return
    print("\nYour open loans:")
    for loan_id, title, cn, checkout, due in open_loans:
        print(f"  Loan {loan_id}: {title} (copy {cn}), due {due}")
    loan_id = prompt_int("Which Loan ID are you returning? ")
    try:
        fined = return_item(con, loan_id)
        if fined:
            print("Returned. Note: this was late, a fine has been recorded on your account.")
        else:
            print("Returned on time. Thank you!")
    except (sqlite3.IntegrityError, ValueError) as e:
        print(f"Could not process the return: {e}")


def menu_donate_item(con):
    title = input("Title of the item you'd like to donate: ").strip()
    print("Item type: PRINT_BOOK, ONLINE_BOOK, MAGAZINE, JOURNAL, RECORD")
    itype = input("Item type: ").strip().upper()
    anon = input("Donate anonymously? (y/n): ").strip().lower()
    member_id = None
    if anon != "y":
        member_id = prompt_int("Your Member ID: ")
    try:
        donation_id = donate_item(con, title, itype, member_id)
        print(f"Thank you! Donation recorded as ID {donation_id}, pending staff review.")
    except sqlite3.IntegrityError as e:
        print(f"Could not record the donation: {e}")


def menu_find_event(con):
    keyword = input("Search by event name/description (blank for all): ").strip() or None
    print("Audience filter: CHILDREN, TEENS, ADULTS, ALL_AGES (blank for any)")
    audience = input("Audience: ").strip().upper() or None
    results = find_event(con, keyword, audience)
    if not results:
        print("No events matched.")
        return
    print(f"\n{'EventID':<8}{'Name':<32}{'Type':<16}{'Date':<12}{'Time':<14}{'Room':<18}{'Audience':<10}{'Seats Left'}")
    for r in results:
        eid, name, etype, edate, start, end, room, aud, seats = r
        print(f"{eid:<8}{name[:30]:<32}{etype:<16}{edate:<12}{(start+'-'+end):<14}{room[:16]:<18}{aud:<10}{seats}")


def menu_register_event(con):
    event_id = prompt_int("Event ID (use 'Find an event' first): ")
    member_id = prompt_int("Your Member ID: ")
    try:
        register_for_event(con, member_id, event_id)
        print("You're registered! See you there.")
    except sqlite3.IntegrityError as e:
        msg = str(e)
        if "UNIQUE" in msg:
            print("You're already registered for this event.")
        elif "capacity" in msg.lower():
            print("Sorry, this event is at full capacity.")
        elif "audience" in msg.lower():
            print("Sorry, this event isn't recommended for your age group.")
        else:
            print(f"Could not complete registration: {e}")


def menu_volunteer(con):
    member_id = prompt_int("Your Member ID: ")
    skill = input("Area of interest (e.g. Shelving, Event Setup, Front Desk): ").strip()
    try:
        vid = volunteer_signup(con, member_id, skill)
        print(f"Welcome to the volunteer team! Volunteer ID {vid}.")
    except sqlite3.IntegrityError as e:
        if "already has a volunteer record" in str(e):
            print("You're already registered as a volunteer.")
        else:
            print(f"Could not complete volunteer signup: {e}")


def menu_ask_help(con):
    member_id = prompt_int("Your Member ID: ")
    topic = input("What do you need help with? ").strip()
    try:
        rid = ask_for_help(con, member_id, topic)
        print(f"Your request has been submitted (Request ID {rid}). A librarian will follow up.")
    except sqlite3.IntegrityError as e:
        print(f"Could not submit the request: {e}")



MENU = {
    "1": ("Find an item", menu_find_item),
    "2": ("Borrow an item", menu_borrow_item),
    "3": ("Return a borrowed item", menu_return_item),
    "4": ("Donate an item", menu_donate_item),
    "5": ("Find an event", menu_find_event),
    "6": ("Register for an event", menu_register_event),
    "7": ("Volunteer for the library", menu_volunteer),
    "8": ("Ask for help from a librarian", menu_ask_help),
}


def main():
    con = get_connection()
    print("=== Welcome to the Library ===")
    while True:
        print("\nWhat would you like to do?")
        for key, (label, _) in MENU.items():
            print(f"  {key}. {label}")
        print("  0. Exit")
        choice = input("> ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        if choice in MENU:
            MENU[choice][1](con)
        else:
            print("Please choose a valid option.")
    con.close()


if __name__ == "__main__":
    main()