from typing_extensions import Buffer

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import io
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas 


app = Flask(__name__)
CORS(app)

# 🔐 PUT YOUR OPENROUTER KEY HERE
OPENROUTER_API_KEY = "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"


# -------------------------------
# 🔥 AI ANALYSIS ROUTE
# -------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    symptoms = data.get("symptoms", "")
    age = data.get("age", "")
    spo2 = data.get("spo2", "")

    # 🧠 THIS IS WHERE YOU CUSTOMIZE AI BEHAVIOR
    prompt = f"""

You are a clinical AI assistant.

Patient Details:
Age: {age}
Symptoms: {symptoms}
SpO2: {spo2}

Instructions:
- Provide a detailed clinical summary (4-6 lines)
- Assess risk level (Low / Moderate / High)
- Provide an AI-based possible diagnosis (NOT final)
- Provide advice

⚠️ This is NOT a medical diagnosis. Must include disclaimer.

Format EXACTLY like this:

Clinical Summary:
<detailed explanation>

Risk Level:
<Low/Moderate/High>

AI Possible Diagnosis:
<possible condition>

Advice:
<next steps>

Doctor Note:
This is an AI-generated assessment and must be reviewed by a licensed medical professional.

"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a clinical triage assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            }
        )

        output = response.json()

        # 🔥 Extract response safely
        result = output["choices"][0]["message"]["content"]

    except Exception as e:
        print("ERROR:", e)
        result = f"AI failed: {str(e)}"

    return jsonify({"result": result})


# -------------------------------
# 📄 PDF GENERATION
# -------------------------------


from flask import request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io
from datetime import datetime

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.json

    name = data.get("name", "Unknown")
    age = data.get("age", "N/A")
    summary = data.get("summary", "")
    bp = data.get("bp", "N/A")
    spo2 = data.get("spo2", "N/A")

    # 🔹 Create overlay
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    can.setFont("Helvetica", 10)

    # -------------------------------
    # 🧍 PATIENT DETAILS
    # -------------------------------
    can.setFont("Times-Roman",13)
    can.drawString(113, 620, name)
    can.drawString(113, 591, str(age))
    can.drawString(113, 563, datetime.now().strftime('%d-%m-%Y'))

    # -------------------------------
    # ❤️ VITALS
    # -------------------------------
    can.drawString(113, 475, f" {bp}")
    can.drawString(113, 441, f" {spo2}")

    # -------------------------------
    # 🧠 FORMAT AI TEXT
    # -------------------------------
    def wrap_text(text, max_chars=80):
        words = text.split()
        lines = []
        line = ""
        for word in words:
            if len(line + word) < max_chars:
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)
        return lines

    # 🔹 Parse sections
    try:
        summary_text = summary.split("Risk Level:")[0].replace("Clinical Summary:", "").strip()
        risk = summary.split("Risk Level:")[1].split("AI Possible Diagnosis:")[0].strip()
        diagnosis = summary.split("AI Possible Diagnosis:")[1].split("Advice:")[0].strip()
        advice = summary.split("Advice:")[1].split("Doctor Note:")[0].strip()
    except:
        summary_text = summary
        risk = ""
        diagnosis = ""
        advice = ""

    y = 350

    # -------------------------------
    # 📝 WRITE TEXT WITH SPACING
    # -------------------------------
    can.setFont("Helvetica-Bold", 11)
    can.drawString(80, y, "Clinical Summary:")
    y -= 15

    can.setFont("Helvetica", 10)
    for line in wrap_text(summary_text):
        can.drawString(80, y, line)
        y -= 14

    y -= 10

    can.setFont("Helvetica-Bold", 11)
    can.drawString(80, y, f"Risk Level: {risk}")
    y -= 18

    can.drawString(80, y, "AI Diagnosis:")
    y -= 15

    can.setFont("Helvetica", 10)
    for line in wrap_text(diagnosis):
        can.drawString(80, y, line)
        y -= 14

    y -= 10

    can.setFont("Helvetica-Bold", 11)
    can.drawString(80, y, "Advice:")
    y -= 15

    can.setFont("Helvetica", 10)
    for line in wrap_text(advice):
        can.drawString(80, y, line)
        y -= 14

    y -= 15

    # 🔥 DISCLAIMER
    can.setFillColorRGB(1, 0, 0)
    can.setFont("Helvetica-Bold", 10)
    can.drawString(80, y, "⚠ AI-generated. Please consult a doctor.")

    can.save()
    packet.seek(0)

    # -------------------------------
    # 📄 MERGE WITH TEMPLATE
    # -------------------------------
    template = PdfReader("template.pdf")
    overlay = PdfReader(packet)

    writer = PdfWriter()

    page = template.pages[0]
    page.merge_page(overlay.pages[0])
    writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="report.pdf",
        mimetype="application/pdf"
    )




# -------------------------------
# 🚀 RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)