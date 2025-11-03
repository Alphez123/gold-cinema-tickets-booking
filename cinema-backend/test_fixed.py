import requests
import json
import random
import string

BASE_URL = "http://localhost:5000"

def generate_random_email():
    """Generate random email for testing"""
    random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"test_{random_string}@example.com"

def print_response(method, endpoint, response):
    print(f"\n{'='*50}")
    print(f"{method} {endpoint}")
    print(f"Status: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))

def test_complete_flow():
    print("🚀 COMPREHENSIVE API TEST WITH UNIQUE USER")
    print("=" * 60)
    
    # Generate unique email for this test
    test_email = generate_random_email()
    print(f"Testing with email: {test_email}")
    
    # Test Registration
    print("\n1. 🔐 TESTING REGISTRATION")
    reg_data = {
        "email": test_email,
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "1234567890"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=reg_data)
    print_response("POST", "/api/auth/register", response)
    
    if response.status_code != 201:
        print("❌ Registration failed, trying login with existing user...")
        # Try with a different email
        test_email = generate_random_email()
        reg_data["email"] = test_email
        response = requests.post(f"{BASE_URL}/api/auth/register", json=reg_data)
        print_response("POST", "/api/auth/register (retry)", response)
    
    if response.status_code == 201:
        token = response.json()['access_token']
        user_data = response.json()['user']
        print(f"✅ Registered user: {user_data['email']}")
    else:
        print("❌ Registration completely failed")
        return
    
    # Test Login
    print("\n2. 🔐 TESTING LOGIN")
    login_data = {
        "email": test_email,
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print_response("POST", "/api/auth/login", response)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print("✅ Login successful")
    else:
        print("❌ Login failed")
        return
    
    # Test Get Movies
    print("\n3. 🎬 TESTING MOVIES ENDPOINT")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{BASE_URL}/api/movies/", headers=headers)
    print_response("GET", "/api/movies/", response)
    
    if response.status_code == 200:
        movies = response.json()['movies']
        if movies:
            movie_id = movies[0]['movie_id']
            print(f"✅ Found {len(movies)} movies. Using movie ID: {movie_id}")
        else:
            print("❌ No movies found")
            return
    else:
        print("❌ Failed to get movies")
        return
    
    # Test Get Screenings
    print("\n4. 📅 TESTING SCREENINGS ENDPOINT")
    response = requests.get(f"{BASE_URL}/api/movies/{movie_id}/screenings", headers=headers)
    print_response("GET", f"/api/movies/{movie_id}/screenings", response)
    
    if response.status_code == 200:
        screenings = response.json()['screenings']
        if screenings:
            screening_id = screenings[0]['screening_id']
            print(f"✅ Found {len(screenings)} screenings. Using screening ID: {screening_id}")
        else:
            print("❌ No screenings found")
            return
    else:
        print("❌ Failed to get screenings")
        return
    
    # Test Create Booking
    print("\n5. 🎫 TESTING BOOKING CREATION")
    booking_data = {
        "screening_id": screening_id,
        "seats": [
            {"seat_number": "B1", "ticket_type": "adult"},
            {"seat_number": "B2", "ticket_type": "adult"}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/api/bookings/", json=booking_data, headers=headers)
    print_response("POST", "/api/bookings/", response)
    
    if response.status_code == 201:
        booking = response.json()['booking']
        booking_id = booking['booking_id']
        print(f"✅ Booking created successfully! Booking ID: {booking_id}")
    else:
        print("❌ Booking creation failed")
        return
    
    # Test Get User Bookings
    print("\n6. 👤 TESTING USER BOOKINGS")
    response = requests.get(f"{BASE_URL}/api/bookings/user", headers=headers)
    print_response("GET", "/api/bookings/user", response)
    
    if response.status_code == 200:
        bookings = response.json()['bookings']
        print(f"✅ User has {len(bookings)} bookings")
    else:
        print("❌ Failed to get user bookings")
        return
    
    # Test Get Specific Booking
    print("\n7. 📋 TESTING SPECIFIC BOOKING")
    response = requests.get(f"{BASE_URL}/api/bookings/{booking_id}", headers=headers)
    print_response("GET", f"/api/bookings/{booking_id}", response)
    
    if response.status_code == 200:
        print("✅ Successfully retrieved specific booking")
    else:
        print("❌ Failed to get specific booking")
        return
    
    # Test Booking Cancellation
    print("\n8. ❌ TESTING BOOKING CANCELLATION")
    response = requests.put(f"{BASE_URL}/api/bookings/{booking_id}/cancel", headers=headers)
    print_response("PUT", f"/api/bookings/{booking_id}/cancel", response)
    
    if response.status_code == 200:
        print("✅ Booking cancelled successfully")
    else:
        print("❌ Booking cancellation failed")
        return
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED! YOUR BACKEND IS WORKING PERFECTLY! 🎉")
    print("=" * 60)

def test_without_auth():
    print("\n\n🔓 TESTING ENDPOINTS WITHOUT AUTHENTICATION")
    print("=" * 50)
    
    # Test public endpoints
    response = requests.get(f"{BASE_URL}/api/movies/")
    print(f"GET /api/movies/ - Status: {response.status_code}")
    
    if response.status_code == 200:
        movies = response.json()['movies']
        print(f"✅ Public movies endpoint works - {len(movies)} movies")
    else:
        print("❌ Public movies endpoint failed")

if __name__ == "__main__":
    try:
        test_complete_flow()
        test_without_auth()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("Make sure your Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")