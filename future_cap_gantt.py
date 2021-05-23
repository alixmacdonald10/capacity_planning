'''
The following script plots the capacity of hte engineering department
with respect to the future potential jobs
'''


from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.express as px


# Define the capacity of the department
# personnel
engineers = 4
# project work capacity
cap_fact = 0.6

# working hours in a year
days_hol = 33
weeks_in_year = 52
work_hours_per_day = 8.5
work_hours_per_year = ((weeks_in_year * 5) - days_hol) * work_hours_per_day
print(f'Work Hours Per Year = {work_hours_per_year}')
department_work_hours_per_year = engineers * work_hours_per_year
print(
    f'Total yearly departmental work hours = {department_work_hours_per_year}'
)

# determine work hours left
day_of_year = datetime.now().timetuple().tm_yday
perc_year_passed = 1 - ((365 - day_of_year) / 365)
yearly_work_hours_remaining = (1 - perc_year_passed) * department_work_hours_per_year
indv_yearly_work_hours_remaining = yearly_work_hours_remaining / engineers
print(
    f'Day number (today) = {day_of_year}',
     f'\nPercentage of year passed = {perc_year_passed}',
     f'\nDepartmental work hours remaining this year = {yearly_work_hours_remaining}'
)

# Time for specific projects
std_engineered = 172
bespoke = 686

# project info

project = [
    "Pontsticill",
    "Crossness: Low and High Level Spare/replacement",
    "East Hull Spare Pump",
    "Iraq Vertical Mixed Flow Pumps",
    "Cam & Wickers Brook P.S.",
    "Cuckoo Lane",
    "The Bristol Port Company: Dock Dewatering Pumps",
    "Catoca Phase 3",
    "Anderby PS",
    "Ingoldmells",
    "Saltfleet",
    "Chittagong Development Authority Project – Moheshkhal Pumping Station",
    "Trusthorpe",
    "Hildenborough",
    "Long Load - Small Pump",
    "Westover Pumping Station",
    "Northmoor Pumping Station",
    "North Drain Pumping Station",
    "Midelney Pumping Station",
    "Huish Pumping Station",
    "Long Load - Large Pumps",
    "Stourmouth",
    "Clifton Ings",
    "Rosneft 2",
    "Filter Feed Pumps (Screw Pumps Replacement - Sharjah"
]

value = [
    32751.00,
    238507.00,
    190000.00,
    378500.00,
    118000.00,
    266000.00,
    2292702.00,
    363879.00,
    300000.00,
    500000.00,
    800000.00,
    2899456.00,
    400000.00,
    150000.00,
    55839.00,
    253607.00,
    110295.00,
    392637.00,
    336201.00,
    402259.00,
    413315.00,
    200000.00,
    130000.00,
    309800.00,
    140000.00
]

probability = [
    75,
    75,
    50,
    75,
    75,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    75,
    50,
    50,
    50,
    50,
    50,
    75,
    50,
    50,
    75,
    50,
    50
]

expected_date = [
    "2021-05-01",
    "2021-05-01",
    "2021-06-01",
    "2021-06-01",
    "2021-06-01",
    "2021-06-01",
    "2021-06-01",
    "2021-06-01",
    "2021-07-01",
    "2021-07-01",
    "2021-07-01",
    "2021-07-01",
    "2021-07-01",
    "2021-08-01",
    "2021-08-01",
    "2021-08-01",
    "2021-08-01",
    "2021-08-01",
    "2021-08-01",
    "2021-08-01",
    "2021-08-01",
    "2021-08-01",
    "2021-09-01",
    "2021-10-01",
    "2021-12-01"
]

difficulty = [
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Bespoke Engineered",
    "Std Engineered",
    "Std Engineered",
    "Bespoke Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Bespoke Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Std Engineered",
    "Bespoke Engineered"
]

# Create dataframe
df = pd.DataFrame(
    list(zip(project, value, probability, expected_date, difficulty)),
               columns =["project", "value", "probability", "expected_date", "difficulty"]
)

# convert date object to datetime
df['expected_date'] = pd.to_datetime(df['expected_date'])

# define func to add weekdays from date
def date_by_adding_business_days(from_date, add_days,holidays):
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5: # sunday = 6
            continue
        if current_date in holidays:
            continue
        business_days_to_add -= 1
    return current_date

holidays = [
    datetime(2021, 5, 31),
    datetime(2021, 8, 30),
    datetime(2021, 12, 27),
    datetime(2021, 12, 28)
]


# set finish date information
std_addition = std_engineered / work_hours_per_day  # days
bespoke_addition = bespoke / work_hours_per_day  # days

# determine end date from start date, project type and expected time'
df['end_date'] = "2021-05-01"
df['end_date'] = pd.to_datetime(df['end_date'])

for i in range(0, len(df)):
    if df['difficulty'][i] == "Std Engineered":
        df['end_date'][i] = date_by_adding_business_days(df['expected_date'][i], std_addition, holidays)
    else:
        df['end_date'][i] = date_by_adding_business_days(df['expected_date'][i], bespoke_addition, holidays)

# determine end date from start date, project type and expected time'
df['time'] = ""

for i in range(0, len(df)):
    if df['difficulty'][i] == "Std Engineered":
        df['time'][i] = std_engineered
    else:
        df['time'][i] = bespoke


# create engineering resource
resource = ['GW', 'JC', 'KT/DAB', 'SB']

# run through every project and assign personnel
df['resource'] = ""
j = 0
for i in range(0, len(df)):
    if j >= len(resource):
        j = 0
        df['resource'][i] = resource[j]
    else:
        df['resource'][i] = resource[j]
    j += 1

# calculate data for plot
project_time = sum(df['time'])
team_work_hours = yearly_work_hours_remaining * cap_fact
discrep = project_time - team_work_hours
personnel_req = discrep / (indv_yearly_work_hours_remaining * cap_fact)

# plot all jobs on a gannt chart
fig = px.timeline(
    df,
    x_start="expected_date", x_end="end_date", y="project",
    color="resource",
    title=f'Department Capacity - Winning every job with >50% prediction<br>CAPACITY:<br>Total project hours required = {round(project_time, 1)} | Team project work capacity = {cap_fact} | Total workable hours of team = {round(team_work_hours, 1)} | Discrepancy = {round(discrep, 1)}| Additional personnel required (est.) = {round(personnel_req, 1)}',
    text=df['probability']
)
fig.update_yaxes(autorange="reversed")
fig.show()


# plot every job with >75% chance
df_75 = df[df['probability']==75]
# calculate data for plot
project_time = sum(df_75['time'])
team_work_hours = yearly_work_hours_remaining * cap_fact
discrep = project_time - team_work_hours
personnel_req = discrep / (indv_yearly_work_hours_remaining * cap_fact)

fig2 = px.timeline(
    df_75,
    x_start="expected_date", x_end="end_date", y="project",
    color="resource",
    title=f'Department Capacity - Winning every job with >75% prediction<br>CAPACITY:<br>Total project hours required = {round(project_time, 1)} | Team project work capacity = {cap_fact} | Total workable hours of team = {round(team_work_hours, 1)} | Discrepancy = {round(discrep, 1)}| Additional personnel required (est.) = {round(personnel_req, 1)}',
    text=df_75['probability']
)
fig2.update_yaxes(autorange="reversed")
fig2.show()


# plot random number of projects dropped from indv data
np.random.seed(10)
# remove a random number of projects
remove_n = np.random.randint(0, len(df))
# create new random df
drop_indices = np.random.choice(df.index, remove_n, replace=False)
df_rand = df.drop(drop_indices)

# calculate data for plot
project_time = sum(df_rand['time'])
team_work_hours = yearly_work_hours_remaining * cap_fact
discrep = project_time - team_work_hours
personnel_req = discrep / (indv_yearly_work_hours_remaining * cap_fact)

fig3 = px.timeline(
    df_rand, x_start="expected_date",
    x_end="end_date", y="project", color="resource",
    title=f'Department Capacity - Random ({remove_n}) projects dropped from overall {len(df)} projects<br>CAPACITY:<br>Total project hours required = {round(project_time, 1)} | Team project work capacity = {cap_fact} | Total workable hours of team = {round(team_work_hours, 1)} | Discrepancy = {round(discrep, 1)}| Additional personnel required (est.) = {round(personnel_req, 1)}',
    text=df_rand['probability']
)
fig3.update_yaxes(autorange="reversed")
fig3.show()
