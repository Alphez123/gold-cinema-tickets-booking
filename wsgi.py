import sys
import os

# Add your project directory to the Python path
project_home = '/home/yourusername/cinema-booking-system/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import your Flask app
from run import app as application

# Optional: Configure any production settings
if __name__ == "__main__":
    application.run()