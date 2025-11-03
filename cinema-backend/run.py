from app import create_app
from app.models import User, Movie, Screening, Booking, Ticket
from app import db
from datetime import datetime, timedelta
import os

app = create_app()

def add_sample_data():
    """Add sample data for testing"""
    with app.app_context():
        # Check if data already exists
        if Movie.query.first() is None:
            print("Adding sample data...")
            
            # Add sample movies
            movies_data = [
                {
                    "title": "Avengers: Endgame",
                    "description": "The epic conclusion to the Infinity Saga.",
                    "genre": "Action, Adventure, Sci-Fi",
                    "duration": 181,
                    "rating": "PG-13",
                    "poster_url": "/static/images/avengers.jpg",
                    "trailer_url": "https://youtube.com/embed/TcMBFSGVi1c",
                    "release_date": datetime(2019, 4, 26).date(),
                    "is_active": True
                },
                {
                    "title": "The Lion King",
                    "description": "Simba's journey to reclaim his kingdom.",
                    "genre": "Animation, Adventure, Drama",
                    "duration": 118,
                    "rating": "G",
                    "poster_url": "/static/images/lionking.jpg",
                    "trailer_url": "https://youtube.com/embed/7TavVZMewpY",
                    "release_date": datetime(2019, 7, 19).date(),
                    "is_active": True
                },
                {
                    "title": "Black Panther",
                    "description": "T'Challa returns home to Wakanda.",
                    "genre": "Action, Adventure, Sci-Fi",
                    "duration": 134,
                    "rating": "PG-13",
                    "poster_url": "/static/images/blackpanther.jpg",
                    "trailer_url": "https://youtube.com/embed/xjDjIWPwcPU",
                    "release_date": datetime(2018, 2, 16).date(),
                    "is_active": True
                }
            ]
            
            for movie_data in movies_data:
                movie = Movie(**movie_data)
                db.session.add(movie)
            
            db.session.commit()
            
            # Get the movie IDs after commit
            movies = Movie.query.all()
            
            # Add sample screenings for next 7 days
            for movie in movies:
                for day in range(1, 8):
                    show_date = datetime.now().date() + timedelta(days=day)
                    
                    screening1 = Screening(
                        movie_id=movie.movie_id,
                        screen_number=1,
                        show_date=show_date,
                        show_time="14:30",
                        total_seats=100,
                        available_seats=100,
                        price=12.50
                    )
                    
                    screening2 = Screening(
                        movie_id=movie.movie_id,
                        screen_number=1,
                        show_date=show_date,
                        show_time="18:00",
                        total_seats=100,
                        available_seats=100,
                        price=15.00
                    )
                    
                    db.session.add(screening1)
                    db.session.add(screening2)
            
            db.session.commit()
            print("✅ Sample data added successfully!")
        else:
            print("📊 Data already exists")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_sample_data()
    
    # Get port from environment variable (for production)
    port = int(os.environ.get("PORT", 5000))
    
    print("\n" + "="*50)
    print("🎬 CINEMA BOOKING SERVER STARTED!")
    print("="*50)
    print("📍 Running in production mode")
    print("📚 API endpoints ready")
    print("🛑 Press CTRL+C to stop the server")
    print("="*50)
    
    # Run the app (debug=False in production)
    app.run(host='0.0.0.0', port=port, debug=False)