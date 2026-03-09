import os

# 1. YOUR PORTFOLIO DATA
portfolio_data = {
    "name": "KASI MEKA",
    "profile_pic": "profile.jpeg",
    "headline": "Specializing in Backend Development, GenAI Integration & Cloud Platforms",
    
    "about_me": """
        Hi, I'm Kasi Meka — a Python Developer and Backend Engineer with over 4 years of experience specializing in backend development, data engineering, and cloud platforms (AWS, Azure, GCP). I have proven expertise in designing data pipelines, ETL/ELT processes, and scalable backend APIs using frameworks like FastAPI, Flask, and Django.
        <br><br>
        I am highly experienced in integrating Generative AI (GenAI) and Large Language Models (LLMs) into enterprise applications for chatbot evaluation, automation, and intelligent data workflows. I thrive in collaborative, Agile environments and am actively looking for new opportunities where I can contribute to innovative, data-driven projects.
    """,
    
    "education": [
        {
            "degree": "Master's in Information Science",
            "school": "University of North Texas | Denton, TX",
            "duration": "2024 - 2025",
            "color": "#3182ce" 
        }
    ],

    "experience": [
        {
            "role": "Senior Python Developer",
            "company": "Cigna Health Care | Plano, TX",
            "duration": "Jun 2024 – Present",
            "bullets": [
                "Developed Python services integrating Generative AI APIs to automate chatbot response evaluation.",
                "Designed backend data workflows using Python and SQL to support scalable analytics.",
                "Implemented automated LLM-based evaluation pipelines to assess chatbot response quality.",
                "Managed AWS cloud infrastructure using VPC, EC2, ECS, S3, and CloudFormation.",
                "Developed ETL pipelines from S3 to Snowflake using Python.",
                "Built APIs using FastAPI and Hug frameworks for cross-functional data sharing.",
                "Improved project code coverage to over 90% using automated unit testing.",
                "Built Airflow data pipelines in GCP for enterprise ETL jobs.",
                "Containerized applications using Docker and deployed via Jenkins CI/CD pipelines."
            ],
            "color": "#3182ce" 
        },
        {
            "role": "Python Developer",
            "company": "Hindustan Aeronautics Limited (HAL) | Bangalore, India",
            "duration": "Aug 2023 – Dec 2023",
            "bullets": [
                "Developed sensor logic using Python scripts and Unix shell scripting.",
                "Built Python batch processors to consume and produce various feeds.",
                "Processed massive Blob datasets using PySpark Map-Reduce.",
                "Wrote cleaning and munging scripts for large-scale datasets."
            ],
            "color": "#4a5568"
        },
        {
            "role": "Python Developer",
            "company": "Cognizant (Client: MERCK) | Hyderabad, India",
            "duration": "June 2021 - Jul 2023",
            "bullets": [
                "Managed automated data workflows using Python, SQL, and R.",
                "Developed pandas scripts for complex CSV data manipulation and comparison.",
                "Built a Django-based GUI for dynamic code documentation display.",
                "Executed long-term technological fixes for data and system bottlenecks."
            ],
            "color": "#4a5568"
        }
    ],

    "skills": {
        "Languages": ["Python", "SQL", "R", "Java", "JavaScript", "TypeScript"],
        "GenAI & Data": ["LLMs", "LangChain", "ETL/ELT", "PySpark", "Snowflake", "Pandas"],
        "Cloud & DevOps": ["AWS", "GCP", "Azure", "Docker", "Git", "FastAPI", "Airflow", "Jenkins"]
    },
    
    "projects": [
        {
            "title": "LLM-Powered Chatbot Evaluation Framework",
            "tech": "Python, LangChain, Generative AI",
            "description": "Built an automated GenAI pipeline leveraging LLM-as-a-judge methodologies to evaluate enterprise chatbot responses for relevance, specificity, and hallucination rates.",
            "category": "GenAI"
        },
        {
            "title": "Automated Resume Parsing API",
            "tech": "Python, FastAPI, NLP",
            "description": "Designed a highly scalable REST API using advanced Natural Language Processing models to extract key entities (skills, experience, education) from unstructured resume PDFs.",
            "category": "ML"
        },
        {
            "title": "Real-Time Cloud Data Ingestion Pipeline",
            "tech": "Python, AWS S3, PySpark",
            "description": "Developed a robust streaming data pipeline to automatically ingest, clean, and store high-throughput event data for downstream analytics and machine learning applications.",
            "category": "Data Engineering"
        },
        {
            "title": "ODI Cricket Analytics Dashboard",
            "tech": "Python, Tableau, Pandas",
            "description": "Utilized Python (Pandas) to clean, transform, and preprocess raw match data before designing interactive visual dashboards in Tableau to uncover 20 years of performance trends.",
            "category": "Data Viz"
        },
        {
            "title": "LA Crime Pattern Analysis",
            "tech": "Python, Data Analytics, Tableau",
            "description": "Extracted messy crime datasets using Python scripts prior to creating interactive Tableau dashboards to analyze graphical trends across Los Angeles.",
            "category": "Data Viz"
        }
    ],

    "publications": [
        {
            "title": "Standards, frameworks, and legislation for artificial intelligence (AI) transparency",
            "journal": "AI and Ethics",
            "year": "2025",
            "authors": "Lund, B., Orhan, Z., Mannuru, N. R., Bevara, R. V. K., Porter, B., Vinaih, M. K., & Bhaskara, P. (2025). Standards, frameworks, and legislation for artificial intelligence (AI) transparency. AI and Ethics, 5(4), 3639-3655.",
            "link": "https://link.springer.com/article/10.1007/s43681-025-00661-4"
        }
    ],
    
    "contact": {
        "email": "vkvkasi17@gmail.com", 
        "phone": "940-290-0996",
        "github": "vkvkasi17-hub",
        "linkedin": "meka-kasi-2193003b1"
    }
}

# 2. GENERATE DYNAMIC HTML CHUNKS
education_html = ""
for edu in portfolio_data['education']:
    education_html += f'<div class="card reveal right"><h3 style="color: var(--accent);">{edu["degree"]}</h3><h4>{edu["school"]}</h4><div class="duration">{edu["duration"]}</div></div>'

skills_html = "<div class='skills-grid'>"
for cat, items in portfolio_data['skills'].items():
    skill_tags = "".join([f"<span class='tag'>{i}</span>" for i in items])
    skills_html += f"<div class='card reveal bottom'><h3>{cat}</h3><div class='tag-container'>{skill_tags}</div></div>"
skills_html += "</div>"

experience_html = ""
for exp in portfolio_data['experience']:
    bullets = "".join([f"<li>{b}</li>" for b in exp['bullets']])
    experience_html += f'<div class="card reveal left" style="border-left: 5px solid {exp["color"]};"><h3 style="color: {exp["color"]};">{exp["role"]}</h3><h4>{exp["company"]}</h4><div class="duration">{exp["duration"]}</div><ul>{bullets}</ul></div>'

icon_mapping = {
    "GenAI": "fa-brain",
    "ML": "fa-robot",
    "Data Engineering": "fa-server",
    "Data Viz": "fa-chart-pie"
}

projects_html = ""
for i, proj in enumerate(portfolio_data['projects']):
    direction = "left" if i % 2 == 0 else "right" 
    cat = proj["category"]
    icon = icon_mapping.get(cat, "fa-code") 

    projects_html += f"""
    <div class="card reveal {direction} new-project-card" data-category="{cat}">
        <div class="card-icon-header">
            <span class="category-badge">{cat}</span>
            <i class="fa-solid {icon}"></i>
        </div>
        <div class="card-content">
            <h3>{proj['title']}</h3>
            <div class="tech">{proj['tech']}</div>
            <p>{proj['description']}</p>
        </div>
    </div>
    """
    
publications_html = ""
for pub in portfolio_data['publications']:
    publications_html += f'<div class="card reveal right"><a href="{pub["link"]}" target="_blank" style="text-decoration: none;"><h3 class="pub-title" style="color: var(--accent); cursor: pointer;">{pub["title"]} ↗</h3></a><div class="tech">{pub["journal"]} ({pub["year"]})</div><p style="font-size: 0.95rem; color: var(--text-muted);">{pub["authors"]}</p></div>'


# 3. HTML TEMPLATE STORED AS A STRING
template_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[[NAME]] | Portfolio</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg: #f8fafc;
            --nav-bg: rgba(248, 250, 252, 0.85);
            --nav-scrolled-bg: #ffffff;
            --text-main: #1a202c;
            --text-muted: #4a5568;
            --accent: #4299e1; 
            --card-bg: #ffffff;
            --border: #e2e8f0;
            --form-border: #cbd5e0;
            --submit-btn: #df9e38;
            --tag-bg: linear-gradient(145deg, #f7fafc, #edf2f7);
            --tag-text: #2d3748;
            --term-bg: #1a202c;
            --term-border: #2d3748;
            --project-header-bg: #f1f5f9;
            --logo-color: #2b6cb0; 
            --grid-color: rgba(0, 0, 0, 0.04);
            --glass-bg: rgba(255, 255, 255, 0.8);
        }
        
        body.dark-mode {
            --bg: #0b0f19;
            --nav-bg: rgba(11, 15, 25, 0.85);
            --nav-scrolled-bg: #0b0f19;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --card-bg: #111827;
            --border: #2d3748;
            --form-border: #4a5568;
            --tag-bg: linear-gradient(145deg, #1e293b, #0f172a);
            --tag-text: #e2e8f0;
            --term-bg: #000000;
            --term-border: #1e293b;
            --project-header-bg: #1e293b;
            --logo-color: #63b3ed; 
            --grid-color: rgba(255, 255, 255, 0.03);
            --glass-bg: rgba(17, 24, 39, 0.8);
        }
        
        * { box-sizing: border-box; }
        html { overflow-x: hidden; scroll-padding-top: 80px; scroll-behavior: smooth;}
        
        body {
            font-family: 'Calibri', 'Segoe UI', Tahoma, sans-serif;
            margin: 0; padding-top: 80px; 
            background-color: var(--bg); color: var(--text-main);
            line-height: 1.6; overflow-x: hidden; transition: background-color 0.4s ease, color 0.4s ease;
        }

        nav {
            position: fixed; top: 0; left: 0; width: 100%;
            background: var(--nav-bg); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            padding: 1.2rem 3rem; display: flex; justify-content: space-between; align-items: center;
            z-index: 9999; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        nav.scrolled { padding: 0.8rem 3rem; background: var(--nav-scrolled-bg); box-shadow: 0 4px 20px rgba(0,0,0,0.1); border-bottom-color: transparent; }
        .nav-left { display: flex; align-items: center; }
        .logo { font-family: 'Arial Black', Impact, sans-serif; font-size: 2.2rem; font-weight: 900; color: var(--logo-color); text-decoration: none; letter-spacing: 2px; transition: transform 0.3s ease, color 0.4s ease; }
        nav.scrolled .logo { transform: scale(0.9); }

        .nav-links { display: flex; align-items: center; gap: 2rem; }
        .nav-links a { text-decoration: none; color: var(--text-main); font-weight: 600; font-size: 1.1rem; transition: all 0.3s ease; }
        .nav-links a:hover { color: var(--accent); transform: translateY(-2px); }

        .theme-toggle-btn {
            background: transparent; border: 1px solid var(--border); border-radius: 8px;
            color: var(--text-main); cursor: pointer; padding: 6px 12px; font-size: 1.1rem;
            transition: all 0.3s ease; display: flex; align-items: center; justify-content: center;
            margin-left: 10px; 
        }
        .theme-toggle-btn:hover { border-color: var(--accent); color: var(--accent); background: var(--card-bg); }

        .hero-section { 
            position: relative; min-height: calc(100vh - 80px); display: flex; flex-direction: column; justify-content: center; align-items: center;
            overflow: hidden; z-index: 1; padding: 40px 20px;
            background-image: linear-gradient(var(--grid-color) 1px, transparent 1px), linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
            background-size: 40px 40px;
        }
        
        body.dark-mode .hero-section::before {
            content: ''; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 800px; height: 800px; border-radius: 50%; z-index: -1;
            background: radial-gradient(circle, rgba(66, 153, 225, 0.12) 0%, rgba(72, 187, 120, 0.05) 40%, transparent 70%);
            animation: pulseGlow 6s infinite alternate ease-in-out; pointer-events: none;
        }
        @keyframes pulseGlow { 0% { transform: translate(-50%, -50%) scale(0.85); opacity: 0.6; } 100% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; } }

        .hero-container { max-width: 1200px; width: 100%; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 40px; position: relative; z-index: 2; padding-bottom: 60px; }

        .hero-text { flex: 1; text-align: left; }
        .hero-text h1 { 
            font-size: 4.2rem; margin: 0; letter-spacing: -0.5px; font-weight: 800;
            background: linear-gradient(90deg, var(--text-main), var(--accent), var(--text-main));
            background-size: 200% auto; color: transparent; -webkit-background-clip: text; background-clip: text;
            animation: textShine 4s linear infinite; line-height: 1.1;
        }
        .typewriter-text { font-size: 2rem; color: var(--accent); margin-top: 10px; font-weight: bold; min-height: 45px; }
        .cursor { display: inline-block; width: 3px; background-color: var(--accent); animation: blink 1s step-end infinite; margin-left: 2px; }
        .hero-desc { font-size: 1.2rem; color: var(--text-muted); margin-top: 15px; margin-bottom: 30px; font-weight: bold; max-width: 90%; }
        
        .hero-ctas { display: flex; gap: 15px; margin-bottom: 25px; }
        .btn-primary { background: var(--accent); color: white; padding: 12px 28px; border-radius: 30px; font-weight: bold; text-decoration: none; font-size: 1.1rem; transition: all 0.3s; box-shadow: 0 4px 15px rgba(66, 153, 225, 0.4); border: none; cursor: pointer; }
        .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(66, 153, 225, 0.6); }
        .btn-secondary { background: transparent; color: var(--text-main); padding: 12px 28px; border-radius: 30px; font-weight: bold; text-decoration: none; font-size: 1.1rem; border: 2px solid var(--border); transition: all 0.3s; }
        .btn-secondary:hover { border-color: var(--accent); color: var(--accent); }

        .hero-socials { display: flex; gap: 20px; }
        .hero-socials a { color: var(--text-muted); font-size: 1.5rem; transition: all 0.3s ease; }
        .hero-socials a:hover { color: var(--accent); transform: translateY(-3px); }

        .hero-visual { flex: 1; display: flex; justify-content: center; position: relative; padding: 20px 0;} /* Added vertical padding for spacing */
        .image-wrapper { position: relative; display: inline-block; }
        .profile-img-large { 
            width: 320px; height: 320px; border-radius: 50%; object-fit: cover; 
            border: 4px solid var(--border); box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.3s;
        }
        .image-wrapper:hover .profile-img-large { transform: scale(1.05) rotate(2deg); border-color: var(--accent); }

        .marquee-container { position: absolute; bottom: 0; left: 0; width: 100%; background: var(--nav-bg); backdrop-filter: blur(5px); border-top: 1px solid var(--border); padding: 12px 0; overflow: hidden; white-space: nowrap; z-index: 3; }
        .marquee-content { display: inline-block; animation: scrollMarquee 25s linear infinite; }
        .marquee-content span { font-size: 1.1rem; font-weight: bold; color: var(--text-muted); margin: 0 15px; letter-spacing: 1px; }
        @keyframes scrollMarquee { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

        .container { max-width: 1200px; margin: 0 auto; padding: 60px 30px; }
        .section-title { font-size: 2.2rem; font-weight: 800; color: var(--text-main); margin-bottom: 15px; text-align: center; display: block; }
        .title-underline { height: 4px; width: 60px; margin: 0 auto 30px auto; background: linear-gradient(90deg, #4299e1, #48bb78); border-radius: 2px; }

        .card { background: var(--card-bg); border: 1px solid var(--border); padding: 40px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease, background-color 0.4s ease, border-color 0.4s ease; }
        .card:hover { transform: translateY(-8px) scale(1.01); box-shadow: 0 15px 35px rgba(0,0,0,0.08); border-color: var(--accent); }

        .duration { font-size: 1rem; color: var(--text-muted); margin-bottom: 15px; font-style: italic; }
        .tech { font-weight: bold; color: var(--accent); font-size: 1rem; margin-bottom: 10px; }
        .pub-title:hover { text-decoration: underline; color: #2b6cb0 !important; }

        .tag-container { display: flex; flex-wrap: wrap; gap: 12px; }
        .tag { background: var(--tag-bg); color: var(--tag-text); padding: 10px 18px; border-radius: 30px; font-size: 0.95rem; font-weight: bold; border: 1px solid var(--border); transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: relative; overflow: hidden; z-index: 1; cursor: default; }
        .tag::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, #4299e1, #48bb78); z-index: -1; transition: opacity 0.4s ease; opacity: 0; }
        .tag:hover { transform: translateY(-5px) scale(1.05); color: white; border-color: transparent; box-shadow: 0 10px 20px rgba(66, 153, 225, 0.3); }
        .tag:hover::before { opacity: 1; }

        .filter-container { display: flex; justify-content: center; flex-wrap: wrap; gap: 15px; margin-bottom: 30px; }
        .filter-btn { padding: 10px 25px; font-size: 1rem; font-weight: bold; font-family: 'Calibri', sans-serif; border-radius: 30px; cursor: pointer; border: 1px solid var(--border); background-color: var(--card-bg); color: var(--text-muted); transition: all 0.3s ease; }
        .filter-btn:hover { border-color: var(--accent); color: var(--text-main); }
        .filter-btn.active { background-color: var(--accent); color: white; border-color: var(--accent); box-shadow: 0 4px 15px rgba(66, 153, 225, 0.4); }
        .project-hidden { display: none !important; }

        .skills-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 25px; }
        
        .new-project-card { padding: 0; display: flex; flex-direction: column; overflow: hidden; border-top: 4px solid var(--accent); }
        .card-icon-header { background-color: var(--project-header-bg); height: 150px; display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 1px solid var(--border); position: relative; }
        .card-icon-header i { font-size: 3.5rem; color: var(--accent); opacity: 0.7; }
        .category-badge { position: absolute; top: 15px; right: 15px; background: var(--card-bg); border: 1px solid var(--border); padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; color: var(--text-muted); }
        .card-content { padding: 30px; flex-grow: 1; display: flex; flex-direction: column; }
        .card-content h3 { margin-top: 0; margin-bottom: 10px; font-size: 1.3rem;}
        .card-content p { margin-bottom: 0; font-size: 0.95rem; }

        .game-container { 
            background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px;
            padding: 40px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 40px;
        }
        .score-board { font-family: 'Courier New', monospace; font-size: 1.8rem; font-weight: bold; display: flex; justify-content: center; gap: 40px; margin-bottom: 25px; }
        .user-score { color: var(--accent); }
        .ai-score { color: #fc8181; }
        
        .game-log {
            min-height: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center;
            background: var(--term-bg); border: 1px solid var(--term-border); border-radius: 8px; 
            margin-bottom: 25px; padding: 20px; color: var(--text-main); font-family: 'Courier New', monospace;
        }
        
        .rps-btn {
            background: transparent; color: var(--text-main); padding: 12px 24px; border-radius: 8px;
            font-weight: bold; font-size: 1.2rem; border: 2px solid var(--border); cursor: pointer;
            transition: all 0.3s;
        }
        .rps-btn:hover { border-color: var(--accent); color: var(--accent); transform: translateY(-3px); box-shadow: 0 4px 10px rgba(66, 153, 225, 0.2); }
        .rps-btn:active { transform: translateY(0); }

        .contact-wrapper { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: stretch; }
        .interactive-terminal { background: var(--term-bg); border-radius: 12px; overflow: hidden; color: #e2e8f0; font-family: 'Courier New', Courier, monospace; font-size: 0.95rem; display: flex; flex-direction: column; box-shadow: 0 10px 25px rgba(0,0,0,0.1); transition: transform 0.3s ease, background-color 0.4s ease; border: 1px solid var(--term-border); }
        .interactive-terminal:hover { transform: scale(1.02) translateY(-5px); box-shadow: 0 15px 35px rgba(0,0,0,0.2); }
        .term-header { background: var(--border); padding: 12px 15px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--form-border); }
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .dot.red { background: #fc8181; } .dot.yellow { background: #f6e05e; } .dot.green { background: #68d391; }
        .term-title { margin: 0 auto; font-size: 0.85rem; color: var(--text-main); font-weight: bold; }
        .term-body { padding: 25px; flex-grow: 1; }
        .prompt { color: #68d391; font-weight: bold; margin-right: 8px; }
        .term-output { color: #fbd38d; margin: 15px 0 15px 25px; line-height: 1.6; }
        .term-output a { color: #63b3ed; text-decoration: none; }
        .term-output a:hover { text-decoration: underline; }
        
        .form-container { background: var(--card-bg); padding: 35px; border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); transition: background-color 0.4s ease, border-color 0.4s ease; }
        .form-group { display: flex; flex-direction: column; text-align: left; margin-bottom: 20px; }
        .form-group label { margin-bottom: 8px; font-weight: 600; color: var(--text-main); font-size: 1.05rem; }
        .form-group input, .form-group textarea { padding: 12px; border: 1px solid var(--form-border); color: var(--text-main); border-radius: 6px; font-family: 'Calibri', sans-serif; font-size: 1rem; background-color: transparent; transition: border-color 0.3s, box-shadow 0.3s; }
        .form-group input:focus, .form-group textarea:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2); }
        .submit-btn { background-color: var(--submit-btn); color: black; font-weight: bold; font-size: 1.2rem; padding: 15px; border: 1px solid var(--form-border); border-radius: 30px; cursor: pointer; transition: all 0.3s; width: 100%; font-family: 'Calibri', sans-serif; margin-top: 10px; border: none;}
        .submit-btn:hover { opacity: 0.9; transform: translateY(-3px); box-shadow: 0 5px 15px rgba(223, 158, 56, 0.4); }

        footer { padding: 40px 3rem; border-top: 1px solid var(--border); background: var(--bg); display: flex; justify-content: space-between; align-items: center; transition: background-color 0.4s ease; }
        .footer-left { display: flex; flex-direction: column; gap: 5px; }
        .footer-logo { font-size: 1.5rem; font-weight: 800; color: var(--accent); text-decoration: none; font-family: 'Arial Black', sans-serif; }
        .footer-copy { color: var(--text-muted); font-size: 0.95rem; margin: 0;}
        .footer-icons { display: flex; gap: 20px; }
        .footer-icons a { color: var(--text-muted); font-size: 1.5rem; transition: all 0.3s ease; }
        .footer-icons a:hover { color: var(--accent); transform: translateY(-3px); }

        #scrollTopBtn { position: fixed; bottom: 30px; right: 30px; z-index: 99; font-size: 1.2rem; border: none; outline: none; background-color: var(--accent); color: white; cursor: pointer; width: 45px; height: 45px; border-radius: 50%; box-shadow: 0 4px 15px rgba(66, 153, 225, 0.4); opacity: 0; transform: translateY(20px); transition: all 0.3s ease; pointer-events: none; display: flex; justify-content: center; align-items: center; }
        #scrollTopBtn.show { opacity: 1; transform: translateY(0); pointer-events: auto; }
        #scrollTopBtn:hover { background-color: #2b6cb0; transform: translateY(-5px); box-shadow: 0 6px 20px rgba(66, 153, 225, 0.6); }

        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); backdrop-filter: blur(5px); display: flex; justify-content: center; align-items: center; z-index: 10000; opacity: 0; pointer-events: none; transition: opacity 0.4s ease; }
        .modal-overlay.show { opacity: 1; pointer-events: auto; }
        .modal-content { background: var(--card-bg); padding: 40px; border-radius: 15px; text-align: center; max-width: 500px; width: 90%; transform: scale(0.8); transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); box-shadow: 0 20px 50px rgba(0,0,0,0.2); border-top: 5px solid var(--accent); }
        .modal-overlay.show .modal-content { transform: scale(1); }
        .modal-content h2 { margin-top: 0; color: var(--text-main); font-size: 2rem; }
        .modal-content p { font-size: 1.15rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 25px; }
        
        .progress-container { width: 100%; height: 6px; background-color: var(--border); border-radius: 3px; margin-bottom: 25px; overflow: hidden; }
        .progress-bar { height: 100%; width: 100%; background-color: var(--accent); transform-origin: left; }
        @keyframes shrinkBar { from { transform: scaleX(1); } to { transform: scaleX(0); } }
        .progress-bar.animate { animation: shrinkBar 9s linear forwards; }

        .close-btn { background: var(--accent); color: white; border: none; padding: 12px 30px; font-size: 1.1rem; font-weight: bold; border-radius: 30px; cursor: pointer; transition: all 0.3s; }
        .close-btn:hover { background: #2b6cb0; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(66, 153, 225, 0.4); }

        .reveal { opacity: 0; transition: all 0.9s cubic-bezier(0.25, 0.46, 0.45, 0.94); }
        .reveal.bottom { transform: translateY(60px); }
        .reveal.left { transform: translateX(-60px); }
        .reveal.right { transform: translateX(60px); }
        .reveal.active { opacity: 1; transform: translate(0, 0); }

        @media (max-width: 900px) {
            nav { padding: 1rem 1.5rem; }
            .nav-links { display: none; } 
            
            .hero-container { flex-direction: column-reverse; text-align: center; gap: 20px; padding-top: 20px;}
            .hero-text { text-align: center; }
            .hero-ctas { justify-content: center; }
            .hero-socials { justify-content: center; }
            .hero-text h1 { font-size: 3.2rem; }
            .profile-img-large { width: 220px; height: 220px; }
            
            footer { flex-direction: column; gap: 20px; text-align: center; }
            .contact-wrapper { grid-template-columns: 1fr; }
            .container { padding: 30px 15px; }
        }
    </style>
</head>
<body>
    <div class="modal-overlay" id="celebrationModal">
        <div class="modal-content">
            <h2>🎉 Thank You! 🎉</h2>
            <p>You have visited my website and reached the bottom of it! I think you are impressed with my portfolio. 
            <br><br>
            Thanks for visiting!</p>
            <div class="progress-container">
                <div class="progress-bar" id="modalProgressBar"></div>
            </div>
            <button class="close-btn" onclick="closeModal()">Close</button>
        </div>
    </div>

    <nav id="navbar">
        <div class="nav-left">
            <a href="#" class="logo">KM</a>
        </div>
        <div class="nav-links">
            <a href="#about">About</a>
            <a href="#experience">Experience</a>
            <a href="#education">Education</a>
            <a href="#skills">Skills</a>
            <a href="#projects">Projects</a>
            <a href="#game">AI Bot</a>
            <a href="#contact">Contact</a>
            
            <button id="themeToggle" class="theme-toggle-btn" aria-label="Toggle Dark Mode">
                <i class="fa-solid fa-moon"></i>
            </button>
        </div>
    </nav>

    <header class="hero-section">
        <div class="hero-container">
            <div class="hero-text reveal left">
                <h1>[[NAME]]</h1>
                <div class="typewriter-text"><span id="typewriter"></span><span class="cursor">&nbsp;</span></div>
                <p class="hero-desc">[[HEADLINE]]</p>
                
                <div class="hero-ctas">
                    <a href="#projects" class="btn-primary">View Projects</a>
                    <a href="#contact" class="btn-secondary">Contact Me</a>
                </div>
                
                <div class="hero-socials">
                    <a href="https://linkedin.com/in/[[LINKEDIN]]" target="_blank" aria-label="LinkedIn"><i class="fa-brands fa-linkedin-in"></i></a>
                    <a href="https://github.com/[[GITHUB]]" target="_blank" aria-label="GitHub"><i class="fa-brands fa-github"></i></a>
                    <a href="mailto:[[EMAIL]]" aria-label="Email"><i class="fa-regular fa-envelope"></i></a>
                </div>
            </div>
            
            <div class="hero-visual reveal right">
                <div class="image-wrapper">
                    <img src="[[PROFILE_PIC]]" class="profile-img-large" onerror="this.style.display='none'">
                    </div>
            </div>
        </div>

        <div class="marquee-container reveal bottom">
            <div class="marquee-content">
                <span>Python • AWS • LangChain • FastAPI • Snowflake • Docker • SQL • GCP • Data Engineering • Machine Learning • </span>
                <span>Python • AWS • LangChain • FastAPI • Snowflake • Docker • SQL • GCP • Data Engineering • Machine Learning • </span>
            </div>
        </div>
    </header>

    <section id="about" class="container">
        <span class="section-title reveal bottom">About Me</span>
        <div class="title-underline reveal bottom"></div>
        <div class="card reveal bottom">
            <p style="margin:0; font-size: 1.25rem;">[[ABOUT_ME]]</p>
        </div>
    </section>

    <section id="experience" class="container">
        <span class="section-title reveal bottom">Professional Experience</span>
        <div class="title-underline reveal bottom"></div>
        [[EXPERIENCE_HTML]]
    </section>

    <section id="education" class="container">
        <span class="section-title reveal bottom">Education</span>
        <div class="title-underline reveal bottom"></div>
        [[EDUCATION_HTML]]
    </section>

    <section id="skills" class="container">
        <span class="section-title reveal bottom">Technical Expertise</span>
        <div class="title-underline reveal bottom"></div>
        [[SKILLS_HTML]]
    </section>

    <section id="projects" class="container">
        <span class="section-title reveal bottom">Featured Research & Projects</span>
        <div class="title-underline reveal bottom"></div>
        
        <div class="filter-container reveal bottom">
            <button class="filter-btn active" onclick="filterProjects('all')">All</button>
            <button class="filter-btn" onclick="filterProjects('GenAI')">GenAI</button>
            <button class="filter-btn" onclick="filterProjects('ML')">ML</button>
            <button class="filter-btn" onclick="filterProjects('Data Engineering')">Data Eng</button>
            <button class="filter-btn" onclick="filterProjects('Data Viz')">Data Viz</button>
        </div>

        <div class="skills-grid" id="project-grid">
            [[PROJECTS_HTML]]
        </div>
    </section>
    
    <section id="publications" class="container">
        <span class="section-title reveal bottom">Research & Publications</span>
        <div class="title-underline reveal bottom"></div>
        [[PUBLICATIONS_HTML]]
    </section>

    <section id="game" class="container">
        <span class="section-title reveal bottom">Beat the AI 🤖</span>
        <div class="title-underline reveal bottom"></div>
        
        <div class="game-container reveal bottom">
            <h3 style="margin-top: 0;">Predictive Rock-Paper-Scissors</h3>
            <p style="color: var(--text-muted); margin-bottom: 20px;">
                This bot uses a simple <b>Markov Chain</b> algorithm to learn your patterns and predict your next move.<br>See if you can trick it!
            </p>
            
            <div class="score-board">
                <div>You: <span id="userScore" class="user-score">0</span></div>
                <div>AI: <span id="aiScore" class="ai-score">0</span></div>
            </div>
            
            <div id="gameLog" class="game-log">
                <div style="color: var(--text-muted); font-size: 1.1rem;">Make your move below to start the algorithm.</div>
            </div>
            
            <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
                <button class="rps-btn" onclick="playRPS('rock')">✊ Rock</button>
                <button class="rps-btn" onclick="playRPS('paper')">✋ Paper</button>
                <button class="rps-btn" onclick="playRPS('scissors')">✌️ Scissors</button>
            </div>
        </div>
    </section>

    <section id="contact" class="container">
        <span class="section-title reveal bottom">Contact Me</span>
        <div class="title-underline reveal bottom"></div>
        
        <div class="contact-wrapper reveal bottom">
            <div class="interactive-terminal">
                <div class="term-header">
                    <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
                    <span class="term-title">contact_kasi.py</span>
                </div>
                <div class="term-body">
                    <p><span class="prompt">>>></span> import developer</p>
                    <p><span class="prompt">>>></span> kasi = developer.get("Kasi Meka")</p>
                    <p><span class="prompt">>>></span> kasi.contact()</p>
                    <div class="term-output">
                        {<br>
                        &nbsp;&nbsp;"email": "<a href='mailto:[[EMAIL]]'>[[EMAIL]]</a>",<br>
                        &nbsp;&nbsp;"phone": "[[PHONE]]",<br>
                        &nbsp;&nbsp;"github": "<a href='https://github.com/[[GITHUB]]' target='_blank'>/[[GITHUB]]</a>",<br>
                        &nbsp;&nbsp;"status": "Available for 2026 Internships"<br>
                        }
                    </div>
                    <p><span class="prompt">>>></span> <span class="cursor" style="background-color: white;">&nbsp;</span></p>
                </div>
            </div>

            <div class="form-container">
                <form action="mailto:[[EMAIL]]?subject=Portfolio Contact" method="POST" enctype="text/plain">
                    <div class="form-group">
                        <label>Name *</label>
                        <input type="text" name="Name" required placeholder="John Doe">
                    </div>
                    <div class="form-group">
                        <label>Email *</label>
                        <input type="email" name="Email" required placeholder="john@example.com">
                    </div>
                    <div class="form-group" style="margin-bottom: 25px;">
                        <label>Message *</label>
                        <textarea name="Message" rows="4" required placeholder="Hello Kasi, I am reaching out regarding..."></textarea>
                    </div>
                    <button type="submit" class="submit-btn">Send Message</button>
                </form>
            </div>
        </div>
    </section>

    <footer>
        <div class="footer-left">
            <a href="#" class="footer-logo logo">KM</a>
            <p class="footer-copy">© 2026 [[NAME]]. All rights reserved.</p>
        </div>
        <div class="footer-icons">
            <a href="https://linkedin.com/in/[[LINKEDIN]]" target="_blank" aria-label="LinkedIn"><i class="fa-brands fa-linkedin-in"></i></a>
            <a href="https://github.com/[[GITHUB]]" target="_blank" aria-label="GitHub"><i class="fa-brands fa-github"></i></a>
            <a href="mailto:[[EMAIL]]" aria-label="Email"><i class="fa-regular fa-envelope"></i></a>
        </div>
    </footer>

    <button id="scrollTopBtn" title="Go to top"><i class="fa-solid fa-arrow-up"></i></button>

    <script>
        // --- GENERAL JS LOGIC ---
        const themeToggleBtn = document.getElementById('themeToggle');
        const body = document.body;
        const icon = themeToggleBtn.querySelector('i');

        const savedTheme = localStorage.getItem('portfolio-theme');
        if (savedTheme === 'dark') {
            body.classList.add('dark-mode');
            icon.classList.replace('fa-moon', 'fa-sun');
        }

        themeToggleBtn.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            if (body.classList.contains('dark-mode')) {
                localStorage.setItem('portfolio-theme', 'dark');
                icon.classList.replace('fa-moon', 'fa-sun');
            } else {
                localStorage.setItem('portfolio-theme', 'light');
                icon.classList.replace('fa-sun', 'fa-moon');
            }
        });

        window.addEventListener('scroll', () => {
            const navbar = document.getElementById('navbar');
            if (window.scrollY > 20) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        const titles = [
            "Python Developer", "Generative AI Engineer", "Backend Specialist", "Data Engineer",
            "Python Developer | Generative AI | Backend Engineer"
        ];
        let count = 0; let index = 0; let currentText = ''; let letter = ''; let isDeleting = false;

        function type() {
            if (count === titles.length) { count = 0; }
            currentText = titles[count];
            
            if (isDeleting) { letter = currentText.slice(0, --index); } 
            else { letter = currentText.slice(0, ++index); }
            
            document.getElementById('typewriter').textContent = letter;
            let typeSpeed = isDeleting ? 30 : 70;
            
            if (!isDeleting && letter.length === currentText.length) {
                typeSpeed = (count === titles.length - 1) ? 4000 : 2000; 
                isDeleting = true;
            } else if (isDeleting && letter.length === 0) {
                isDeleting = false; count++; typeSpeed = 500; 
            }
            setTimeout(type, typeSpeed);
        }
        document.addEventListener("DOMContentLoaded", type);

        function filterProjects(category) {
            const buttons = document.querySelectorAll('.filter-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            const projects = document.querySelectorAll('.new-project-card');
            projects.forEach(project => {
                project.classList.remove('active'); 
                if (category === 'all' || project.dataset.category === category) {
                    project.classList.remove('project-hidden');
                } else { project.classList.add('project-hidden'); }
            });
            setTimeout(reveal, 50);
        }

        let hasCelebrated = false;
        let closeTimeout; 

        function reveal() {
            var reveals = document.querySelectorAll(".reveal");
            var windowHeight = window.innerHeight;
            
            for (var i = 0; i < reveals.length; i++) {
                if(reveals[i].classList.contains('project-hidden')) continue; 
                var elementTop = reveals[i].getBoundingClientRect().top;
                var elementBottom = reveals[i].getBoundingClientRect().bottom;
                
                if (elementTop < windowHeight - 50 && elementBottom > 0) { reveals[i].classList.add("active"); } 
                else { reveals[i].classList.remove("active"); }
            }

            var arrowBtn = document.getElementById("scrollTopBtn");
            if (window.scrollY > 400) { arrowBtn.classList.add("show"); } 
            else { arrowBtn.classList.remove("show"); }

            if (!hasCelebrated && (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 150) {
                hasCelebrated = true; 
                var duration = 3000; var end = Date.now() + duration;
                (function frame() {
                    confetti({ particleCount: 7, angle: 60, spread: 55, origin: { x: 0 }, colors: ['#4299e1', '#48bb78', '#df9e38'] });
                    confetti({ particleCount: 7, angle: 120, spread: 55, origin: { x: 1 }, colors: ['#4299e1', '#48bb78', '#df9e38'] });
                    if (Date.now() < end) { requestAnimationFrame(frame); }
                }());
                
                setTimeout(() => { 
                    document.getElementById('celebrationModal').classList.add('show'); 
                    document.getElementById('modalProgressBar').classList.add('animate');
                    
                    closeTimeout = setTimeout(() => {
                        closeModal();
                    }, 9000);
                }, 500);
            }
        }
        
        window.addEventListener("scroll", reveal);
        setTimeout(reveal, 100);

        function closeModal() { 
            document.getElementById('celebrationModal').classList.remove('show'); 
            document.getElementById('modalProgressBar').classList.remove('animate');
            clearTimeout(closeTimeout); 
        }

        document.getElementById("scrollTopBtn").addEventListener("click", function(e) {
            e.preventDefault();
            const scrollDuration = 1200; const startY = window.scrollY; const startTime = performance.now();
            function step(currentTime) {
                const timeElapsed = currentTime - startTime;
                const progress = Math.min(timeElapsed / scrollDuration, 1);
                const ease = progress < 0.5 ? 4 * progress * progress * progress : 1 - Math.pow(-2 * progress + 2, 3) / 2;
                window.scrollTo(0, startY * (1 - ease));
                if (progress < 1) { requestAnimationFrame(step); }
            }
            requestAnimationFrame(step);
        });

        // --- PREDICTIVE "BEAT THE AI" LOGIC ---
        const userScoreEl = document.getElementById('userScore');
        const aiScoreEl = document.getElementById('aiScore');
        const gameLog = document.getElementById('gameLog');

        let uScore = 0;
        let aScore = 0;
        let lastUserMove = null;

        const history = {
            'rock': { 'rock': 0, 'paper': 0, 'scissors': 0 },
            'paper': { 'rock': 0, 'paper': 0, 'scissors': 0 },
            'scissors': { 'rock': 0, 'paper': 0, 'scissors': 0 }
        };

        const moves = ['rock', 'paper', 'scissors'];
        const beats = { 'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper' };
        const losesTo = { 'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock' };
        const emojis = { 'rock': '✊', 'paper': '✋', 'scissors': '✌️' };

        function playRPS(userMove) {
            let aiMove = moves[Math.floor(Math.random() * 3)];

            if (lastUserMove) {
                const pastMoves = history[lastUserMove];
                let predictedMove = 'rock';
                let maxCount = -1;
                
                for (const move of moves) {
                    if (pastMoves[move] > maxCount) {
                        maxCount = pastMoves[move];
                        predictedMove = move;
                    }
                }
                
                if (maxCount > 0) {
                    aiMove = losesTo[predictedMove];
                }
            }

            if (lastUserMove) {
                history[lastUserMove][userMove]++;
            }
            lastUserMove = userMove;

            let resultText = '';
            let resultColor = '';
            
            if (userMove === aiMove) {
                resultText = "It's a Tie!";
                resultColor = "var(--text-muted)";
            } else if (beats[userMove] === aiMove) {
                resultText = "You Win! 🎉";
                resultColor = "var(--accent)";
                uScore++;
            } else {
                resultText = "AI Wins! 🤖";
                resultColor = "#fc8181";
                aScore++;
            }

            userScoreEl.innerText = uScore;
            aiScoreEl.innerText = aScore;
            
            gameLog.innerHTML = `
                <div style="font-size: 1.1rem; color: var(--text-main); margin-bottom: 15px;">
                    You <span style="font-size: 2.5rem; margin: 0 15px;">${emojis[userMove]}</span> 
                    <span style="color: var(--text-muted);">vs</span> 
                    <span style="font-size: 2.5rem; margin: 0 15px;">${emojis[aiMove]}</span> AI
                </div>
                <div style="font-weight: bold; font-size: 1.3rem; color: ${resultColor};">${resultText}</div>
            `;
        }
    </script>
</body>
</html>
"""

# 4. INJECT AND SAVE
final_html = template_content.replace("[[NAME]]", portfolio_data["name"])
final_html = final_html.replace("[[PROFILE_PIC]]", portfolio_data["profile_pic"])
final_html = final_html.replace("[[HEADLINE]]", portfolio_data["headline"])
final_html = final_html.replace("[[ABOUT_ME]]", portfolio_data["about_me"])
final_html = final_html.replace("[[EMAIL]]", portfolio_data["contact"]["email"])
final_html = final_html.replace("[[PHONE]]", portfolio_data["contact"]["phone"])
final_html = final_html.replace("[[GITHUB]]", portfolio_data["contact"]["github"])
final_html = final_html.replace("[[LINKEDIN]]", portfolio_data["contact"]["linkedin"])

final_html = final_html.replace("[[EDUCATION_HTML]]", education_html)
final_html = final_html.replace("[[SKILLS_HTML]]", skills_html)
final_html = final_html.replace("[[EXPERIENCE_HTML]]", experience_html)
final_html = final_html.replace("[[PROJECTS_HTML]]", projects_html)
final_html = final_html.replace("[[PUBLICATIONS_HTML]]", publications_html)

with open("index.html", "w") as file:
    file.write(final_html)

print("Glass tiles removed and layout polished successfully!")