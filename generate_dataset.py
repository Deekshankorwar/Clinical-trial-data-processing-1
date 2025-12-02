import csv
import random
import datetime

# Generate a random date between start and end
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + datetime.timedelta(days=random_days))

# Sample data lists
diseases = ["Diabetes", "Hypertension", "Cancer", "Asthma", "Arthritis"]
treatments = ["Drug A", "Drug B", "Drug C", "Therapy X", "Therapy Y"]
outcomes = ["Improved", "No Change", "Worsened"]
genders = ["Male", "Female"]

# Generate dataset for 100 patients
num_patients = 100
rows = []

for pid in range(1, num_patients + 1):
    name = f"Patient{pid}"
    age = random.randint(20, 80)
    gender = random.choice(genders)
    disease = random.choice(diseases)
    treatment = random.choice(treatments)
    outcome = random.choice(outcomes)
    dosage_mg = random.choice([50, 100, 150, 200, 250])

    start_date = random_date(datetime.date(2025, 1, 1), datetime.date(2025, 12, 31))
    end_date = random_date(start_date, datetime.date(2025, 12, 31))

    rows.append([pid, name, age, gender, disease, treatment,
                 dosage_mg, start_date, end_date, outcome])

# Save CSV
with open("clinical_trial_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["PatientID", "Name", "Age", "Gender", "Disease", "Treatment",
                     "Dosage(mg)", "StartDate", "EndDate", "Outcome"])
    writer.writerows(rows)

print("Dataset generated: clinical_trial_data.csv")