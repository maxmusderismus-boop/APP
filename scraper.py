"""
AEC Portal Scraper & HTML Table Parser.
"""
import requests
from bs4 import BeautifulSoup
from bunk_calculator import calculate_bunk_status

BASE_URL = "https://info.aec.edu.in/aus"
LOGIN_URL = f"{BASE_URL}/default.aspx"
ATTENDANCE_URL = f"{BASE_URL}/Attendance.aspx"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def parse_attendance_html(html_content: str, target_percent: float = 75.0) -> dict:
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table")

    subjects = []
    overall_total = 0
    overall_attended = 0

    for table in tables:
        rows = table.find_all("tr")
        if not rows:
            continue

        for row in rows:
            cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
            if len(cols) < 4:
                continue

            try:
                total_val = None
                attended_val = None
                subject_name = cols[0]

                for i in range(1, len(cols)):
                    val = cols[i].replace("%", "").strip()
                    if val.isdigit():
                        if total_val is None:
                            total_val = int(val)
                        elif attended_val is None:
                            attended_val = int(val)

                if total_val is not None and attended_val is not None and total_val > 0:
                    status_info = calculate_bunk_status(attended_val, total_val, target_percent)
                    subjects.append({
                        "subject": subject_name,
                        "total": total_val,
                        "attended": attended_val,
                        "percentage": status_info["percentage"],
                        "bunk_info": status_info
                    })
                    overall_total += total_val
                    overall_attended += attended_val
            except Exception:
                continue

    overall_status = calculate_bunk_status(overall_attended, overall_total, target_percent)

    return {
        "overall": {
            "total": overall_total,
            "attended": overall_attended,
            "percentage": overall_status["percentage"],
            "bunk_info": overall_status
        },
        "subjects": subjects
    }

def fetch_attendance(roll_number: str, target_percent: float = 75.0) -> dict:
    session = requests.Session()
    session.headers.update(HEADERS)

    # 1. Fetch ASP.NET tokens
    res = session.get(LOGIN_URL, verify=False, timeout=15)
    soup = BeautifulSoup(res.text, "html.parser")

    viewstate = soup.find("input", {"id": "__VIEWSTATE"})
    viewstate_val = viewstate["value"] if viewstate else ""
    event_val = soup.find("input", {"id": "__EVENTVALIDATION"})
    event_val_val = event_val["value"] if event_val else ""
    generator = soup.find("input", {"id": "__VIEWSTATEGENERATOR"})
    generator_val = generator["value"] if generator else ""

    # 2. Submit student roll number
    payload = {
        "__VIEWSTATE": viewstate_val,
        "__VIEWSTATEGENERATOR": generator_val,
        "__EVENTVALIDATION": event_val_val,
        "userType": "rbtStudent",
        "txtUserId": roll_number.strip(),
        "txtPassword": "",
        "btnLogin": "LOGIN"
    }

    session.post(LOGIN_URL, data=payload, verify=False, timeout=15)

    # 3. Request Attendance page
    att_res = session.get(ATTENDANCE_URL, verify=False, timeout=15)

    # 4. Parse table
    return parse_attendance_html(att_res.text, target_percent)
