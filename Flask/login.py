# Import necessary libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Initialize Flask application
app = Flask(__name__)

# Set up SQLite database with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/leandro/finalproject/whitelist.db'
app.config['SECRET_KEY'] = 'tele4642'  # Add a secret key for flash messages
db = SQLAlchemy(app)

# Define database model for MAC addresses
class MacAddress(db.Model):
    __tablename__ = 'mac_addresses'
    mac = db.Column(db.String, primary_key=True)

# Run the application
if __name__ == "__main__":
    # Start the Flask application
    app.run(host='10.3.141.1', port=5000)
