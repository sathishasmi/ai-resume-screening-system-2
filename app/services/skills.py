import re

SKILLS_DB = {
    "data_science": [
        "python", "pandas", "numpy", "matplotlib",
        "seaborn", "machine learning", "sql",
        "scikit-learn", "tensorflow", "keras"
    ],

    "machine_learning": [
        "machine learning", "scikit-learn",
        "tensorflow", "keras", "deep learning",
        "nlp", "opencv"
    ],

    "Frontend_Developer": [
        "html", "css", "javascript", "react",
        "angular", "vue", "bootstrap",
        "tailwind", "typescript"
    ],

    "Backend_Developer": [
        "python", "django", "flask", "fastapi",
        "node.js", "express", "mysql",
        "postgresql", "mongodb", "rest api"
    ],

    "Cloud_Engineer": [
        "aws", "azure", "gcp", "docker",
        "kubernetes", "terraform", "jenkins",
        "linux", "devops", "ci/cd"
    ]
}


def extract_skills(text):
    text = text.lower()

    found_skills = set()

    # flatten all skills
    all_skills = []
    for skills in SKILLS_DB.values():
        all_skills.extend(skills)

    # remove duplicates
    all_skills = list(set(all_skills))

    for skill in all_skills:
        pattern = re.escape(skill.lower())
        if re.search(pattern, text):
            found_skills.add(skill.lower())

    return list(found_skills)