AI Clinical Triage and Emergency Assistant

An intelligent healthcare web application designed to assist in early-stage clinical triage, generate structured medical reports, and enable rapid emergency response using real-time user input and location services.

This system is built as a decision-support tool to aid preliminary assessment and improve accessibility to healthcare insights, while ensuring that all outputs are reviewed by qualified medical professionals.

Overview

The application collects basic patient information such as symptoms, age, and vital parameters (e.g., blood pressure and SpO2 levels), and uses an AI model to generate a structured clinical response.

The output includes:

A detailed clinical summary
Risk classification (Low, Moderate, High)
AI-assisted possible diagnosis (non-final)
Suggested next steps

Additionally, the system provides:

A downloadable clinical report in PDF format
Emergency SOS functionality
Location-based hospital discovery
Key Features
1. AI-Based Clinical Analysis
Processes patient symptoms and vitals in real time
Generates structured and readable medical insights
Designed with controlled prompting to avoid direct diagnosis
Produces consistent, formatted outputs for clarity
2. Structured Clinical Report Generation
Automatically generates a professional PDF report
Includes:
Patient details
Vital signs (BP, SpO2)
AI-generated clinical summary
Risk level and recommendations
Uses a hospital-style template with proper formatting and spacing
3. Risk Assessment System
Categorizes patient condition into:
Low Risk
Moderate Risk
High Risk
Can be extended with visual indicators for quick interpretation
4. Emergency SOS Integration
One-click emergency call functionality
Designed to support immediate action in critical scenarios
5. Location-Based Hospital Discovery
Uses browser geolocation to detect user position
Redirects to nearby hospitals via map services
Ensures reliability without dependency on unstable external APIs
6. Safety and Ethical Design
Explicitly avoids making definitive medical diagnoses
Includes a mandatory disclaimer in both UI and PDF reports
Reinforces that outputs must be reviewed by licensed professionals
Technology Stack

Frontend

HTML
CSS
JavaScript

Backend

Python (Flask)

AI Integration

OpenRouter API (Large Language Models)

PDF Generation

ReportLab
PyPDF2

Other Integrations

Browser Geolocation API
Native device call functionality (tel protocol)
How It Works
The user inputs:
Symptoms
Age
Blood Pressure
SpO2 level
The backend processes the data and sends it to the AI model
The AI returns a structured clinical response
The user can:
View results in the interface
Download a formatted PDF report
Trigger emergency SOS
Locate nearby hospitals

Setup Instructions
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

pip install -r requirements.txt

for security reasons the api key is disabledd in the code, change the line by generating an AP Key from open router 

run the application

Disclaimer

This system provides AI-assisted preliminary analysis only.
It is not a substitute for professional medical advice, diagnosis, or treatment.

All outputs must be reviewed by a qualified healthcare professional before any medical decision is made.

Future Improvements
Visual risk indicators (color-coded triage system)
Patient history and report storage
Voice-based symptom input
Integration with verified healthcare APIs
Enhanced UI for clinical environments
Author

Tanmay Anand, Madhav Gupta, Anushka Gupta, Palchin 
Student and developer focused on building practical AI-driven solutions,CyberSecurity Projects
