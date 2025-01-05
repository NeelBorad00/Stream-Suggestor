# Stream Suggestor 🎓

A intelligent career guidance system powered by Gemini AI that helps 10th-grade students make informed decisions about their academic streams and future career paths.

## 🌟 Features

- **Multi-step Analysis**: Intuitive interface to gather student information:
  - Personal goals and aspirations
  - Individual interests
  - Current skill set
  - Willingness to learn new skills

- **AI-Powered Recommendations**: 
  - Top 10 relevant professions based on student profile
  - Required skills analysis
  - Detailed career progression paths
  - Current market statistics
  - Success stories

- **Interactive Visualizations**:
  - Career growth timeline
  - Skills requirement comparison
  - Career path flowcharts

- **Export Functionality**:
  - Download recommendations as PDF
  - Detailed career roadmaps
  - Resource links for skill development

## 🛠️ Technology Stack

- **Frontend**:
  - HTML5
  - Tailwind CSS
  - JavaScript
  - Chart.js for visualizations

- **Backend**:
  - Flask (Python)
  - Google Gemini AI API
  - Rate limiting implementation

- **Additional Libraries**:
  - html2pdf.js for PDF generation
  - Custom theme implementation

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stream-suggestor.git
cd stream-suggestor
```

2. Install required Python packages:
```bash
pip install flask google-generativeai fpdf
```

3. Set up your Gemini API key:
   - Create a file named `.env` in the root directory
   - Add your API key: `GEMINI_API_KEY=your_api_key_here`

4. Run the application:
```bash
python app.py
```

5. Access the application at `http://localhost:5000`

## 🔒 Rate Limits

Free tier limitations:
- 15 Requests Per Minute (RPM)
- 1 million Tokens Per Minute (TPM)
- 1,500 Requests Per Day (RPD)

## 📱 Usage

1. **Enter Personal Information**:
   - Define your career goals
   - List your interests
   - Specify current skills

2. **Review Recommendations**:
   - Examine suggested career paths
   - Review required skills
   - Check market statistics
   - Read success stories

3. **Export Results**:
   - Download comprehensive PDF report
   - Save career roadmap
   - Access resource links

## 🙏 Acknowledgments

- Google Gemini AI for powering the career analysis
- Chart.js for beautiful visualizations
- Tailwind CSS for styling
- Flask community for the robust backend framework

## 🔄 Future Updates

- [ ] Mobile application development
- [ ] Integration with educational resources
- [ ] Personalized learning path recommendations
- [ ] Real-time job market analytics
- [ ] Community features and success stories
