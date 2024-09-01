import math
import requests

# Function to calculate distance between two lat/lng points using Haversine formula
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371 * 1000  # Radius of Earth in meters (6371 km)
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in meters
    distance = R * c
    return distance

# Function to check if a point is within the geofence
def is_within_geofence(device_lat, device_lon, fence_lat, fence_lon, radius=200):
    distance = haversine_distance(device_lat, device_lon, fence_lat, fence_lon)
    return distance <= radius

# Function to get the geofence center (latitude and longitude) from the GPS device
def get_gps_location():
    # In a real-world scenario, this would involve reading data from a GPS module
    # For demonstration, we'll use hardcoded GPS coordinates (e.g., bus depot)
    gps_lat = 37.7749  # Example latitude for geofence center (e.g., San Francisco)
    gps_lon = -122.4194  # Example longitude for geofence center
    return gps_lat, gps_lon

# Function to get the device's location using an IP address
def get_location_from_ip(ip_address):
    try:
        # Using the ip-api.com service to get the device's location from IP
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        if data['status'] == 'success':
            device_lat = data['lat']
            device_lon = data['lon']
            return device_lat, device_lon
        else:
            print("Could not get location for IP address.")
            return None, None
    except Exception as e:
        print(f"Error fetching IP location: {e}")
        return None, None

# Example usage

# Get the geofence center from the GPS (you can replace this with real GPS readings)
geofence_lat, geofence_lon = get_gps_location()

# Get the device location using the IP address
ip_address = input("Enter the device IP address: ")  # Get the IP address from the user
device_lat, device_lon = get_location_from_ip(ip_address)

# Check if the location from IP is valid
if device_lat is not None and device_lon is not None:
    # Check if the device is within the 200m radius geofence
    if is_within_geofence(device_lat, device_lon, geofence_lat, geofence_lon):
        print(f"The device with IP {ip_address} is within the geofence.")
    else:
        print(f"The device with IP {ip_address} is outside the geofence.")
else:
    print("Could not determine the device's location.")
