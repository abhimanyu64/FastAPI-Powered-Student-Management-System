
import csv
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

CSV_FILE = "students.csv"
API_URL = "http://127.0.0.1:5500/students"

added = 0
skipped = 0
failed = 0

try:
    with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required = {"name", "email", "course", "year"}
        headers = {h.strip().lower() for h in (reader.fieldnames or [])}

        if not required.issubset(headers):
            raise ValueError(
                "CSV must contain these columns: name, email, course, year"
            )

        for line_number, row in enumerate(reader, start=2):
            # Normalize column names and values
            row = {
                key.strip().lower(): (value or "").strip()
                for key, value in row.items()
                if key is not None
            }

            try:
                student = {
                    "name": row["name"],
                    "email": row["email"],
                    "course": row["course"],
                    "year": int(row["year"]),
                }

                if not all([
                    student["name"],
                    student["email"],
                    student["course"],
                ]):
                    raise ValueError("Name, email and course are required")

                request = Request(
                    API_URL,
                    data=json.dumps(student).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )

                with urlopen(request, timeout=10) as response:
                    result = json.loads(
                        response.read().decode("utf-8")
                    )
                    print(
                        f"ADDED: ID={result['id']} | "
                        f"{result['name']} | {result['email']}"
                    )
                    added += 1

            except HTTPError as error:
                message = error.read().decode("utf-8")
                if error.code == 409:
                    print(f"SKIPPED duplicate email on row {line_number}")
                    skipped += 1
                else:
                    print(
                        f"FAILED row {line_number}: "
                        f"HTTP {error.code} - {message}"
                    )
                    failed += 1

            except (ValueError, KeyError) as error:
                print(f"INVALID row {line_number}: {error}")
                failed += 1

            except URLError as error:
                print(f"Cannot connect to backend: {error.reason}")
                print("Check that the backend is running on port 5500.")
                break

except FileNotFoundError:
    print(f"CSV file not found: {CSV_FILE}")
    print("Place students.csv in the main project folder.")

except (OSError, ValueError) as error:
    print(f"Import could not start: {error}")

print("\n========== IMPORT SUMMARY ==========")
print(f"Added:   {added}")
print(f"Skipped: {skipped}")
print(f"Failed:  {failed}")
