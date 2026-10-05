"""
Bunk & Recovery Calculator for Attendance.
Target default: 75%
"""
import math

def calculate_bunk_status(attended: int, total: int, target_percent: float = 75.0) -> dict:
    if total == 0:
        return {
            "percentage": 100.0,
            "status": "Safe",
            "margin_type": "bunk",
            "classes_count": 0,
            "message": "No classes conducted yet."
        }

    percentage = round((attended / total) * 100, 2)
    threshold = target_percent / 100.0

    if percentage >= target_percent:
        max_bunks = int((attended - (threshold * total)) / threshold)
        return {
            "percentage": percentage,
            "status": "Safe",
            "margin_type": "bunk",
            "classes_count": max_bunks,
            "message": f"Can miss next {max_bunks} class{'es' if max_bunks != 1 else ''} safely!" if max_bunks > 0 else "Borderline! Don't miss next class."
        }
    else:
        needed = math.ceil(((threshold * total) - attended) / (1 - threshold))
        return {
            "percentage": percentage,
            "status": "Low",
            "margin_type": "attend",
            "classes_count": needed,
            "message": f"Must attend next {needed} class{'es' if needed != 1 else ''} consecutively to reach {target_percent}%!"
        }
