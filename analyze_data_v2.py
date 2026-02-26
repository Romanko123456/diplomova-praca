
import csv
import math
import os

data_dir = r"c:\Users\Legion\Desktop\skola\DPText\data_csv"

def read_csv(filename):
    path = os.path.join(data_dir, filename)
    data = []
    # Try cp1250 (central european) or latin1
    encoding = 'cp1250'
    
    with open(path, 'r', encoding=encoding) as f:
        reader = csv.reader(f)
        # Manually parse to handle potential BOM or weird format
        lines = [row for row in reader]

    # Find stats start
    data_start = 0
    for i, row in enumerate(lines):
        if len(row) > 0 and "Respondent" in row[0]:
            data_start = i + 1
            break
            
    parsed_data = []
    for row in lines[data_start:]:
        if not row: continue
        # Check if first column is number
        try:
             int(row[0])
             parsed_data.append(row)
        except:
             continue
             
    return parsed_data

def calculate_stats(data, index):
    values = []
    for row in data:
        try:
            val = float(row[index].replace(',', '.')) # Handle decimal comma
            values.append(val)
        except:
            pass
    
    if not values: return 0.0, 0.0, 0.0, 0.0
    
    n = len(values)
    mean = sum(values) / n
    variance = sum([(x - mean) ** 2 for x in values]) / (n - 1) if n > 1 else 0
    sd = math.sqrt(variance)
    return mean, sd, min(values), max(values)

# --- Process ITF Group ---
# Columns:
# 0: Resp, 1: Gender, 2: Age, 3: Height, 4: Weight, 5: Job, 6: Pain PRE, 7: Char, 8: When, 9: Stiffness
print("\n--- ITF Group ---")
itf_data = read_csv("ITF + kinezioterapia.csv")
print(f"Sample size: {len(itf_data)}")
m, s, mn, mx = calculate_stats(itf_data, 6)
print(f"Pain PRE (VAS): Mean={m:.2f}, SD={s:.2f}, Min={mn}, Max={mx}")

# Morning stiffness count (col 9: 1=Yes, 2=No)
yes = 0
no = 0
for row in itf_data:
    try:
        if int(row[9]) == 1: yes += 1
        elif int(row[9]) == 2: no += 1
    except: pass
print(f"Morning Stiffness (PRE): Yes={yes}, No={no}")

# --- Process Kinezioterapia Group ---
print("\n--- Kinezioterapia Group ---")
kin_data = read_csv("Kinezioterapia.csv")
print(f"Sample size: {len(kin_data)}")
m, s, mn, mx = calculate_stats(kin_data, 6)
print(f"Pain PRE (VAS): Mean={m:.2f}, SD={s:.2f}")

yes = 0
no = 0
for row in kin_data:
    try:
        if int(row[9]) == 1: yes += 1
        elif int(row[9]) == 2: no += 1
    except: pass
print(f"Morning Stiffness (PRE): Yes={yes}, No={no}")

# --- Process Questionnaires (Post-treatment & comparison) ---
# Inspect columns of "ITF Questionnaire"
# Based on prev output: 
# Row 0: Kdovanie | seln hodnota (0-10) |  | seln hodnota (0-10) | ...
# Row 1: Respondent . | 1. ADL |  | 2.Boles pri chdzi |  | ...
# Row 2: | Pred | Po | ...
# So data starts at line 4 (index 3 if 0-based)?
# And columns are paired: 
# 1: ADL Pred, 2: ADL Po
# 3: Walking Pain Pred, 4: Walking Pain Po
# 5: Stiffness Pred, 6: Stiffness Po
# 7: Fatigue Pred, 8: Fatigue Po
# 9: Joint Pain Pred, 10: Joint Pain Po (guessing based on pattern)

print("\n--- Questionnaire ITF ---")
q_itf = read_csv("Dotazník ITF.csv")
# Analyze ADL (col 1=Pred, 2=Po) -> indices might be offset by 1 because col 0 is Respondent
# Actually indices in python list: 
# 0: Resp
# 1: ADL Pred
# 2: ADL Po
# 3: Walking Pred
# 4: Walking Po
# 5: Stiffness Pred
# 6: Stiffness Po
# 7: Fatigue Pred
# 8: Fatigue Po
# 9: Joint Pain Pred
# 10 or 11?: There might be empty cols

print(f"First row sample: {q_itf[0]}")
m_pre, s_pre, _, _ = calculate_stats(q_itf, 1)
m_post, s_post, _, _ = calculate_stats(q_itf, 2)
print(f"ADL: Pred [{m_pre:.2f}, {s_pre:.2f}] -> Po [{m_post:.2f}, {s_post:.2f}]")

print("\n--- Questionnaire Kinezioterapia ---")
q_kin = read_csv("Dotazník Kinezioterapia.csv")
m_pre, s_pre, _, _ = calculate_stats(q_kin, 1)
m_post, s_post, _, _ = calculate_stats(q_kin, 2)
print(f"ADL: Pred [{m_pre:.2f}, {s_pre:.2f}] -> Po [{m_post:.2f}, {s_post:.2f}]")
