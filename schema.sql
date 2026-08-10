-- Step 4: Schema creation for Library Management System
PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- PUBLISHER
-- ---------------------------------------------------------------------
CREATE TABLE PUBLISHER (
    PublisherID  INTEGER PRIMARY KEY AUTOINCREMENT,
    Name         TEXT NOT NULL UNIQUE,
    Address      TEXT,
    Phone        TEXT
);

-- ---------------------------------------------------------------------
-- AUTHOR
-- ---------------------------------------------------------------------
CREATE TABLE AUTHOR (
    AuthorID   INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName  TEXT NOT NULL,
    LastName   TEXT NOT NULL,
    Bio        TEXT
);

-- ---------------------------------------------------------------------
-- ITEM (superclass)  
-- ---------------------------------------------------------------------
CREATE TABLE ITEM (
    ItemID           INTEGER PRIMARY KEY AUTOINCREMENT,
    Title            TEXT NOT NULL,
    ItemType         TEXT NOT NULL CHECK (ItemType IN
                        ('PRINT_BOOK','ONLINE_BOOK','MAGAZINE','JOURNAL','RECORD')),
    PublisherID      INTEGER NOT NULL REFERENCES PUBLISHER(PublisherID),
    PublicationYear  INTEGER CHECK (PublicationYear BETWEEN 1400 AND 2100),
    Genre            TEXT,
    Language         TEXT NOT NULL DEFAULT 'English'
);

-- ISA subclasses: ItemID is both PK and FK to ITEM
CREATE TABLE PRINT_BOOK (
    ItemID        INTEGER PRIMARY KEY REFERENCES ITEM(ItemID) ON DELETE CASCADE,
    PageCount     INTEGER CHECK (PageCount > 0),
    ShelfCategory TEXT
);

CREATE TABLE ONLINE_BOOK (
    ItemID              INTEGER PRIMARY KEY REFERENCES ITEM(ItemID) ON DELETE CASCADE,
    FileFormat          TEXT CHECK (FileFormat IN ('EPUB','PDF','MOBI')),
    FileSizeMB          REAL CHECK (FileSizeMB > 0),
    ConcurrentLicenses  INTEGER NOT NULL DEFAULT 1 CHECK (ConcurrentLicenses > 0)
);

CREATE TABLE MAGAZINE (
    ItemID       INTEGER PRIMARY KEY REFERENCES ITEM(ItemID) ON DELETE CASCADE,
    IssueNumber  TEXT,
    Frequency    TEXT CHECK (Frequency IN ('WEEKLY','MONTHLY','QUARTERLY'))
);

CREATE TABLE JOURNAL (
    ItemID        INTEGER PRIMARY KEY REFERENCES ITEM(ItemID) ON DELETE CASCADE,
    Volume        INTEGER,
    IssueNumber   INTEGER,
    PeerReviewed  INTEGER NOT NULL DEFAULT 1 CHECK (PeerReviewed IN (0,1))
);

CREATE TABLE RECORD (
    ItemID          INTEGER PRIMARY KEY REFERENCES ITEM(ItemID) ON DELETE CASCADE,
    MediaFormat     TEXT CHECK (MediaFormat IN ('VINYL','CD','CASSETTE')),
    DurationMinutes INTEGER CHECK (DurationMinutes > 0)
);

-- ---------------------------------------------------------------------
-- ITEM_AUTHOR 
-- ---------------------------------------------------------------------
CREATE TABLE ITEM_AUTHOR (
    ItemID    INTEGER NOT NULL REFERENCES ITEM(ItemID)     ON DELETE CASCADE,
    AuthorID  INTEGER NOT NULL REFERENCES AUTHOR(AuthorID) ON DELETE CASCADE,
    PRIMARY KEY (ItemID, AuthorID)
);

-- ---------------------------------------------------------------------
-- ITEM_COPY -- WEAK ENTITY: identity depends on ITEM.
-- Composite key (ItemID, CopyNumber); 
-- ---------------------------------------------------------------------
CREATE TABLE ITEM_COPY (
    ItemID          INTEGER NOT NULL REFERENCES ITEM(ItemID) ON DELETE CASCADE,
    CopyNumber      INTEGER NOT NULL,
    Status          TEXT NOT NULL DEFAULT 'AVAILABLE'
                        CHECK (Status IN ('AVAILABLE','BORROWED','RESERVED','LOST','DAMAGED')),
    AcquisitionDate DATE NOT NULL,
    ShelfLocation   TEXT,
    PRIMARY KEY (ItemID, CopyNumber)
);

-- ---------------------------------------------------------------------
-- MEMBER  
-- ---------------------------------------------------------------------
CREATE TABLE MEMBER (
    MemberID        INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName       TEXT NOT NULL,
    LastName        TEXT NOT NULL,
    Email           TEXT,
    Phone           TEXT,
    Address         TEXT,
    DOB             DATE NOT NULL,
    MembershipDate  DATE NOT NULL
);

-- Derived membership type 
CREATE VIEW MEMBER_WITH_TYPE AS
SELECT
    MemberID, FirstName, LastName, Email, Phone, Address, DOB, MembershipDate,
    CASE
        WHEN (JULIANDAY('now') - JULIANDAY(DOB)) / 365.25 < 18 THEN 'CHILD'
        WHEN (JULIANDAY('now') - JULIANDAY(DOB)) / 365.25 < 65 THEN 'REGULAR'
        ELSE 'SENIOR'
    END AS MembershipType
FROM MEMBER;

-- ---------------------------------------------------------------------
-- LOAN 
-- ---------------------------------------------------------------------
CREATE TABLE LOAN (
    LoanID       INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemID       INTEGER NOT NULL,
    CopyNumber   INTEGER NOT NULL,
    MemberID     INTEGER NOT NULL REFERENCES MEMBER(MemberID),
    CheckoutDate DATE NOT NULL,
    DueDate      DATE NOT NULL,
    ReturnDate   DATE,
    FOREIGN KEY (ItemID, CopyNumber) REFERENCES ITEM_COPY(ItemID, CopyNumber),
    CHECK (DueDate > CheckoutDate),
    CHECK (ReturnDate IS NULL OR ReturnDate >= CheckoutDate)
);

-- ---------------------------------------------------------------------
-- FINE 
-- ---------------------------------------------------------------------
CREATE TABLE FINE (
    FineID     INTEGER PRIMARY KEY AUTOINCREMENT,
    LoanID     INTEGER NOT NULL UNIQUE REFERENCES LOAN(LoanID),
    Amount     REAL NOT NULL CHECK (Amount >= 0),
    IssuedDate DATE NOT NULL,
    PaidDate   DATE,
    Status     TEXT NOT NULL DEFAULT 'UNPAID' CHECK (Status IN ('UNPAID','PAID','WAIVED'))
);

-- ---------------------------------------------------------------------
-- ROOM
-- ---------------------------------------------------------------------
CREATE TABLE ROOM (
    RoomID    INTEGER PRIMARY KEY AUTOINCREMENT,
    RoomName  TEXT NOT NULL UNIQUE,
    Capacity  INTEGER NOT NULL CHECK (Capacity > 0)
);

-- ---------------------------------------------------------------------
-- EVENT
-- ---------------------------------------------------------------------
CREATE TABLE EVENT (
    EventID        INTEGER PRIMARY KEY AUTOINCREMENT,
    Name           TEXT NOT NULL,
    EventType      TEXT NOT NULL CHECK (EventType IN
                        ('BOOK_CLUB','WORKSHOP','ART_SHOW','FILM_SCREENING','AUTHOR_TALK')),
    Description    TEXT,
    EventDate      DATE NOT NULL,
    StartTime      TEXT NOT NULL,
    EndTime        TEXT NOT NULL,
    RoomID         INTEGER NOT NULL REFERENCES ROOM(RoomID),
    TargetAudience TEXT NOT NULL DEFAULT 'ALL_AGES'
                        CHECK (TargetAudience IN ('CHILDREN','TEENS','ADULTS','ALL_AGES')),
    CHECK (EndTime > StartTime)
);

-- ---------------------------------------------------------------------
-- ATTENDANCE 
-- ---------------------------------------------------------------------
CREATE TABLE ATTENDANCE (
    MemberID         INTEGER NOT NULL REFERENCES MEMBER(MemberID),
    EventID          INTEGER NOT NULL REFERENCES EVENT(EventID),
    RegistrationDate DATE NOT NULL,
    PRIMARY KEY (MemberID, EventID)
);

-- ---------------------------------------------------------------------
-- STAFF
-- ---------------------------------------------------------------------
CREATE TABLE STAFF (
    EmployeeID  INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName   TEXT NOT NULL,
    LastName    TEXT NOT NULL,
    Position    TEXT NOT NULL,
    Salary      REAL NOT NULL CHECK (Salary > 0),
    Phone       TEXT,
    Email       TEXT NOT NULL UNIQUE,
    HireDate    DATE NOT NULL
);

-- ---------------------------------------------------------------------
-- FUTURE_ACQUISITION
-- ---------------------------------------------------------------------
CREATE TABLE FUTURE_ACQUISITION (
    AcquisitionID        INTEGER PRIMARY KEY AUTOINCREMENT,
    Title                TEXT NOT NULL,
    ItemType             TEXT NOT NULL CHECK (ItemType IN
                            ('PRINT_BOOK','ONLINE_BOOK','MAGAZINE','JOURNAL','RECORD')),
    RequestedByMemberID  INTEGER REFERENCES MEMBER(MemberID),
    RequestDate          DATE NOT NULL,
    Priority             TEXT NOT NULL DEFAULT 'MEDIUM' CHECK (Priority IN ('LOW','MEDIUM','HIGH')),
    Status               TEXT NOT NULL DEFAULT 'CONSIDERING'
                            CHECK (Status IN ('CONSIDERING','ORDERED','RECEIVED')),
    EstimatedCost        REAL CHECK (EstimatedCost >= 0)
);

-- ---------------------------------------------------------------------
-- VOLUNTEER  
-- ---------------------------------------------------------------------
CREATE TABLE VOLUNTEER (
    VolunteerID  INTEGER PRIMARY KEY AUTOINCREMENT,
    MemberID     INTEGER NOT NULL UNIQUE REFERENCES MEMBER(MemberID),
    StartDate    DATE NOT NULL,
    SkillArea    TEXT,
    Status       TEXT NOT NULL DEFAULT 'ACTIVE' CHECK (Status IN ('ACTIVE','INACTIVE'))
);

-- ---------------------------------------------------------------------
-- DONATION 
-- ---------------------------------------------------------------------
CREATE TABLE DONATION (
    DonationID    INTEGER PRIMARY KEY AUTOINCREMENT,
    MemberID      INTEGER REFERENCES MEMBER(MemberID),
    ItemTitle     TEXT NOT NULL,
    ItemType      TEXT NOT NULL CHECK (ItemType IN
                        ('PRINT_BOOK','ONLINE_BOOK','MAGAZINE','JOURNAL','RECORD')),
    DonationDate  DATE NOT NULL,
    Status        TEXT NOT NULL DEFAULT 'PENDING' CHECK (Status IN ('PENDING','ACCEPTED','REJECTED'))
);

-- ---------------------------------------------------------------------
-- HELP_REQUEST 
-- ---------------------------------------------------------------------
CREATE TABLE HELP_REQUEST (
    RequestID    INTEGER PRIMARY KEY AUTOINCREMENT,
    MemberID     INTEGER NOT NULL REFERENCES MEMBER(MemberID),
    EmployeeID   INTEGER REFERENCES STAFF(EmployeeID),
    RequestDate  DATE NOT NULL,
    Topic        TEXT NOT NULL,
    Status       TEXT NOT NULL DEFAULT 'OPEN' CHECK (Status IN ('OPEN','IN_PROGRESS','RESOLVED')),
    Notes        TEXT
);

-- =====================================================================
-- TRIGGERS
-- =====================================================================

-- (T1) Prevent borrowing a copy that isn't AVAILABLE
CREATE TRIGGER trg_loan_copy_available
BEFORE INSERT ON LOAN
WHEN (SELECT Status FROM ITEM_COPY WHERE ItemID = NEW.ItemID AND CopyNumber = NEW.CopyNumber) <> 'AVAILABLE'
BEGIN
    SELECT RAISE(ABORT, 'Item copy is not available for borrowing');
END;

-- (T2) On checkout, flip the copy to BORROWED
CREATE TRIGGER trg_loan_mark_borrowed
AFTER INSERT ON LOAN
BEGIN
    UPDATE ITEM_COPY SET Status = 'BORROWED'
    WHERE ItemID = NEW.ItemID AND CopyNumber = NEW.CopyNumber;
END;

-- (T3) On return, free the copy
CREATE TRIGGER trg_loan_mark_returned
AFTER UPDATE OF ReturnDate ON LOAN
WHEN NEW.ReturnDate IS NOT NULL AND OLD.ReturnDate IS NULL
BEGIN
    UPDATE ITEM_COPY SET Status = 'AVAILABLE'
    WHERE ItemID = NEW.ItemID AND CopyNumber = NEW.CopyNumber;
END;

-- (T4) On late return, auto-create a FINE ($0.25/day late)
CREATE TRIGGER trg_loan_late_fine
AFTER UPDATE OF ReturnDate ON LOAN
WHEN NEW.ReturnDate IS NOT NULL AND OLD.ReturnDate IS NULL
     AND NEW.ReturnDate > NEW.DueDate
BEGIN
    INSERT INTO FINE (LoanID, Amount, IssuedDate, Status)
    VALUES (NEW.LoanID,
            ROUND((JULIANDAY(NEW.ReturnDate) - JULIANDAY(NEW.DueDate)) * 0.25, 2),
            NEW.ReturnDate, 'UNPAID');
END;

-- (T5) Cap event registration at the room's capacity
CREATE TRIGGER trg_event_capacity
BEFORE INSERT ON ATTENDANCE
WHEN (SELECT COUNT(*) FROM ATTENDANCE WHERE EventID = NEW.EventID)
     >= (SELECT r.Capacity FROM EVENT e JOIN ROOM r ON e.RoomID = r.RoomID WHERE e.EventID = NEW.EventID)
BEGIN
    SELECT RAISE(ABORT, 'Event is at full capacity');
END;

-- (T6) A member can only have one active VOLUNTEER record
CREATE TRIGGER trg_volunteer_no_duplicate
BEFORE INSERT ON VOLUNTEER
WHEN (SELECT COUNT(*) FROM VOLUNTEER WHERE MemberID = NEW.MemberID) > 0
BEGIN
    SELECT RAISE(ABORT, 'This member already has a volunteer record');
END;

CREATE TRIGGER trg_event_audience_check
BEFORE INSERT ON ATTENDANCE
WHEN (SELECT TargetAudience FROM EVENT WHERE EventID = NEW.EventID) <> 'ALL_AGES'
     AND (
         CASE
             WHEN (JULIANDAY('now') - JULIANDAY((SELECT DOB FROM MEMBER WHERE MemberID = NEW.MemberID))) / 365.25 < 13 THEN 'CHILDREN'
             WHEN (JULIANDAY('now') - JULIANDAY((SELECT DOB FROM MEMBER WHERE MemberID = NEW.MemberID))) / 365.25 < 18 THEN 'TEENS'
             ELSE 'ADULTS'
         END
     ) <> (SELECT TargetAudience FROM EVENT WHERE EventID = NEW.EventID)
BEGIN
    SELECT RAISE(ABORT, 'Member age does not match this event''s target audience');
END;