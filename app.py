# app.py
from flask import Flask, render_template, request, jsonify, url_for
import google.generativeai as genai
import json
from fpdf import FPDF
import re
import sqlite3
from datetime import datetime
import os
import pandas as pd

app = Flask(__name__)

# Database setup
def init_db():
    # Ensure the database directory exists
    db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(db_dir, exist_ok=True)
    
    # Connect to database in the data directory
    db_path = os.path.join(db_dir, 'stream_suggestor.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS user_profiles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  goals TEXT NOT NULL,
                  interests TEXT NOT NULL,
                  current_skills TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Configure Gemini API
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
my_api_key = os.getenv('GEMINI_API_KEY')
if not my_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=my_api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Rate limiting variables
from datetime import datetime, timedelta
import threading

class RateLimiter:
    def __init__(self):
        self.locks = threading.Lock()
        self.requests = []
        self.daily_requests = 0
        self.last_reset = datetime.now()

    def can_make_request(self):
        now = datetime.now()
        
        # Reset daily counter if it's a new day
        if now.date() > self.last_reset.date():
            with self.locks:
                self.daily_requests = 0
                self.last_reset = now

        # Clean old requests
        minute_ago = now - timedelta(minutes=1)
        self.requests = [req for req in self.requests if req > minute_ago]

        # Check limits
        if (len(self.requests) >= 15 or  # 15 RPM
            self.daily_requests >= 1500): # 1,500 RPD
            return False

        return True

    def add_request(self):
        now = datetime.now()
        with self.locks:
            self.requests.append(now)
            self.daily_requests += 1

rate_limiter = RateLimiter()

def extract_json_from_response(text):
    """Extract JSON from the response text, handling potential formatting issues."""
    try:
        # First try direct JSON parsing
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            # Try to find JSON-like structure in the text
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                return json.loads(json_match.group())
            
            # If no JSON structure found, create a structured response
            return format_unstructured_response(text)
        except Exception:
            return format_unstructured_response(text)

def format_unstructured_response(text):
    """Format unstructured text into our expected JSON structure."""
    return {
        "professions": [
            {
                "name": "Career Option",
                "requiredSkills": ["Based on provided information"],
                "careerPath": ["Please try again with more specific information"],
                "salaryRange": "Varies",
                "marketStats": "Data unavailable",
                "successStory": "Please try again"
            }
        ]
    }

@app.route('/')
def home():
    return render_template('lp.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_profile():
    if not rate_limiter.can_make_request():
        return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

    data = request.json
    
    # Store user profile in database
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'stream_suggestor.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO user_profiles (name, goals, interests, current_skills)
                     VALUES (?, ?, ?, ?)''',
                  (data['name'], data['goals'], data['interests'], data['currentSkills']))
        profile_id = c.lastrowid
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving profile: {str(e)}")
        return jsonify({'error': 'Failed to save profile'}), 500
    
    # Structured prompt for Gemini
    prompt = f"""
    Act as a career counselor analyzing a student's profile. Based on the following information, suggest suitable career paths:
    
    Name: {data['name']}
    Goals: {data['goals']}
    Interests: {data['interests']}
    Current Skills: {data['currentSkills']}
    
    Provide a detailed analysis in the following JSON format exactly:
    {{
        "professions": [
            {{
                "name": "Profession Name",
                "requiredSkills": ["skill1", "skill2", "skill3"],
                "careerPath": ["10th Grade - Focus on relevant subjects", "12th Grade - Choose appropriate stream", "Bachelor's Degree details", "Master's/Additional qualifications", "Entry-level position", "Career progression"],
                "salaryRange": "Entry level to Senior level salary range in INR",
                "marketStats": "Current job market statistics and future outlook",
                "successStory": "A real-world example of someone who succeeded in this field, including their educational background, key achievements, and current position. For example: 'Sarah Johnson, who started with a passion for coding in high school, pursued Computer Science at IIT Bombay. After graduating, she joined Google as a Software Engineer and within 5 years became a Senior Tech Lead, leading a team of 20 engineers and contributing to major projects like Google Maps.'"
            }}
        ]
    }}

    Important: 
    1. Provide exactly 10 professions
    2. Ensure all JSON fields are present for each profession
    3. Make sure the response is properly formatted JSON
    4. Be specific and detailed in each field
    5. Personalize the recommendations based on the user's name
    6. For success stories, include real-world examples with specific names, educational background, career progression, and current achievements
    """
    
    rate_limiter.add_request()
    
    try:
        response = model.generate_content(prompt)
        
        # Extract and parse the response
        career_data = extract_json_from_response(response.text)
        
        # Add profile ID to the response
        career_data['profile_id'] = profile_id
        
        return jsonify(career_data)
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request. Please try again.',
            'details': str(e)
        }), 500

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/profiles')
def get_profiles():
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'stream_suggestor.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM user_profiles ORDER BY created_at DESC')
        profiles = c.fetchall()
        conn.close()
        
        return jsonify([{
            'id': profile[0],
            'name': profile[1],
            'goals': profile[2],
            'interests': profile[3],
            'current_skills': profile[4],
            'created_at': profile[5]
        } for profile in profiles])
    except Exception as e:
        print(f"Error fetching profiles: {str(e)}")
        return jsonify({'error': 'Failed to fetch profiles'}), 500

@app.route('/admin/feedback')
def get_feedback():
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'stream_suggestor.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM feedback ORDER BY created_at DESC')
        feedback = c.fetchall()
        conn.close()
        
        return jsonify([{
            'id': item[0],
            'profile_id': item[1],
            'rating': item[2],
            'comments': item[3],
            'created_at': item[4]
        } for item in feedback])
    except Exception as e:
        print(f"Error fetching feedback: {str(e)}")
        return jsonify({'error': 'Failed to fetch feedback'}), 500

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Career Recommendations Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

@app.route('/generate-report', methods=['POST'])
def generate_report():
    try:
        data = request.get_json()
        
        # Create PDF
        pdf = PDF()
        pdf.add_page()
        
        # Set auto page break
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Add header
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Career Recommendation Report', ln=True, align='C')
        pdf.ln(10)
        
        # Add user information
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Personal Information', ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Name: {data["name"]}', ln=True)
        pdf.cell(0, 10, f'Goals: {data["goals"]}', ln=True)
        pdf.cell(0, 10, f'Interests: {data["interests"]}', ln=True)
        pdf.cell(0, 10, f'Current Skills: {data["currentSkills"]}', ln=True)
        pdf.ln(10)
        
        # Add recommendations
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Career Recommendations', ln=True)
        pdf.ln(5)
        
        for profession in data['professions']:
            # Check if we need a new page
            if pdf.get_y() > 250:
                pdf.add_page()
            
            # Profession name
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, profession['name'], ln=True)
            pdf.ln(5)
            
            # Required Skills
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 10, 'Required Skills:', ln=True)
            pdf.set_font('Arial', '', 10)
            for skill in profession['requiredSkills']:
                pdf.cell(0, 10, f'• {skill}', ln=True)
            pdf.ln(5)
            
            # Career Path
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 10, 'Career Path:', ln=True)
            pdf.set_font('Arial', '', 10)
            for step in profession['careerPath']:
                pdf.cell(0, 10, f'• {step}', ln=True)
            pdf.ln(5)
            
            # Salary Range
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 10, 'Salary Range:', ln=True)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 10, profession['salaryRange'], ln=True)
            pdf.ln(5)
            
            # Market Statistics
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 10, 'Market Statistics:', ln=True)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 10, profession['marketStats'], ln=True)
            pdf.ln(5)
            
            # Success Story
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 10, 'Success Story:', ln=True)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 10, profession['successStory'])
            pdf.ln(10)
        
        # Ensure reports directory exists
        reports_dir = os.path.join('static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Save the PDF
        filename = f"career-report-{data['name'].lower().replace(' ', '-')}.pdf"
        filepath = os.path.join(reports_dir, filename)
        
        # Save the PDF with proper encoding
        pdf.output(filepath, 'F')
        
        # Return the URL for the generated PDF
        pdf_url = url_for('static', filename=f'reports/{filename}', _external=True)
        
        return jsonify({
            'success': True,
            'url': pdf_url,
            'filename': filename
        })
        
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
