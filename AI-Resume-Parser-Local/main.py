from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import docx
import re
import io
import uvicorn

app = FastAPI(title="Resume Parser Pro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TECH_SKILLS = [
    "Python", "Java", "C++", "SQL", "NoSQL", "AWS", "Azure", "GCP", "Docker", 
    "Kubernetes", "FastAPI", "Flask", "Django", "Machine Learning", "NLP", 
    "Data Engineering", "Pandas", "PySpark", "Snowflake", "LangChain", 
    "LLMs", "Generative AI", "React", "JavaScript", "TypeScript", "HTML", "CSS",
    "Airflow", "Jenkins", "Git", "Tableau", "PowerBI", "R", "C#", "Golang",
    "Kafka", "RabbitMQ", "Camunda", "MySQL", "PostgreSQL", "MongoDB", "DynamoDB",
    "CloudWatch", "Splunk", "Linux", "Unix", "JIRA", "VMware", "PyCharm", "SailPoint",
    "ETL", "ELT", "LSTMs", "ARIMA", "React JS", "React Native", "NumPy",
    "DataBricks", "Qlik", "Bitbucket", "RESTful API", "Microservices", "CI/CD"
]

SECTION_HEADERS = [
    "experience", "work experience", "professional experience", "employment history",
    "education", "academic background", "academic history", "education summary",
    "skills", "technical skills", "core competencies", "expertise",
    "projects", "personal projects", "academic projects", "research & projects",
    "summary", "professional summary", "profile", "about me", "objective",
    "certifications", "publications", "research & publications", "awards", "honors"
]

def fix_pdf_text_corruption(text):
    text = re.sub(r'([a-zA-Z])6([a-zA-Z])', r'\g<1>ti\g<2>', text)
    text = re.sub(r'([a-zA-Z])8([a-zA-Z])', r'\g<1>tf\g<2>', text)
    return text

# --- THE SUMMARY GLUER ---
# Fixes PDF line breaks in summaries and paragraphs
def glue_paragraphs(text):
    if not text: return text
    lines = text.split('\n')
    glued = []
    for line in lines:
        clean_line = line.strip()
        if not clean_line: continue
        
        is_bullet = bool(re.match(r'^[\u2022\u2023\u25E6\u2043\u2219\*\-]', clean_line))
        
        if not glued:
            glued.append(clean_line)
        else:
            prev = glued[-1]
            # If current line is NOT a bullet, AND (starts with lowercase OR previous doesn't end in punctuation)
            if not is_bullet and (clean_line[0].islower() or not prev.endswith(('.', '!', '?', ':'))):
                glued[-1] = prev + " " + clean_line
            else:
                glued.append(clean_line)
    return "\n".join(glued)

def extract_email(text):
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return emails[0] if emails else "Not Found"

def extract_phone(text):
    phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return phones[0] if phones else "Not Found"

def extract_skills(text):
    text_lower = text.lower()
    found_skills = []
    for skill in TECH_SKILLS:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
            found_skills.append(skill)
    return found_skills

def extract_sections(text):
    lines = text.split('\n')
    sections = {"Contact & Intro": []}
    current_section = "Contact & Intro"
    
    for i, line in enumerate(lines):
        cleaned_line = line.strip()
        if not cleaned_line: continue
            
        clean_for_header = re.sub(r'^[\u2022\u2023\u25E6\u2043\u2219\*\-]\s*', '', cleaned_line)
        line_lower = clean_for_header.lower().replace(":", "").strip()
        words = line_lower.split()
        is_header = False
        
        if len(words) <= 6:
            for header in SECTION_HEADERS:
                if line_lower == header or line_lower == header + "s":
                    is_header = True
                    current_section = header.title()
                    break
                    
        if not is_header and i > 4 and len(words) > 0 and len(words) <= 4:
            if current_section.lower() not in ["experience", "work experience", "professional experience", "employment history"]:
                if not re.search(r'\d', clean_for_header):
                    if clean_for_header.istitle() or clean_for_header.isupper():
                        if line_lower not in ["email", "phone", "mobile", "page", "location", "description"]:
                            is_header = True
                            current_section = clean_for_header.title().replace(":", "")
        
        if is_header:
            if current_section not in sections: sections[current_section] = []
        else:
            sections[current_section].append(cleaned_line)
            
    return {k: "\n".join(v).strip() for k, v in sections.items() if "\n".join(v).strip()}

# --- 3. BULLETPROOF ATS PARSER (DATE ANCHORED) ---
def parse_workday_experience(experience_text):
    lines = [line.strip() for line in experience_text.split('\n') if line.strip()]
    date_pattern = re.compile(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\.,]*\d{4}|\d{1,2}/\d{2,4}|\d{4})\s*[-–to]+\s*(Present|Current|Till Date|Date|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\.,]*\d{4}|\d{1,2}/\d{2,4}|\d{4})', re.IGNORECASE)
    
    date_indices = []
    for i, line in enumerate(lines):
        if date_pattern.search(line):
            date_indices.append(i)
            
    jobs_raw = []
    for i, d_idx in enumerate(date_indices):
        start_idx = d_idx
        for step in range(1, 4): # Look up to 3 lines above the date
            candidate_idx = d_idx - step
            if candidate_idx < 0: break
            if i > 0 and candidate_idx <= date_indices[i-1] + 1: break 
            
            line_above = lines[candidate_idx].strip()
            
            # THE BLEED STOPPER: If the line ends with a period, it's a previous bullet. STOP.
            if line_above.endswith('.'): break 
            if len(line_above.split()) > 10: break 
            
            start_idx = candidate_idx
            
        if i + 1 < len(date_indices):
            next_d_idx = date_indices[i+1]
            next_start_idx = next_d_idx
            for step in range(1, 4):
                candidate_idx = next_d_idx - step
                line_above = lines[candidate_idx].strip()
                if line_above.endswith('.'): break # Apply bleed stopper here too
                if len(line_above.split()) > 10: break
                next_start_idx = candidate_idx
            end_idx = next_start_idx
        else:
            end_idx = len(lines)
            
        jobs_raw.append(lines[start_idx:end_idx])
        
    # Added "assistant" to catch "Research assistant"
    job_titles_keywords = ["developer", "engineer", "analyst", "scientist", "manager", "architect", "lead", "consultant", "intern", "assistant"]
    action_verbs = ["develop", "design", "create", "build", "manage", "led", "work", "using", "implement", "automate", "participate", "collaborate", "simplified"]
    
    parsed_jobs = []
    for job_lines in jobs_raw:
        title = "Role Not Specified"
        company = "Company Not Specified"
        location = "Location Not Specified"
        date_str = ""
        
        header_lines = []
        bullet_lines = []
        found_bullets = False
        
        # --- STEP 1: Separate Headers from Bullets ---
        for line in job_lines:
            raw_line = line.strip()
            if not raw_line: continue
            
            date_match = date_pattern.search(raw_line)
            if date_match and not date_str:
                date_str = date_match.group(0)
                raw_line = raw_line.replace(date_str, "").strip(" |,-")
            
            if not raw_line: continue
            
            is_bullet_char = bool(re.match(r'^[\u2022\u2023\u25E6\u2043\u2219\*\-]', raw_line))
            is_action_verb = any(raw_line.lower().startswith(v) for v in action_verbs)
            is_long = len(raw_line.split()) > 12
            
            if is_bullet_char or is_action_verb or is_long or raw_line.lower().startswith("responsibilities"):
                found_bullets = True
            
            if found_bullets:
                if raw_line.lower().replace(":", "") != "responsibilities":
                    bullet_lines.append(raw_line)
            else:
                header_lines.append(raw_line)
                
        # --- STEP 2: Parse Header (Intercepting Tech Stacks & Commas) ---
        unassigned_headers = []
        tech_stack_lines = []
        
        for h_line in header_lines:
            tech_count = sum(1 for skill in TECH_SKILLS if skill.lower() in h_line.lower())
            if tech_count >= 2 and ',' in h_line and len(h_line.split()) < 15:
                tech_stack_lines.append(h_line)
                continue
                
            loc_match = re.search(r'([A-Za-z\s]+,\s*[A-Z]{2}\b|[A-Za-z\s]+,\s*India\b)', h_line, re.IGNORECASE)
            if loc_match and location == "Location Not Specified":
                location = loc_match.group(0).strip()
                h_line = h_line.replace(location, "").strip(" ,-|")
            
            if not h_line: continue
            
            # THE COMMA SPLITTER: Handles "Title, Company" mixed lines
            parts = [p.strip() for p in re.split(r'\|| – | - ', h_line) if p.strip()]
            
            for p in parts:
                if ',' in p:
                    comma_parts = [cp.strip() for cp in p.split(',')]
                    # If one of the comma-separated parts has a job keyword, slice it!
                    if any(any(k in cp.lower() for k in job_titles_keywords) for cp in comma_parts):
                        unassigned_headers.extend(comma_parts)
                        continue
                unassigned_headers.append(p)
            
        for part in unassigned_headers:
            # Quick check for standalone locations like "Denton"
            if part.lower() in ["denton", "remote", "onsite"] and location == "Location Not Specified":
                location = part
                continue
                
            if any(k in part.lower() for k in job_titles_keywords) and title == "Role Not Specified":
                title = part
            elif company == "Company Not Specified":
                company = part
            elif title == "Role Not Specified":
                title = part 
                
        # --- STEP 3: The Sentence Gluer (Fixing Bullets) ---
        responsibilities = []
        
        for ts in tech_stack_lines:
             responsibilities.append(f"Environment/Tech Stack: {ts}")
             
        for b_line in bullet_lines:
            is_bullet_char = bool(re.match(r'^[\u2022\u2023\u25E6\u2043\u2219\*\-]', b_line))
            clean_b = re.sub(r'^[\u2022\u2023\u25E6\u2043\u2219\*\-]\s*', '', b_line).strip()
            
            if not clean_b: continue
            
            if not responsibilities:
                responsibilities.append(clean_b)
            else:
                prev_b = responsibilities[-1]
                if not is_bullet_char and (clean_b[0].islower() or not prev_b.endswith(('.', '!', '?'))):
                    responsibilities[-1] = prev_b + " " + clean_b
                else:
                    responsibilities.append(clean_b)
                    
        parsed_jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "date": date_str if date_str else "Date Not Specified",
            "responsibilities": responsibilities
        })
        
    return parsed_jobs

@app.post("/parse-resume/")
async def parse_resume(file: UploadFile = File(...)):
    filename = file.filename.lower()
    contents = await file.read()
    full_text = ""
    
    try:
        if filename.endswith('.pdf'):
            with pdfplumber.open(io.BytesIO(contents)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text(layout=True)
                    if text: full_text += text + "\n"
        elif filename.endswith('.docx'):
            doc = docx.Document(io.BytesIO(contents))
            for para in doc.paragraphs:
                text = para.text.strip()
                if not text: continue
                if para.style.name.startswith('List') or 'Bullet' in para.style.name or text.startswith(('•', '-', '▪', 'v', '➢', 'o')):
                    if not re.match(r'^[\u2022\u2023\u25E6\u2043\u2219\*\-]', text):
                        full_text += "• " + text + "\n"
                    else:
                        full_text += text + "\n"
                else:
                    full_text += text + "\n"
        else:
            raise HTTPException(status_code=400, detail="Only .pdf and .docx files are supported.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

    full_text = fix_pdf_text_corruption(full_text)
    extracted_sections = extract_sections(full_text)
    
    ext_email = extract_email(full_text)
    ext_phone = extract_phone(full_text)
    ext_skills = extract_skills(full_text)
    
    exp_key = next((k for k in extracted_sections.keys() if "experience" in k.lower()), None)
    sum_key = next((k for k in extracted_sections.keys() if "summary" in k.lower() or "profile" in k.lower() or "about me" in k.lower()), None)
    skill_key = next((k for k in extracted_sections.keys() if "skill" in k.lower()), None)
    
    final_summary = None
    if sum_key:
        # APPLY GLUER TO SUMMARY
        final_summary = glue_paragraphs(extracted_sections[sum_key])
    else:
        intro_text = extracted_sections.get("Contact & Intro", "")
        clean_intro = intro_text.replace(ext_email, "").replace(ext_phone, "")
        fallback_lines = [l.strip() for l in clean_intro.split('\n') if len(l.split()) > 8]
        if fallback_lines:
            final_summary = glue_paragraphs("\n".join(fallback_lines))
    
    handled_keys = {exp_key, sum_key, skill_key, "Contact & Intro"}
    
    # APPLY GLUER TO OTHER SECTIONS (like Projects/Education)
    other_sections = {}
    for k, v in extracted_sections.items():
        if k not in handled_keys:
            other_sections[k] = glue_paragraphs(v)
    
    parsed_experience = parse_workday_experience(extracted_sections[exp_key]) if exp_key else []

    return {
        "status": "Success",
        "filename": file.filename,
        "data": {
            "email": ext_email,
            "phone": ext_phone,
            "skills": ext_skills,
            "summary": final_summary,
            "parsed_experience": parsed_experience,
            "other_sections": other_sections 
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)