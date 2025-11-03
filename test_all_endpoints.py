import requests
import json

BASE_URL = "http://localhost:5000"

def print_response(method, endpoint, response):
    print(f"\n{'='*50}")
    print(f"{method} {endpoint}")
    print(f"Status: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))

def test_auth():
    print("🔐 TESTING AUTH ENDPOINTS")
    
    # Test Registration
    reg_data = {
        "email": "testuser@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe", 
        "phone_number": "1234567890"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=reg_data)
    print_response("POST", "/api/auth/register", response)
    
    if response.status_code == 201:
        token = response.json()['access_token']
        user_data = response.json()['user']
        user_id = user_data['user_id']
        print(f"✅ Registered user: {user_data['email']}")
        print(f"🔑 Token received: {token[:20]}...")
    else:
        print("❌ Registration failed")
        token = None
        return None
    
    # Test Login
    login_data = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print_response("POST", "/api/auth/login", response)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print(f"✅ Login successful")
        print(f"🔑 New token: {token[:20]}...")
        return token
    else:
        print("❌ Login failed")
        return None

def test_movies(token):
    print("\n🎬 TESTING MOVIE ENDPOINTS")
    
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    
    # Get all movies
    response = requests.get(f"{BASE_URL}/api/movies/", headers=headers)
    print_response("GET", "/api/movies/", response)
    
    if response.status_code == 200:
        movies = response.json()['movies']
        print(f"✅ Found {len(movies)} movies")
        return movies[0]['movie_id'] if movies else None
    return None

def test_screenings(token, movie_id):
    print("\n📅 TESTING SCREENING ENDPOINTS")
    
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    
    # Get screenings for a movie
    response = requests.get(f"{BASE_URL}/api/movies/{movie_id}/screenings", headers=headers)
    print_response("GET", f"/api/movies/{movie_id}/screenings", response)
    
    if response.status_code == 200:
        screenings = response.json()['screenings']
        print(f"✅ Found {len(screenings)} screenings for movie {movie_id}")
        return screenings[0]['screening_id'] if screenings else None
    return None

def test_bookings(token, screening_id):
    print("\n🎫 TESTING BOOKING ENDPOINTS")
    
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    
    # Create a booking
    booking_data = {
        "screening_id": screening_id,
        "seats": [
            {"seat_number": "A1", "ticket_type": "adult"},
            {"seat_number": "A2", "ticket_type": "adult"}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/api/bookings/", 
                           json=booking_data, 
                           headers=headers)
    print_response("POST", "/api/bookings/", response)
    
    if response.status_code == 201:
        booking = response.json()['booking']
        booking_id = booking['booking_id']
        print(f"✅ Booking created: ID {booking_id}")
        return booking_id
    return None

def test_user_bookings(token):
    print("\n👤 TESTING USER BOOKINGS ENDPOINT")
    
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    
    # Get user bookings
    response = requests.get(f"{BASE_URL}/api/bookings/user", headers=headers)
    print_response("GET", "/api/bookings/user", response)
    
    if response.status_code == 200:
        bookings = response.json()['bookings']
        print(f"✅ User has {len(bookings)} bookings")
        return bookings[0]['booking_id'] if bookings else None
    return None

def test_booking_cancellation(token, booking_id):
    print("\n❌ TESTING BOOKING CANCELLATION")
    
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    
    # Cancel booking
    response = requests.put(f"{BASE_URL}/api/bookings/{booking_id}/cancel", headers=headers)
    print_response("PUT", f"/api/bookings/{booking_id}/cancel", response)
    
    if response.status_code == 200:
        print("✅ Booking cancelled successfully")
        return True
    else:
        print("❌ Booking cancellation failed")
        return False

def main():
    print("🚀 STARTING COMPREHENSIVE API TESTS")
    print("Make sure your server is running on http://localhost:5000")
    print("="*60)
    
    try:
        # Run all tests
        token = test_auth()
        
        if token:
            movie_id = test_movies(token)
            
            if movie_id:
                screening_id = test_screenings(token, movie_id)
                
                if screening_id:
                    booking_id = test_bookings(token, screening_id)
                    
                    if booking_id:
                        user_booking_id = test_user_bookings(token)
                        test_booking_cancellation(token, booking_id)
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS COMPLETED!")
        print("Check the results above for any failures.")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("Make sure your Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    main()