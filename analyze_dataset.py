
import pandas as pd
import numpy as np

CSV_FILE = "students.csv"  # Change this if your CSV is elsewhere

df = pd.read_csv(CSV_FILE)
df.columns = df.columns.str.strip().str.lower()

required = {"name", "email", "course", "year"}
if not required.issubset(df.columns):
    raise ValueError("CSV must contain name, email, course, year columns")

df["year"] = pd.to_numeric(df["year"], errors="coerce")
years = df["year"].dropna().to_numpy(dtype=float)
years = years[np.isfinite(years)]

print("=== Student Dataset Analysis ===")
print("Total rows:", len(df))
print("Unique email addresses:", df["email"].astype(str).str.strip().str.lower().nunique())

print("\nStudents by course:")
print(df.groupby("course")["name"].count().sort_values(ascending=False))

if len(years):
    print("\nAcademic Year Statistics (NumPy)")
    print("Minimum:", np.min(years))
    print("Maximum:", np.max(years))
    print("Mean:", round(float(np.mean(years)), 2))
    print("Median:", float(np.median(years)))
    print("Years outside 1-8:", int(np.sum((years < 1) | (years > 8))))

print("\nDataset preview:")
print(df.head(10).to_string(index=False))
