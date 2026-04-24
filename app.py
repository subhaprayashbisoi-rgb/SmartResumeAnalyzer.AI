from flask import Flask, render_template, request
from skills import skills_list

app = Flask(__name__)

def analyze_resume(text):
    found_skills = []
    missing_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    score = int((len(found_skills) / len(skills_list)) * 100)

    return found_skills, missing_skills, score


@app.route("/", methods=["GET", "POST"])
def index():
    skills = []
    missing = []
    score = 0

    if request.method == "POST":
        text = request.form["resume"]
        skills, missing, score = analyze_resume(text)

    return render_template("index.html", skills=skills, missing=missing, score=score)


if __name__ == "__main__":
    app.run(debug=True)