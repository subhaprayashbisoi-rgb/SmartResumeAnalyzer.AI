from flask import Flask, render_template, request
import PyPDF2
import docx
from PIL import Image
import pytesseract

app = Flask(__name__)

skills_list = ["python", "java", "html", "css", "sql", "machine learning", "flask"]

def extract_text(file):
    filename = file.filename.lower()

    try:
        if filename.endswith('.txt'):
            return file.read().decode('utf-8', errors='ignore')

        elif filename.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content

            if text.strip() == "":
                image = Image.open(file)
                text = pytesseract.image_to_string(image)

            return text

        elif filename.endswith('.docx'):
            doc = docx.Document(file)
            return "\n".join([p.text for p in doc.paragraphs])

        elif filename.endswith(('.jpg', '.png')):
            image = Image.open(file)
            return pytesseract.image_to_string(image)

    except Exception as e:
        print("Error:", e)

    return ""


def analyze_resume(text):
    found_skills = []
    missing_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    score = int((len(found_skills) / len(skills_list)) * 100)
    

    # 🔥 Suggestions (NEW)
    suggestions = []
    if score < 50:
        suggestions.append("Add more technical skills relevant to the job.")
    if "project" not in text.lower():
        suggestions.append("Include project experience.")
    if "experience" not in text.lower():
        suggestions.append("Mention work experience.")
    if "education" not in text.lower():
        suggestions.append("Add your education details.")

    return found_skills, missing_skills, score, suggestions

@app.route("/", methods=["GET", "POST"])
def index():
    skills = []
    missing = []
    score = 0

    if request.method == "POST":
        file = request.files.get("resume_file")

        if file:
            text = extract_text(file)

            print("Extracted text:", text[:200])

            skills, missing, score, suggestions = analyze_resume(text)

    return render_template("index.html", 
                       skills=skills, 
                       missing=missing, 
                       score=score,
                       suggestions=suggestions)


if __name__ == "__main__":
    app.run(debug=True)