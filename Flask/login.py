# Import necessary libraries
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os
import re
import requests
from datetime import datetime

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

# Function to get ARP table and parse it
def get_arp_table():
    arp_table = os.popen('arp -n').read()  # Get ARP table as string
    ip_to_mac = {}

    # Parse ARP table, line by line
    for line in arp_table.split('\n')[1:]:
        parts = re.split(r'\s+', line)
        if len(parts) >= 3:
            ip = parts[0]
            mac = parts[2]
            ip_to_mac[ip] = mac

    return ip_to_mac

# Run the application
if __name__ == "__main__":
    # Start the Flask application
    app.run(host='10.3.141.1', port=5000)
