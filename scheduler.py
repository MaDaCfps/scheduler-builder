import json
from datetime import datetime, timedelta


def load_data():
    with open("data/staff.json", "r") as f:
        staff = json.load(f)
    with open("data/shifts.json", "r") as f:
        shifts = json.load(f)
    with open("data/store_hours.json", "r") as f:
        store_hours = json.load(f)
    return staff, shifts, store_hours


def to_hours(start, end):
    start_dt = datetime.strptime(start, "%H:%M")
    end_dt = datetime.strptime(end, "%H:%M")
    return (end_dt - start_dt).seconds / 3600


def assign_schedule():
    staff_list, shifts, store_hours = load_data()

    # Track hours worked
    for staff in staff_list:
        staff["hours_scheduled"] = 0

    today = datetime.today()
    schedule = {}

    for i in range(7):  # For the next 7 days
        date = today + timedelta(days=i)
        day_name = date.strftime("%a").lower()
        schedule[date.strftime("%Y-%m-%d")] = []

        for shift in shifts:
            for staff in sorted(staff_list, key=lambda s: -s["seniority"]):
                available = staff["availability"].get(day_name, [])
                if not available:
                    continue

                if date.strftime("%Y-%m-%d") in staff["time_off"]:
                    continue

                # Is staff available during the shift?
                if available[0] <= shift["start"] and available[1] >= shift["end"]:
                    shift_hours = to_hours(shift["start"], shift["end"])
                    if staff["hours_scheduled"] + shift_hours <= staff["max_hours"]:
                        schedule[date.strftime("%Y-%m-%d")].append({
                            "staff": staff["name"],
                            "shift": shift["name"],
                            "start": shift["start"],
                            "end": shift["end"]
                        })
                        staff["hours_scheduled"] += shift_hours
                        break  # Move to the next shift

    return schedule
