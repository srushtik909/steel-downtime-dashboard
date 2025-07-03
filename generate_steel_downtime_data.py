import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
fake = Faker()
random.seed(42)
np.random.seed(42)

# Parameters
num_rows = 1000
machines = [f'M{str(i).zfill(2)}' for i in range(1, 31)]
departments = ['Melting', 'Rolling', 'Casting', 'Finishing']
shifts = ['A', 'B', 'C']
downtime_reasons = [
    'Maintenance', 'Overheating', 'Power Failure', 'Operator Error',
    'Material Shortage', 'Sensor Fault', 'Mechanical Jam', 'Inspection',
    'Setup Change', 'Unknown'
]
operators = [fake.name() for _ in range(40)]

# Generate data
data = []
start_date = datetime(2023, 1, 1)
for _ in range(num_rows):
    timestamp = start_date + timedelta(minutes=random.randint(0, 525600))  # within a year
    machine = random.choice(machines)
    shift = random.choice(shifts)
    downtime_reason = random.choices(
        downtime_reasons,
        weights=[0.25, 0.15, 0.1, 0.1, 0.08, 0.07, 0.07, 0.06, 0.06, 0.06],
        k=1
    )[0]
    department = random.choices(
        departments,
        weights=[0.3, 0.4, 0.2, 0.1],
        k=1
    )[0]
    operator = random.choice(operators)
    downtime_minutes = int(np.clip(np.random.normal(45, 30), 5, 240))
    # Production loss: 0.5 to 2.5 tons per minute, or ₹10k-₹50k per minute
    if random.random() < 0.5:
        prod_loss = round(downtime_minutes * random.uniform(0.5, 2.5), 2)
        prod_loss_str = f"{prod_loss} tons"
    else:
        prod_loss = int(downtime_minutes * random.uniform(10000, 50000))
        prod_loss_str = f"₹{prod_loss}"
    data.append({
        'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'Machine_ID': machine,
        'Shift': shift,
        'Downtime_Minutes': downtime_minutes,
        'Downtime_Reason': downtime_reason,
        'Department': department,
        'Operator_Name': operator,
        'Production_Loss': prod_loss_str
    })

df = pd.DataFrame(data)
df.to_csv('steel_downtime_data.csv', index=False)
print('Dataset generated: steel_downtime_data.csv') 