from scheduler import assign_schedule
import csv
import json

schedule = assign_schedule()

# Create a CSV file
with open("schedule_output.csv", "w", newline="") as csvfile:
    fieldnames = ["date", "staff", "shift", "start", "end"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for date, entries in schedule.items():
        for entry in entries:
            writer.writerow({
                "date": date,
                "staff": entry["staff"],
                "shift": entry["shift"],
                "start": entry["start"],
                "end": entry["end"]
            })

print("Schedule exported to schedule_output.csv")
