# app.py
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import json
from fpdf import FPDF
import re

app = Flask(__name__)

# Configure Gemini API
my_api_key="API_key_Goes_here"
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
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_profile():
    if not rate_limiter.can_make_request():
        return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

    data = request.json
    
    # Structured prompt for Gemini
    prompt = f"""
    Act as a career counselor analyzing a student's profile. Based on the following information, suggest suitable career paths:
    
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
                "successStory": "A brief success story in this field"
            }}
        ]
    }}

    Important: 
    1. Provide exactly 10 professions
    2. Ensure all JSON fields are present for each profession
    3. Make sure the response is properly formatted JSON
    4. Be specific and detailed in each field
    """
    
    rate_limiter.add_request()
    
    try:
        response = model.generate_content(prompt)
        
        # Extract and parse the response
        career_data = extract_json_from_response(response.text)
        
        return jsonify(career_data)
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request. Please try again.',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)