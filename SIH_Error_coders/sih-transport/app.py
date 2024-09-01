from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the CSV files
table1 = pd.read_csv('sih_delhi.csv')
table2 = pd.read_csv('sih_dtc.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/allocate', methods=['POST'])
def allocate_route():
    print("Request form data:", request.form)  # Log the entire form data
    
    crew_id = request.form.get('Crew_Id')
    print(f"Received Crew_Id: {crew_id}")  # Log Crew_Id
    
    if crew_id is None:
        return jsonify({'error': 'Crew ID not provided'}), 400
    
    crew_id = crew_id.strip().upper()
    crew_row = table2[table2['Crew_Id'].str.strip().str.upper() == crew_id]
    if crew_row.empty:
        return jsonify({'error': 'Crew ID not found'}), 404
    
    familiar_routes = crew_row['Familiar_Route_Number'].values[0].split(',')
    
    # Choose a route from the familiar routes
    allocated_route = familiar_routes[0]  # You can apply a more complex scheduling algorithm here
    
    # Get details from table1
    route_details = table1[table1['Route_Number'] == allocated_route]
    
    if route_details.empty:
        return jsonify({'error': 'Route details not found'}), 404
    
    route_info = route_details.to_dict(orient='records')[0]
    
    response = {
        'driver_name': crew_row['Driver_Name'].values[0],
        'conductor_name': crew_row['Conductor_Name'].values[0],
        'allocated_route': allocated_route,
        'route_stops': route_info['Route_Stops'],
        'route_timings': route_info['Route_Timings'],
        'bus_number': route_info['Bus_Number']
    }
    
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
