import pandas as pd

# Define the data
data = {
    'Name': ['John Doe', 'Jane Smith', 'Alice Johnson', 'Bob Brown', 'Emily Davis',
             'Michael Lee', 'Sarah Wilson', 'David Brown', 'Laura Green'],
    'Crew ID': ['C1A2B3', 'C2D4E5', 'C3F6G7', 'C4H8I9', 'C5J0K1',
                'C7X8Y9', 'D1E2F3', 'E4F5G6', 'F7G8H9'],
    'IP Address': ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4', '192.168.1.5',
                   '192.168.1.6', '192.168.1.7', '192.168.1.8', '192.168.1.9']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('crew_data.csv', index=False)

print("CSV file 'crew_data.csv' has been created.")
