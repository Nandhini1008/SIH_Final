from flask import Flask, request, render_template, redirect, url_for, session
import random
import requests
import math
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = '311f671a9ec498740d7d27fd3b361ad3b4bd6705bb8cc705'


# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC8d7a2298d14a128943955c7cd600d8e2'
TWILIO_AUTH_TOKEN = '6999a4438f05f0351ff247b2ae51ee29'
TWILIO_PHONE_NUMBER = '+14694164254'

# Function to generate a 6-digit OTP
def generate_otp():
    return random.randint(100000, 999999)

def send_otp_via_sms(phone_number, otp):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your OTP is {otp}',
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid

# Function to calculate distance between two lat/lng points using Haversine formula
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371 * 1000  # Radius of Earth in meters (6371 km)
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

# Function to check if a point is within the geofence
def is_within_geofence(device_lat, device_lon, fence_lat, fence_lon, radius=200):
    distance = haversine_distance(device_lat, device_lon, fence_lat, fence_lon)
    return distance <= radius

# Function to get the device's location using an IP address
def get_location_from_ip(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        if data['status'] == 'success':
            device_lat = data['lat']
            device_lon = data['lon']
            return device_lat, device_lon
        else:
            return None, None
    except Exception as e:
        return None, None

@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    phone_number = request.form['phone_number']
    otp = generate_otp()
    
    # Store OTP in session for verification (for demo purposes, this would be sent via SMS in a real app)
    session['otp'] = otp
    session['phone_number'] = phone_number
    
    # In a real application, you would send the OTP via SMS
    try:
        message_sid = send_otp_via_sms(phone_number, otp)
        print(f"Sent OTP {otp} to phone number {phone_number} (Message SID: {message_sid})")
    except Exception as e:
        return f"Failed to send OTP: {str(e)}"
    
    return redirect(url_for('verify_otp'))

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if 'otp' in session and str(session['otp']) == entered_otp:
            # OTP is correct, get the user's IP address
            user_ip = request.remote_addr
            print(user_ip)
            session['user_ip'] = user_ip  # Save the IP address in the session
            
            return redirect(url_for('geofence_check'))
        else:
            return "Invalid OTP, try again."
    return render_template('verify_otp.html')

@app.route('/geofence_check')
def geofence_check():
    user_ip = session.get('user_ip')
    
    if user_ip:
        device_lat, device_lon = get_location_from_ip(user_ip)
        
        if device_lat is not None and device_lon is not None:
            # Hardcoded geofence center (replace with actual GPS data)
            geofence_lat, geofence_lon = 13.009651, 80.005104
            
            if is_within_geofence(device_lat, device_lon, geofence_lat, geofence_lon):
                return f"The device with IP {user_ip} is within the geofence."
            else:
                return f"The device with IP {user_ip} is outside the geofence."
        else:
            return "Your Schedule is sent through SMS." 
    else:
        return "User IP address not found."

if __name__ == '__main__':
    app.run(debug=True)
