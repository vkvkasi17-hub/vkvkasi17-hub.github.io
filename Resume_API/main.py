from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import pdfplumber
import docx
import re
import io

app = FastAPI(title="Resume Parser Pro")

# --- 1. EXPANDED NLP SKILL DATABASE ---
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

# --- 2. DYNAMIC DATA EXTRACTION LOGIC ---
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
        
        # Known headers
        if len(words) <= 6:
            for header in SECTION_HEADERS:
                if line_lower == header or line_lower == header + "s":
                    is_header = True
                    current_section = header.title()
                    break
                    
        # Dynamic headers
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
    
    # Step 1: Find all lines containing dates
    date_indices = []
    for i, line in enumerate(lines):
        if date_pattern.search(line):
            date_indices.append(i)
            
    # Step 2: Chunk the text into precise Job Blocks based on dates
    jobs_raw = []
    for i, d_idx in enumerate(date_indices):
        start_idx = d_idx
        # Look above the date to capture Company Name
        for step in range(1, 3):
            candidate_idx = d_idx - step
            if candidate_idx < 0: break
            if i > 0 and candidate_idx <= date_indices[i-1] + 1: break # Don't bleed into previous job
            if len(lines[candidate_idx].split()) > 10: break # Don't capture previous job's bullets
            start_idx = candidate_idx
            
        if i + 1 < len(date_indices):
            next_d_idx = date_indices[i+1]
            next_start_idx = next_d_idx
            for step in range(1, 3):
                candidate_idx = next_d_idx - step
                if len(lines[candidate_idx].split()) > 10: break
                next_start_idx = candidate_idx
            end_idx = next_start_idx
        else:
            end_idx = len(lines)
            
        jobs_raw.append(lines[start_idx:end_idx])
        
    job_titles_keywords = ["developer", "engineer", "analyst", "scientist", "manager", "architect", "lead", "consultant", "coordinator", "specialist"]
    
    # Step 3: Parse the extracted chunks perfectly
    parsed_jobs = []
    for job_lines in jobs_raw:
        title = "Role Not Specified"
        company = "Company Not Specified"
        location = "Location Not Specified"
        date_str = ""
        responsibilities = []
        found_first_responsibility = False
        
        for line in job_lines:
            is_bullet_char = bool(re.match(r'^[\u2022\u2023\u25E6\u2043\u2219\*\-]', line.strip()))
            line_clean = re.sub(r'^[\u2022\u2023\u25E6\u2043\u2219\*\-]\s*', '', line).strip()
            lower_line = line_clean.lower()
            
            # Skip filler words
            if lower_line.replace(":", "") in ["responsibilities", "roles and responsibilities", "description", "technical environment", "environment"]:
                found_first_responsibility = True
                continue
                
            date_match = date_pattern.search(line_clean)
            if date_match and not date_str:
                date_str = date_match.group(0)
                line_clean = line_clean.replace(date_str, "").strip(" |,-")
                if not line_clean: continue
                
            is_long = len(line_clean.split()) > 8
            is_explicit_desc = lower_line.startswith("description:") or lower_line.startswith("environment:")
            
            # Identify if line is a bullet/responsibility
            if found_first_responsibility or is_long or is_explicit_desc or is_bullet_char:
                found_first_responsibility = True
                res = re.sub(r'^(Description|Project|Environment|Technical Environment):\s*', '', line_clean, flags=re.IGNORECASE).strip()
                
                # THE SENTENCE GLUER: Fixes randomly broken lines in DOCX
                if responsibilities and not is_bullet_char and not is_explicit_desc:
                    if not responsibilities[-1].strip().endswith(('.', '!', '?')) or (res and res[0].islower()):
                        responsibilities[-1] += " " + res
                        continue
                        
                if res: responsibilities.append(res)
                continue
                
            # If not a responsibility, it's Title/Company/Location
            parts = [p.strip() for p in re.split(r'\|| – | - ', line_clean) if p.strip()]
            for part in parts:
                part_lower = part.lower()
                part = re.sub(r'^(Client|Company|Project):\s*', '', part, flags=re.IGNORECASE).strip()
                if not part: continue
                
                loc_match = re.search(r'([A-Za-z\s]+,\s*[A-Z]{2}\b|[A-Za-z\s]+,\s*India\b)', part, re.IGNORECASE)
                if loc_match:
                    loc_str = loc_match.group(0).strip()
                    if location == "Location Not Specified": location = loc_str
                    comp = part.replace(loc_str, "").strip(" ,-")
                    if comp:
                        if company == "Company Not Specified": company = comp
                        elif comp not in company: company += ", " + comp
                elif any(k in part_lower for k in job_titles_keywords) and title == "Role Not Specified":
                    title = part.replace("Title:", "").strip()
                else:
                    if company == "Company Not Specified": company = part
                    elif part not in company: company += ", " + part
                    
        parsed_jobs.append({
            "title": title,
            "company": company.strip(" ,"),
            "location": location,
            "date": date_str if date_str else "Date Not Specified",
            "responsibilities": responsibilities
        })
        
    return parsed_jobs

# --- 4. THE API ENDPOINT ---
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

    extracted_sections = extract_sections(full_text)
    
    ext_email = extract_email(full_text)
    ext_phone = extract_phone(full_text)
    ext_skills = extract_skills(full_text)
    
    exp_key = next((k for k in extracted_sections.keys() if "experience" in k.lower()), None)
    sum_key = next((k for k in extracted_sections.keys() if "summary" in k.lower() or "profile" in k.lower() or "about me" in k.lower()), None)
    skill_key = next((k for k in extracted_sections.keys() if "skill" in k.lower()), None)
    
    final_summary = None
    if sum_key:
        final_summary = extracted_sections[sum_key]
    else:
        intro_text = extracted_sections.get("Contact & Intro", "")
        clean_intro = intro_text.replace(ext_email, "").replace(ext_phone, "")
        fallback_lines = [l.strip() for l in clean_intro.split('\n') if len(l.split()) > 8]
        if fallback_lines:
            final_summary = "\n".join(fallback_lines)
    
    handled_keys = {exp_key, sum_key, skill_key, "Contact & Intro"}
    other_sections = {k: v for k, v in extracted_sections.items() if k not in handled_keys}
    
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

# --- 5. THE ANIMATED COLORFUL FRONTEND ---
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vibrant AI Resume Parser</title>
        <style>
            :root {
                --bg: #f4f7f8; --surface: #ffffff; 
                --text-main: #2d3436; --text-muted: #636e72; --border: #dfe6e9;
            }
            * { box-sizing: border-box; }
            body { 
                font-family: 'Calibri', 'Segoe UI', sans-serif; background-color: var(--bg); 
                color: var(--text-main); margin: 0; padding: 0; min-height: 100vh; 
                display: flex; flex-direction: column; align-items: center; padding-bottom: 60px;
                overflow-x: hidden;
            }

            nav { 
                width: 100%; background: var(--surface); border-bottom: 1px solid var(--border);
                padding: 1.2rem 3rem; display: flex; justify-content: space-between; align-items: center; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 40px; position: sticky; top: 0; z-index: 100;
            }
            .logo { font-weight: 800; font-size: 1.6rem; color: #ff4757; }
            .badge { background: #ffeaa7; color: #d35400; padding: 6px 14px; border-radius: 20px; font-size: 0.9rem; font-weight: bold; }

            .container { width: 100%; max-width: 850px; padding: 0 20px; display: flex; flex-direction: column; gap: 30px; }
            
            .panel { 
                background: var(--surface); border: 1px solid var(--border); border-radius: 24px; padding: 40px; 
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.04); width: 100%; text-align: center;
            }
            .panel h2 { margin-top: 0; font-size: 2.2rem; margin-bottom: 10px; color: #2d3436; font-weight: 800;}
            .panel p { color: var(--text-muted); margin-bottom: 30px; font-size: 1.1rem; line-height: 1.5; }
            
            .upload-zone { 
                border: 3px dashed #74b9ff; border-radius: 20px; padding: 60px 20px; 
                background: #f0f8ff; transition: all 0.3s ease; cursor: pointer; margin-bottom: 25px; display: block; 
            }
            .upload-zone:hover { background: #e3f2fd; border-color: #0984e3; transform: scale(1.02); }
            .upload-icon { font-size: 4rem; margin-bottom: 15px; }
            #file-name { font-weight: bold; color: #0984e3; font-size: 1.2rem; }
            .file-types { font-size: 0.95rem; color: #74b9ff; margin-top: 10px; }
            input[type="file"] { display: none; }

            .btn { 
                background: linear-gradient(135deg, #FF6B6B, #feca57); color: white; border: none; 
                padding: 18px; font-size: 1.2rem; font-weight: bold; border-radius: 12px; cursor: pointer; 
                transition: all 0.3s; width: 100%; display: flex; justify-content: center; align-items: center; gap: 12px; 
                box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4); text-transform: uppercase; letter-spacing: 1px; font-family: 'Calibri', sans-serif;
            }
            .btn:hover { filter: brightness(1.1); transform: translateY(-3px); box-shadow: 0 12px 25px rgba(255, 107, 107, 0.5); }
            .btn:disabled { background: #b2bec3; cursor: not-allowed; transform: none; box-shadow: none; }

            .spinner { border: 3px solid rgba(255,255,255,0.4); border-radius: 50%; border-top: 3px solid white; width: 22px; height: 22px; animation: spin 1s linear infinite; display: none; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

            .results-panel { display: none; text-align: left; }
            .results-header { display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #f1f2f6; }
            .status-icon { background: #e8f8f5; color: #1dd1a1; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.6rem; font-weight: bold;}

            .scroll-animate {
                opacity: 0;
                transform: translateY(30px) scale(0.98);
                transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
                will-change: opacity, transform;
            }
            .scroll-animate.visible {
                opacity: 1;
                transform: translateY(0) scale(1);
            }

            .colorful-block { padding: 25px; border-radius: 16px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);}
            .bg-blue { background: #f0f8ff; border-left: 5px solid #48dbfb; }
            .bg-purple { background: #fdf4ff; border-left: 5px solid #a29bfe; }
            .bg-yellow { background: #fff9ed; border-left: 5px solid #feca57; }
            .bg-green { background: #f0fff4; border-left: 5px solid #1dd1a1; }
            
            .data-label { font-size: 1rem; font-weight: bold; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }
            .text-content { color: #2d3436; line-height: 1.7; font-size: 1.05rem; white-space: pre-wrap;}
            .data-value { font-size: 1.2rem; color: #0984e3; font-weight: bold; word-break: break-all; }

            .contact-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px; }

            .skills-grid { display: flex; flex-wrap: wrap; gap: 10px; }
            .skill-tag { background: #e0e8f9; color: #4b7bec; border: 1px solid #4b7bec; padding: 8px 16px; border-radius: 20px; font-size: 1rem; font-weight: bold; }

            .section-title { font-size: 1.6rem; color: #2d3436; margin: 40px 0 20px 0; font-weight: 800; display: flex; align-items: center; gap: 10px;}
            .job-card { background: white; border: 1px solid #dfe6e9; border-top: 5px solid #ff9f43; border-radius: 16px; padding: 25px; margin-bottom: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.04); }
            .job-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
            .job-title { font-size: 1.3rem; font-weight: bold; color: #2d3436; }
            .job-date { font-size: 0.95rem; color: #e17055; background: #ffeaa7; padding: 5px 12px; border-radius: 8px; font-weight: bold;}
            
            /* NEW: Location styling isolated from Company Name */
            .job-company { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; flex-wrap: wrap;}
            .company-name { font-size: 1.15rem; font-weight: bold; color: #636e72; }
            .location-badge { font-size: 0.85rem; color: #0984e3; background: #e3f2fd; padding: 4px 10px; border-radius: 6px; font-weight: bold; border: 1px solid #74b9ff;}
            
            .job-bullets { margin: 0; padding-left: 20px; color: #2d3436; }
            .job-bullets li { margin-bottom: 10px; line-height: 1.6; font-size: 1.05rem; }

            @media (max-width: 768px) {
                .contact-grid { grid-template-columns: 1fr; }
                .job-header { flex-direction: column; gap: 10px; }
            }
        </style>
    </head>
    <body>
        <nav>
            <div class="logo">NexusParse AI</div>
            <div class="badge">Dynamic Engine Active</div>
        </nav>

        <div class="container">
            <div class="panel">
                <h2>Upload Resume</h2>
                <p>Our AI perfectly reconstructs broken text, isolates locations, and animates data extraction.</p>
                
                <label class="upload-zone" id="drop-zone">
                    <div class="upload-icon">📄</div>
                    <div id="file-name">Click to browse files</div>
                    <div class="file-types">Supports .PDF and .DOCX</div>
                    <input type="file" id="file-input" accept=".pdf,.docx">
                </label>
                
                <button class="btn" id="submit-btn" disabled>
                    <span id="btn-text">Extract Data</span>
                    <div class="spinner" id="spinner"></div>
                </button>
            </div>

            <div class="panel results-panel" id="results-panel">
                <div class="results-header scroll-animate">
                    <div class="status-icon">✓</div>
                    <h2 style="margin: 0;">Extraction Successful</h2>
                </div>

                <div id="summary-container" class="colorful-block bg-purple scroll-animate" style="display: none;">
                    <div class="data-label">Professional Summary</div>
                    <div class="text-content" id="res-summary"></div>
                </div>

                <div class="contact-grid">
                    <div class="colorful-block bg-blue scroll-animate" style="margin-bottom: 0;">
                        <div class="data-label">Email Address</div>
                        <div class="data-value" id="res-email">...</div>
                    </div>
                    <div class="colorful-block bg-green scroll-animate" style="margin-bottom: 0;">
                        <div class="data-label">Phone Number</div>
                        <div class="data-value" id="res-phone">...</div>
                    </div>
                </div>

                <div class="colorful-block scroll-animate" style="background: white; border: 1px solid var(--border);">
                    <div class="data-label">Detected Technical Skills</div>
                    <div class="skills-grid" id="res-skills"></div>
                </div>

                <div class="section-title scroll-animate">💼 Professional Experience</div>
                <div id="res-experience"></div>

                <div id="dynamic-sections-container"></div>
            </div>
        </div>

        <script>
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    } else {
                        entry.target.classList.remove('visible');
                    }
                });
            }, { threshold: 0.1 });

            const fileInput = document.getElementById('file-input');
            const fileNameDisplay = document.getElementById('file-name');
            const submitBtn = document.getElementById('submit-btn');
            const btnText = document.getElementById('btn-text');
            const spinner = document.getElementById('spinner');
            const resultsPanel = document.getElementById('results-panel');

            fileInput.addEventListener('change', (e) => {
                if(e.target.files.length > 0) {
                    fileNameDisplay.textContent = e.target.files[0].name;
                    submitBtn.disabled = false;
                    resultsPanel.style.display = 'none'; 
                }
            });

            submitBtn.addEventListener('click', async () => {
                const file = fileInput.files[0];
                if(!file) return;

                btnText.textContent = "Scanning Document...";
                spinner.style.display = "block";
                submitBtn.disabled = true;

                const formData = new FormData();
                formData.append("file", file);

                try {
                    const response = await fetch('/parse-resume/', { method: 'POST', body: formData });
                    const jsonResponse = await response.json();
                    
                    if(response.ok) {
                        document.getElementById('res-email').textContent = jsonResponse.data.email;
                        document.getElementById('res-phone').textContent = jsonResponse.data.phone;
                        
                        if (jsonResponse.data.summary) {
                            document.getElementById('res-summary').textContent = jsonResponse.data.summary;
                            document.getElementById('summary-container').style.display = 'block';
                        } else {
                            document.getElementById('summary-container').style.display = 'none';
                        }
                        
                        const skillsContainer = document.getElementById('res-skills');
                        skillsContainer.innerHTML = '';
                        if(jsonResponse.data.skills.length > 0) {
                            jsonResponse.data.skills.forEach(skill => {
                                const span = document.createElement('span');
                                span.className = 'skill-tag';
                                span.textContent = skill;
                                skillsContainer.appendChild(span);
                            });
                        }

                        const expContainer = document.getElementById('res-experience');
                        expContainer.innerHTML = '';
                        if(jsonResponse.data.parsed_experience.length > 0) {
                            jsonResponse.data.parsed_experience.forEach(job => {
                                let bulletsHtml = job.responsibilities.map(b => `<li>${b}</li>`).join('');
                                
                                let locationHtml = job.location !== "Location Not Specified" 
                                    ? `<span class="location-badge">📍 ${job.location}</span>` 
                                    : "";
                                    
                                let html = `
                                <div class="job-card scroll-animate">
                                    <div class="job-header">
                                        <div class="job-title">${job.title}</div>
                                        <div class="job-date">⏱️ ${job.date}</div>
                                    </div>
                                    <div class="job-company">
                                        <span class="company-name">🏢 ${job.company}</span>
                                        ${locationHtml}
                                    </div>
                                    <ul class="job-bullets">${bulletsHtml}</ul>
                                </div>`;
                                expContainer.insertAdjacentHTML('beforeend', html);
                            });
                        }

                        const dynamicContainer = document.getElementById('dynamic-sections-container');
                        dynamicContainer.innerHTML = ''; 
                        
                        const otherSections = jsonResponse.data.other_sections;
                        if (Object.keys(otherSections).length > 0) {
                            const colors = ['bg-blue', 'bg-yellow', 'bg-purple', 'bg-green'];
                            for (const [sectionName, sectionContent] of Object.entries(otherSections)) {
                                const randomColor = colors[Math.floor(Math.random() * colors.length)];
                                let html = `
                                <div class="section-title scroll-animate">📌 ${sectionName}</div>
                                <div class="colorful-block ${randomColor} scroll-animate">
                                    <div class="text-content">${sectionContent}</div>
                                </div>`;
                                dynamicContainer.insertAdjacentHTML('beforeend', html);
                            }
                        }
                        
                        resultsPanel.style.display = 'block';

                        setTimeout(() => {
                            document.querySelectorAll('.scroll-animate').forEach(el => observer.observe(el));
                        }, 100);

                    } else {
                        alert("Error: " + jsonResponse.detail);
                    }
                } catch (error) {
                    alert("Failed to connect to server.");
                }

                btnText.textContent = "Extract Data";
                spinner.style.display = "none";
                submitBtn.disabled = false;
            });
        </script>
    </body>
    </html>
    """
    return html_content