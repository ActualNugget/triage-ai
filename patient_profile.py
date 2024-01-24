import pandas as pd 
from pathlib import Path
from collections import namedtuple
from random import randint

#get data from excel file
folder_path = Path(__file__).parent.resolve()
input_conditions_path = Path(__file__).parent / "input_conditions.xlsx"
pd.set_option('display.max_rows', None) 
pd.set_option('display.max_columns', None)
df = pd.read_excel(input_conditions_path)

#turn each possible case into an object
possible_case = namedtuple ("case", ["condition", "priority", "facilities", "in_or_out"])
cases = []
facilities_list = []

for index, row in df.iterrows():
    row = df.iloc[index]
    priority = int(row['Priority'])
    condition = row['Examples']
    facilities = list(row['Facilities'].split(", "))
    in_or_out = int(row['In/outpatient'])
    temp = possible_case(condition, priority, facilities, in_or_out)
    cases.append(temp)
    for facility in facilities:
        facilities_list.append(facility)

facilities_list = set(facilities_list)

#generate random patient cases
N = len(cases)
    
def generate_random_patient(num_cases, cases_list):
    patient_profile = {}
    i = randint(0, num_cases-1)
    case = cases_list[i]
    if case.in_or_out == 2:
        case.in_or_out = randint(0,1)
        if (condition == "Cataracts" or condition == "Limb fractor/ dislocation") and in_or_out == 0:
            case.facilities.remove("Operating Theatre")
    if case.in_or_out == 0:
        status = "Outpatient"
    elif case.in_or_out == 1:
        status = "Inpatient"
    patient_profile.update({
        'Condition' : case.condition,
        'Priority' : case.priority,
        'Facilities Required' : case.facilities,
        'Inpatient/Outpatient' : status,
    })
    
    return patient_profile

p1_cases = [case for case in cases if case.priority == 1]
p2_cases = [case for case in cases if case.priority == 2]
p3_cases = [case for case in cases if case.priority == 3]
p4_cases = [case for case in cases if case.priority == 4]

print(p1_cases)