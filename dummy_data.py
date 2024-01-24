import pandas as pd 
from pathlib import Path
from collections import namedtuple
from random import randint
import patient_profile

#get data from excel file
folder_path = Path(__file__).parent.resolve()
dummydata_path = Path(__file__).parent / "dummydata.xlsx"
dummydata_excel = pd.ExcelFile(dummydata_path)

df_1 = dummydata_excel.parse("TimeSeries")
df_2 = dummydata_excel.parse("Probability Distribution")


# Creating a dictionary where each object is month_number: [p1, p2, p3, p4]
# p1, p2, p3, p4 = the probability of a patient coming in with the corresponding priority level
year_probDist = {}

for index, row in df_2.iterrows():
    row = df_2.iloc[index]
    month = int(row['Month'])
    p1 = row['A']
    p2 = row['B']
    p3 = row['C']
    p4 = row['D']
    ttl = row["Total Attendance"] #total attendance = average number of a&e patients/ week for that month

    month_dist = [p1, p2, p3, p4]
    year_probDist.update({
        month : [month_dist, ttl]
    })

#Setting up Probability Distribution workbook
facilities = patient_profile.facilities_list
for facility in facilities:
    df_1[facility] = 0 #Setting all inital facilities count to 0


#importing the different cases that could occur under each priority level
x = [patient_profile.p1_cases, patient_profile.p2_cases, patient_profile.p3_cases, patient_profile.p4_cases]

#iterating over each week in order to get the number of times each facility is needed
for index, row in df_1.iterrows():
    # determining the set of p1-4 for the month
    r = df_1.iloc[index]["Date"]
    month = pd.to_datetime(r).month
    probs = year_probDist[month][0]

    # determining the weekly average attendance for the month
    avg_pop = year_probDist[month][1]

    # determining the average population of patients per priority level
    pop_p1 = (probs[0]/100)*avg_pop
    pop_p2 = (probs[1]/100)*avg_pop
    pop_p3 = (probs[2]/100)*avg_pop
    pop_p4 = (probs[3]/100)*avg_pop

    pop_list = [pop_p1, pop_p2, pop_p3, pop_p4]

    # randomly generating cases to get the corresponding facilities count for that week
    for i in range(4):
        for person in range(int(pop_list[i])):
            case_index = randint(0,len(x[i])-1)
            case = x[i][case_index]
            for facility in case.facilities:
                df_1.at[index, facility] += 1
    # progress checker
    print(index/(df_1.shape[0])) 

print(df_1)


 

