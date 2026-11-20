# -*- coding: utf-8 -*-
"""
Flight Booking Management System - Academic Viva Preparation Guide (Hinglish)
Generates a comprehensive, easy-to-learn bilingual viva guide directly on Desktop.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

DESKTOP_PATH = r"C:\Users\OMEN\Desktop"
PDF_NAME = "Flight_Booking_Management_System_Viva_Guide_Hinglish.pdf"
PDF_PATH = os.path.join(DESKTOP_PATH, PDF_NAME)


class PageNumCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(PageNumCanvas, self).__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_footer(page_count)
            super(PageNumCanvas, self).showPage()
        super(PageNumCanvas, self).save()

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(45, 755, "Rungta International Skills University | PS No. 84: Flight Booking Management System")
            self.setStrokeColor(colors.HexColor("#D0D7DE"))
            self.setLineWidth(0.5)
            self.line(45, 747, 567, 747)

        # Footer
        self.drawString(45, 30, "Academic Viva & Project Defense Guide (Hinglish) — Prepared for Aditya Sao")
        self.drawRightString(567, 30, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#D0D7DE"))
        self.setLineWidth(0.5)
        self.line(45, 42, 567, 42)
        self.restoreState()


def create_viva_guide():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'MainTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=16, leading=20,
        textColor=colors.HexColor('#003366'), alignment=1, spaceAfter=4
    )
    sub_title = ParagraphStyle(
        'SubTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=14,
        textColor=colors.HexColor('#005580'), alignment=1, spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'Heading1', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=11, leading=15,
        textColor=colors.HexColor('#003366'), spaceBefore=9, spaceAfter=4, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=colors.HexColor('#005580'), spaceBefore=6, spaceAfter=3, keepWithNext=True
    )
    body = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.3, leading=11.3,
        textColor=colors.HexColor('#1F2328'), spaceAfter=3
    )
    hin = ParagraphStyle(
        'Hin', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.3, leading=11.3,
        textColor=colors.HexColor('#111111'), spaceAfter=3
    )
    q_title = ParagraphStyle(
        'QTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=11.5,
        textColor=colors.HexColor('#003366'), spaceBefore=4, spaceAfter=1
    )
    ans_text = ParagraphStyle(
        'AnsText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.2, leading=11.2,
        textColor=colors.HexColor('#222222'), spaceAfter=4
    )

    story = []

    # =========================================================================
    # HEADER & METADATA TABLE
    # =========================================================================
    story.append(Paragraph("FLIGHT BOOKING MANAGEMENT SYSTEM", title_style))
    story.append(Paragraph("COMPLETE ACADEMIC VIVA & PRESENTATION GUIDE (HINGLISH + ENGLISH)", sub_title))
    
    meta = [
        [Paragraph("<b>Student Name:</b> Aditya Sao", body),
         Paragraph("<b>Class:</b> B.Tech CSE (First Year)", body)],
        [Paragraph("<b>Course:</b> Programming Fundamentals Using Python", body),
         Paragraph("<b>Problem Statement:</b> Problem Statement No. 84", body)],
        [Paragraph("<b>Institution:</b> Rungta International Skills University", body),
         Paragraph("<b>Language & Stack:</b> Pure Python 3 (Standard Library)", body)]
    ]
    t_m = Table(meta, colWidths=[261, 261])
    t_m.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F4F7FB')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#B0C4DE')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DCE5F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_m)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 1: 1-MINUTE ELEVATOR PITCH
    # =========================================================================
    story.append(Paragraph("1. Project Overview & 1-Minute Elevator Pitch (Examiner ke Saamne Kya Bolna Hai)", h1_style))
    pitch_text = (
        "<b>Examiner ko Hindi/English mix me kaise start karein:</b><br/>"
        "<i>\"Good morning Sir/Ma'am, mera project hai <b>Flight Booking Management System (Problem Statement No. 84)</b>. "
        "Yeh ek pure Python 3 console application hai jo commercial flight schedules ko <code>flights.csv</code> dataset se load karta hai. "
        "Isme commuter origin aur destination dekar case-insensitive flights search kar sakta hai, seat booking karne par automatic total fare "
        "<code>seats * fare</code> calculate hota hai aur available seats decrement ho jati hain. "
        "Agar passenger booking cancel kare to system inventory me exact seats restore kar deta hai. "
        "Maine isme Object-Oriented Programming (OOP) ka <code>Flight</code> class use kiya hai aur kisi bhi external library ki jarurat nahi hai.\"</i>"
    )
    t_pitch = Table([[Paragraph(pitch_text, hin)]], colWidths=[522])
    t_pitch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EBF3FB')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#005580')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_pitch)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 2: PYTHON CONCEPTS & DATA STRUCTURES MATRIX
    # =========================================================================
    story.append(Paragraph("2. Core Python Concepts & Data Structures Matrix", h1_style))
    concepts = [
        ["Concept", "Code Me Kahan Hai?", "Viva Me Explain Kaise Karein?"],
        ["Class & Objects\n(OOP Encapsulation)",
         "class Flight:\n  def __init__(...)\n  book_seats()\n  cancel_seats()",
         "Flight ka data (number, cities, seats, fare) aur uske operations (seat booking, cancel) ko ek sath bind karne ke liye OOP class use ki hai."],
        ["File Persistence\n(CSV I/O)",
         "csv.DictReader(f)\ncsv.writer(f)\nwith open('flights.csv') as f:",
         "Program restart hone par bhi seat counts aur bookings safe rahein isliye CSV files use ki hain. 'with' context manager file ko auto-close karta hai."],
        ["Lists & List Comprehensions",
         "matches = [f.format_search_result()\nfor f in flights if f.matches_route(...)]",
         "1,000 flights ko in-memory hold karne ke liye List of Flight objects use kiya hai. List comprehension se route filtering fast aur clean hoti hai."],
        ["Dictionary\n(Key-Value Lookup)",
         "bookings = {\n  'BK1': {'Passenger': ...}\n}",
         "Bookings ko Booking ID se directly access karne ke liye Dictionary use ki hai. Iska average search time O(1) hota hai."],
        ["Defensive Input Validation",
         "try:\n  num_seats = int(seats_str)\nexcept ValueError:",
         "User agar negative seat, zero, ya alphabetical text daale to code crash nahi hota balki user-friendly error message deta hai."],
        ["Case-Insensitive String Methods",
         "origin.lower() ==\nquery.lower()",
         "User capital me 'RAIPUR' likhe ya small me 'raipur', program bina error ke accurate match karta hai."]
    ]
    t_c = Table(concepts, colWidths=[95, 175, 252])
    t_c.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F9FBFD'), colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_c)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 3: TOP RAPID-FIRE VIVA QUESTIONS & ANSWERS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Top 20 Rapid-Fire Viva Questions & Best Answers", h1_style))
    story.append(Paragraph("Examiner aam taur par ye questions direct puchte hain. Inhe simple Hindi + English mix me confident ho kar answer karein:", hin))
    story.append(Spacer(1, 3))

    qa_list = [
        ("Q1: Problem Statement No. 84 ka main objective kya hai?",
         "<b>Answer:</b> Problem Statement 84 ka main goal ek Object-Oriented Flight Booking program banana hai jisme: (1) Class Flight ho, (2) flights.csv se flight data load ho, (3) Origin & Destination se search ho, (4) Booking hone par seats count ghate aur total = seats * fare calculate ho, aur (5) Cancellation par seats wapas add ho jayein bina inventory corrupt hue."),

        ("Q2: Class 'Flight' me kaunse attributes aur methods hain?",
         "<b>Answer:</b> Attributes: <code>flight_no</code>, <code>origin</code>, <code>destination</code>, <code>seats</code>, aur <code>fare</code>.<br/>"
         "Methods: <code>matches_route()</code> (route check), <code>book_seats()</code> (capacity check karke seats deduct karna), <code>cancel_seats()</code> (seats restore karna), aur <code>format_search_result()</code> (display format)."),

        ("Q3: Total Fare calculation ka formula kya hai?",
         "<b>Answer:</b> <code>total_fare = num_seats * flight.fare</code>. Example: Agar user flight AI202 ki 2 seats book karta hai jiska fare Rs. 5500 hai, to total fare $2 \\times 5500 = 11,000$ INR banta hai."),

        ("Q4: Seat count ki consistency (integrity) kaise maintain hoti hai?",
         "<b>Answer:</b> Booking ke waqt <code>flight.seats -= num_seats</code> hota hai aur turant <code>save_flights()</code> se CSV file me update ho jata hai. Cancellation ke waqt <code>flight.seats += booking['Seats']</code> hota hai aur dobara file save hoti hai. Isse system restart hone par bhi seat counts strictly exact rehti hain."),

        ("Q5: Agar user flight me available seats se zyada seats maange (Overbooking)?",
         "<b>Answer:</b> Code me check lagaya hai: <code>if num_seats > self.seats: raise ValueError('Only X seat(s) available on flight.')</code>. Isse system overbooking reject kar deta hai aur flight inventory negative nahi hoti."),

        ("Q6: Agar flight me 0 seats bachi hon (Flight Full) tab kya hoga?",
         "<b>Answer:</b> Code check karta hai <code>if self.seats == 0: raise ValueError(f'Flight {self.flight_no} is full.')</code>. Booking cancel ho jati hai aur clear message print hota hai."),

        ("Q7: Agar user negative ya zero seats (-2 ya 0) enter kare?",
         "<b>Answer:</b> Code me rule hai <code>if num_seats < 1: raise ValueError('Number of seats must be at least 1.')</code>. Iske alawa <code>seats_str.isdigit()</code> se alphabetic ya special character inputs bhi filter ho jate hain."),

        ("Q8: Unique Booking ID (BK1, BK2, ...) kaise generate hoti hai?",
         "<b>Answer:</b> System <code>bookings.csv</code> ke existing keys scan karta hai, numeric suffix extract karta hai (jaise 'BK1' se 1), highest number nikalta hai aur <code>max + 1</code> karke naya ID banata hai. Kabhi duplicate ID nahi banta."),

        ("Q9: Case-insensitive search kaise achieve kiya?",
         "<b>Answer:</b> String function <code>.lower()</code> use karke. <code>self.origin.lower() == origin.strip().lower()</code>. User chahe 'RAIPUR', 'Raipur', ya 'raipur' likhe, exact match hota hai."),

        ("Q10: flights.csv me kitna data hai?",
         "<b>Answer:</b> Dataset me 1,000 commercial flights ka data hai jo major airlines (Air India, IndiGo, SpiceJet, Vistara, Akasa Air) ke routes aur domestic/international airports cover karta hai."),

        ("Q11: File open karte waqt 'with open()' kyun use kiya?",
         "<b>Answer:</b> 'with' statement Python ka Context Manager hai. Yeh ensure karta hai ki file read ya write hone ke baad automatically close ho jaye, chahe code me error aaye ya na aaye. Isse memory leaks aur locked files nahi hoti."),

        ("Q12: csv.DictReader aur normal csv.reader me kya difference hai?",
         "<b>Answer:</b> <code>csv.reader</code> data ko list of lists ke form me deta hai jisme index (row[0], row[1]) yaad rakhna padta hai. Jabki <code>csv.DictReader</code> header row ko keys bana kar dictionary deta hai (jaise <code>row['Seats']</code>), jo zyada safe aur readable hai."),

        ("Q13: Agar ek cancelled booking ko koi wapas cancel karne ki koshish kare?",
         "<b>Answer:</b> System check karta hai <code>if booking['Status'] == 'CANCELLED': print('Booking BK1 is already cancelled.')</code>. Isse double seat restoration ki bug prevent hoti hai."),

        ("Q14: External database (MySQL / SQLite) ki jagah CSV kyun use kiya?",
         "<b>Answer:</b> Problem statement me specifically <code>flights.csv</code> se load karne ko kaha gaya tha. CSV file human-readable hoti hai, lightweight hai, aur bina kisi heavy SQL server ke Python standard library se directly handle ho jati hai."),

        ("Q15: Aapke code ka Time Complexity kya hai?",
         "<b>Answer:</b> Route search ka time complexity $O(N)$ hai kyunki yeh 1,000 flights ko ek baar iterate karta hai. Booking ID lookup $O(1)$ constant time hai dictionary hashing ki wajah se.")
    ]

    for q, a in qa_list:
        story.append(Paragraph(q, q_title))
        story.append(Paragraph(a, ans_text))
        story.append(Spacer(1, 1))

    # =========================================================================
    # SECTION 4: EXAMINER TRAP QUESTIONS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Examiner 'Trap Questions' & How to Defend Confidently", h1_style))
    story.append(Paragraph("Examiner student ka deep logic test karne ke liye aksar aise tricky questions puchte hain:", hin))
    story.append(Spacer(1, 3))

    traps = [
        ("Trap 1: 'Kya do users ek sath book karein to concurrency issue aayega?'",
         "<b>Answer:</b> 'Sir, yeh ek single-threaded console application hai jisme CLI user inputs sequentially process hote hain. Real-world airline systems me multi-threading ya distributed transactions (like ACID locks ya Redis locks) use hote hain, lekin academic PS No. 84 ke single-user console scope me atomic file read-write sequentially seat integrity maintain rakhti hai.'"),

        ("Trap 2: 'Aapne AI slop kyun hataya? Purane code me itne saare classes the.'",
         "<b>Answer:</b> 'Sir, original code me over-engineering thi—6 custom exception classes, temporary file atomic swappers, aur file loggers jo is problem ke required logic ke liye bilkul unnecessary the. Humne code ko clean, concise (~250 lines), aur beginner-friendly banaya jo seedha Problem Statement 84 ke core rules ko implement karta hai.'"),

        ("Trap 3: 'Agar flights.csv file achanak delete ho jaye to code crash hoga?'",
         "<b>Answer:</b> 'Sir, <code>load_flights()</code> me <code>if not os.path.exists(FLIGHTS_FILE): return flights</code> laga hua hai. Agar file nahi hogi to code crash nahi karega, balki empty list return karega aur menu smooth run hota rahega.'"),

        ("Trap 4: 'Aapne Pandas ya NumPy use kyun nahi kiya?'",
         "<b>Answer:</b> 'Sir, Python standard library ka <code>csv</code> module lightweight hai aur zero-dependency execution deta hai. Kisi bhi system par bina <code>pip install</code> kiye yeh project out-of-the-box run ho jata hai.'")
    ]

    for q, a in traps:
        story.append(Paragraph(q, q_title))
        story.append(Paragraph(a, ans_text))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 4))

    # =========================================================================
    # SECTION 5: LIVE VIVA DEMO CHECKLIST
    # =========================================================================
    story.append(Paragraph("5. Step-by-Step Live Terminal Demo Checklist", h1_style))
    story.append(Paragraph("Examiner ke samne practical viva me in steps ko sequence me perform karein:", hin))

    steps_data = [
        ["Step #", "Action / Input", "Expected Terminal Output", "Examiner ko Kya Dikhana Hai"],
        ["Step 1", "python main.py", "Banner + Main Menu (1-7)", "Clean startup without errors."],
        ["Step 2", "Option 1: Raipur -> Delhi", "AI101 | Raipur -> Delhi | Seats: 5 | Fare: Rs. 6000", "Case-insensitive route search (Test Case 1)."],
        ["Step 3", "Option 2: Book AI202 (2 seats)", "Booking confirmed. ID: BK1 ... Seats left: 0", "Boundary booking: Remaining seats become 0 (Test Case 2)."],
        ["Step 4", "Option 2: Book AI303 (1 seat)", "Flight AI303 is full.", "Capacity check: Full flight rejection (Test Case 3a)."],
        ["Step 5", "Option 2: Book AI101 (6 seats)", "Only 5 seat(s) available on AI101.", "Overbooking rejection: Requested > Available (Test Case 3b)."],
        ["Step 6", "Option 2: Book AI101 (0 seats)", "Number of seats must be at least 1.", "Boundary check: Non-positive input rejection (Test Case 3c)."],
        ["Step 7", "Option 2: Book AI101 (3 seats)", "Booking confirmed. ID: BK2 ... Seats left: 2", "Seat reduction from 5 to 2."],
        ["Step 8", "Option 3: Cancel BK2", "Booking BK2 cancelled. Seats left on AI101: 5", "State Restoration: Seats returned back to 5 (Test Case 4)."]
    ]
    t_steps = Table(steps_data, colWidths=[40, 125, 175, 182])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F4F7FB'), colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_steps)

    # Build document
    doc.build(story, canvasmaker=PageNumCanvas)
    print(f"Viva Guide successfully generated at: {PDF_PATH}")


if __name__ == "__main__":
    create_viva_guide()
