import io
import spacy
import pdfplumber
from docx import Document
from jobs.models import Skill

# Load the spaCy model once
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # This can happen if the model is not downloaded
    print("Downloading spaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    """Extracts text from a PDF file."""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    """Extracts text from a DOCX file."""
    doc = Document(io.BytesIO(file.read()))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_skills(text):
    """Extracts skills from text using a predefined skill list."""
    # Get all skills from the database
    all_skills = list(Skill.objects.values_list('name', flat=True))
    
    # Use spaCy's PhraseMatcher for efficient skill finding
    matcher = spacy.matcher.PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in all_skills]
    matcher.add("SKILL", patterns)

    doc = nlp(text)
    matches = matcher(doc)
    
    found_skills = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        found_skills.add(span.text.lower())
        
    return list(found_skills)

def extract_details(text):
    """Extracts name, email, and phone number from text."""
    doc = nlp(text)
    details = {
        'name': None,
        'email': None,
        'mobile_number': None,
    }

    # Extract Email
    for token in doc:
        if token.like_email:
            details['email'] = token.text
            break
    
    # Extract Name (heuristic: look for proper nouns labeled as PERSON near the beginning)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not details['name']:
            details['name'] = ent.text
            break

    # A simple regex could be used for phone numbers, but this is a placeholder
    # For a more robust solution, consider using regex patterns for phone numbers.

    return details

def calculate_match_score(resume_skills, job_skills):
    """Calculates the percentage of job skills found in the resume."""
    if not job_skills:
        return 0.0
    common_skills = set(s.lower() for s in resume_skills).intersection(set(j.lower() for j in job_skills))
    score = (len(common_skills) / len(job_skills)) * 100
    return score
