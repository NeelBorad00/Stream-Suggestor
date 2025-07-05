# Stream Suggestor

A modern career counseling web application that helps students choose their career paths based on their personal profile using AI-powered recommendations.

## 🚀 Features

- **Interactive Form Flow**: 4-step questionnaire collecting name, goals, interests, and skills
- **AI-Powered Analysis**: Uses Google Gemini AI to generate personalized career recommendations
- **Rich Career Data**: Each recommendation includes required skills, career path, salary range, market statistics, and success stories
- **Beautiful UI/UX**: Modern, responsive design with card-based navigation and swipe gestures
- **Timeline Career Paths**: Visual timeline format for career progression steps
- **PDF Report Generation**: Download detailed career reports
- **Mobile Responsive**: Optimized for all devices with touch-friendly interface
- **Rate Limiting**: API protection for stable performance

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **AI**: Google Gemini API
- **Database**: SQLite
- **PDF**: FPDF library
- **Frontend**: HTML/CSS/JavaScript
- **Deployment**: Gunicorn (for production)

## 📱 Screenshots

### Desktop View
- Modern card-based interface
- Smooth animations and transitions
- Timeline format for career paths

### Mobile View
- Touch-friendly interface
- Swipe gestures for navigation
- Responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/NeelBorad00/stream-suggestor.git
   cd stream-suggestor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create a .env file and add your API key
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Database
The application uses SQLite for data storage. The database file is automatically created in the `data/` directory.

## 📁 Project Structure

```
stream-suggestor/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore           # Git ignore rules
├── data/                # Database directory
│   └── stream_suggestor.db
├── static/              # Static assets
│   ├── a.png           # Background image
│   └── reports/        # Generated PDF reports
└── templates/          # HTML templates
    ├── index.html      # Main application page
    └── lp.html         # Landing page
```

## 🎯 How It Works

1. **User Input**: Users fill out a 4-step questionnaire
2. **AI Analysis**: Google Gemini AI analyzes the profile and generates recommendations
3. **Career Matching**: System provides 10 personalized career options
4. **Detailed Information**: Each career includes skills, path, salary, and success stories
5. **Timeline View**: Career paths are displayed in an attractive timeline format
6. **PDF Export**: Users can download detailed career reports

## 🔒 Security Features

- Rate limiting (15 RPM, 1500 RPD)
- Input validation
- Secure API key handling
- SQL injection protection

## 📊 API Endpoints

- `GET /`: Landing page
- `GET /index`: Main application
- `POST /analyze`: Analyze user profile and generate recommendations
- `POST /generate-report`: Generate PDF career report
- `GET /admin`: Admin panel (for viewing user profiles)

## 🚀 Deployment

### Render.com Deployment

1. **Connect your GitHub repository** to Render.com
2. **Create a new Web Service**
3. **Configure the service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**: Add your `GEMINI_API_KEY`
4. **Deploy** and enjoy your live application!

### Environment Variables for Production
- `GEMINI_API_KEY`: Your Google Gemini API key
- `FLASK_ENV`: Set to `production`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Neel Borad**
- GitHub: [@NeelBorad00](https://github.com/NeelBorad00)

## 🙏 Acknowledgments

- Google Gemini AI for providing the AI capabilities
- Flask community for the excellent web framework
- All contributors and users of this project

## 📞 Support

If you have any questions or need support, please open an issue on GitHub or contact the author.

---

**Made with ❤️ for helping students find their perfect career path!** 