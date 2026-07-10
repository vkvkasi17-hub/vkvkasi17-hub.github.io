import json
import os

print("Starting build process...")

# 1. LOAD DATA
with open('portfolio_data.json', 'r') as file:
    portfolio_data = json.load(file)

# 2. GENERATE DYNAMIC HTML CHUNKS
education_html = "" 
for edu in portfolio_data['education']:
    education_html += f'<div class="card"><h3 style="color: var(--accent); margin-top:0; font-size: 1.5rem;">{edu["degree"]}</h3><h4 style="margin:5px 0; font-size: 1.15rem;">{edu["school"]}</h4><div style="font-weight:600; color:var(--text-muted); font-size: 1.05rem;">{edu["duration"]}</div></div>'

skills_html = "<div class='skills-grid'>"
for cat, items in portfolio_data['skills'].items():
    skill_tags = "".join([f"<span class='tag skill-tag'>{i}</span>" for i in items])
    skills_html += f"<div class='card'><h3 style='font-size: 1.4rem;'>{cat}</h3><div class='tag-container'>{skill_tags}</div></div>"
skills_html += "</div>"

# --- THE STACKING EXPERIENCE LOOP ---
# --- PERFECT BLENDED MOUSE EXPERIENCE LOOP ---
# --- EXPERIENCES LOOP WITH SKILLS BADGES & ENLARGED DISNEY IMAGE ---
# --- EXPERIENCES LOOP WITH DYNAMIC AUTO-HEIGHT MAPPING ---
# --- EXPERIENCES LOOP WITH INTERACTIVE TECH CLUSTERS & COMPACT LAYOUT ---
# --- BALANCED EXPERIENCES LOOP WITH INTEGRATED TECH STACKS ---
# --- EXPERIENCES LOOP WITH PERFECTLY CENTERED ENLARGED IMAGE ---
# --- FULLY STANDARDIZED EXPERIENCE GRID SYSTEM LOOP ---
experience_html = '<div class="experience-container" style="display: flex; flex-direction: column; gap: 35px;">'
for exp in portfolio_data['experience']:
    bullets = "".join([f"<li style='margin-bottom: 12px; position: relative; padding-left: 24px;'><span style='position: absolute; left: 0; color: var(--accent);'>•</span>{b}</li>" for b in exp['bullets']])
    
    company_lower = exp["company"].lower()
    brand_graphic_html = ""
    
    # 1. Disney Experience
    if "disney" in company_lower:
        disney_skills = ["Python", "Snowflake", "SQL", "ETL", "Airflow", "API Integration"]
        badges = "".join([f"<button class='tech-badge-btn'>{tech}</button>" for tech in disney_skills])
        brand_graphic_html = f"""
        <div style="display: flex; flex: 1; justify-content: center; align-items: center; width: 100%; min-height: 220px; z-index: 1;">
            <img src="disney-logo.jpeg" 
                 style="width: 280px; height: auto; pointer-events: none; mix-blend-mode: multiply;" />
        </div>
        <div style="margin-top: auto; padding-top: 15px; border-top: 1px dashed var(--border);">
            <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); font-weight: 700; margin-bottom: 10px;">Technologies Handled</div>
            <div style="display: flex; flex-wrap: wrap;">
                {badges}
            </div>
        </div>
        """
    # 2. Cigna Experience
    elif "cigna" in company_lower:
        cigna_skills = ["Python", "FastAPI", "AWS", "Snowflake", "Docker", "GCP", "Airflow", "LLM Eval"]
        badges = "".join([f"<button class='tech-badge-btn'>{tech}</button>" for tech in cigna_skills])
        brand_graphic_html = f"""
        <div style="margin-top: auto; padding-top: 20px;">
            <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); font-weight: 700; margin-bottom: 10px;">Technologies Handled</div>
            <div style="display: flex; flex-wrap: wrap;">
                {badges}
            </div>
        </div>
        """
    # 3. Cognizant / Merck Experience
    elif "cognizant" in company_lower or "merck" in company_lower:
        cognizant_skills = ["Python", "Pandas", "Django", "SQL", "R", "Data Wrangling"]
        badges = "".join([f"<button class='tech-badge-btn'>{tech}</button>" for tech in cognizant_skills])
        brand_graphic_html = f"""
        <div style="margin-top: auto; padding-top: 20px;">
            <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); font-weight: 700; margin-bottom: 10px;">Technologies Handled</div>
            <div style="display: flex; flex-wrap: wrap;">
                {badges}
            </div>
        </div>
        """
    # 4. HAL Experience
    elif "aeronautics" in company_lower or "hal" in company_lower:
        hal_skills = ["Python", "PySpark", "Unix Shell", "Map-Reduce", "Blob Data"]
        badges = "".join([f"<button class='tech-badge-btn'>{tech}</button>" for tech in hal_skills])
        brand_graphic_html = f"""
        <div style="margin-top: auto; padding-top: 20px;">
            <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); font-weight: 700; margin-bottom: 10px;">Technologies Handled</div>
            <div style="display: flex; flex-wrap: wrap;">
                {badges}
            </div>
        </div>
        """
    # 5. Any Fallback default layout
    else:
        fallback_skills = ["Python", "Backend", "SQL", "ETL"]
        badges = "".join([f"<button class='tech-badge-btn'>{tech}</button>" for tech in fallback_skills])
        brand_graphic_html = f"""
        <div style="margin-top: auto; padding-top: 20px;">
            <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); font-weight: 700; margin-bottom: 10px;">Technologies Handled</div>
            <div style="display: flex; flex-wrap: wrap;">
                {badges}
            </div>
        </div>
        """

    experience_html += f"""
    <div class="card exp-card-grid" style="padding: 35px 40px; background: var(--card-bg); border-radius: 20px; border: 1px solid var(--border); display: grid; grid-template-columns: 32% 68%; gap: 35px; align-items: stretch; position: relative; overflow: hidden;">
        
        <div style="border-right: 1px solid var(--border); padding-right: 25px; display: flex; flex-direction: column; justify-content: space-between; position: relative; z-index: 1;">
            <div>
                <h3 style="margin: 0; font-size: 1.6rem; font-weight: 800; color: var(--text-main); line-height: 1.2;">{exp["role"]}</h3>
                
                <h4 style="margin: 6px 0 12px 0; font-size: 1.15rem; color: var(--accent); font-weight: 600;">{exp["company"]}</h4>
                
                <div style="display: inline-flex; align-items: center; font-size: 0.85rem; font-weight: 600; color: var(--text-muted); background: rgba(49, 130, 206, 0.06); padding: 5px 12px; border-radius: 8px; border: 1px solid rgba(49, 130, 206, 0.15);">
                    <i class="fa-regular fa-calendar" style="margin-right: 6px; color: var(--accent);"></i> {exp["duration"]}
                </div>
            </div>
            
            {brand_graphic_html}
        </div>
        
        <div style="margin: 0; padding-left: 5px; display: flex; align-items: center; position: relative; z-index: 2;">
            <ul style="margin: 0; padding: 0; list-style: none; color: var(--text-muted); font-size: 1.05rem; line-height: 1.75; width: 100%;">
                {bullets}
            </ul>
        </div>
        
    </div>
    """
experience_html += '</div>'

# --- PROJECTS AND OTHER SECTIONS ---
icon_mapping = { "GenAI": "fa-brain", "ML": "fa-robot", "Data Engineering": "fa-server", "Data Viz": "fa-chart-pie" }
projects_html = ""
for proj in portfolio_data['projects']:
    cat = proj["category"]
    icon = icon_mapping.get(cat, "fa-code") 
    github = proj.get("github_link", "")
    website = proj.get("website_link", "")
    overview = proj.get("overview", "")
    github_html = f'<a href="{github}" target="_blank" onclick="event.stopPropagation();" title="View Source"><i class="fa-brands fa-github"></i></a>' if github else ''
    website_html = f'<a href="{website}" target="_blank" onclick="event.stopPropagation();" title="Live Link"><i class="fa-solid fa-arrow-up-right-from-square"></i></a>' if website else ''

    projects_html += f'<div class="card new-project-card modal-trigger" style="cursor: pointer; padding: 35px;" data-category="{cat}" data-title="{proj["title"]}" data-tech="{proj["tech"]}" data-overview="{overview}" data-github="{github}" data-website="{website}">'
    projects_html += f'<div class="card-top-bar" style="margin-bottom:20px;"><div class="icon-box"><i class="fa-solid {icon}"></i></div><div class="link-icons">{github_html}{website_html}</div></div>'
    projects_html += f'<div class="card-content"><span class="category-badge-text" style="display:inline-block; margin-bottom:12px; font-weight:600; font-size: 1rem;">{cat}</span><h3 style="margin:0 0 12px 0; font-size:1.5rem;">{proj["title"]}</h3><p style="margin:0; font-size:1.1rem; color:var(--text-muted);">{proj["description"]}</p></div></div>'

certifications_html = '<div class="cert-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px;">'
if 'certifications' in portfolio_data:
    for cert in portfolio_data['certifications']:
        certifications_html += f'<div class="card cert-card cert-item" data-img="{cert.get("image", "")}" style="display:flex; align-items:center; gap:20px; padding:25px;"><i class="fa-solid fa-award cert-icon" style="font-size:2.5rem; color:var(--accent);"></i><div><h4 style="margin:0; font-size:1.3rem;">{cert["name"]}</h4><p style="margin:0; font-size:1.05rem; color:var(--text-muted);">{cert["issuer"]}</p></div></div>'
certifications_html += '</div>'

publications_html = ""
for pub in portfolio_data['publications']:
    publications_html += f'<div class="card"><a href="{pub["link"]}" target="_blank" style="text-decoration: none;"><h3 class="pub-title" style="color: var(--accent); margin:0 0 8px 0; font-size: 1.5rem;">{pub["title"]} ↗</h3></a><div class="tech" style="font-weight:600; margin-bottom:12px; font-size: 1.1rem;">{pub["journal"]} ({pub["year"]})</div><p style="margin:0; font-size: 1.1rem; color: var(--text-muted);">{pub["authors"]}</p></div>'

# 3. LOAD TEMPLATE AND INJECT DATA
with open('template.html', 'r') as file:
    final_html = file.read()

final_html = final_html.replace("[[NAME]]", portfolio_data["name"])
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
final_html = final_html.replace("[[CERTIFICATIONS_HTML]]", certifications_html) 
final_html = final_html.replace("[[PUBLICATIONS_HTML]]", publications_html)

# 4. SAVE TO INDEX.HTML
with open("index.html", "w") as file:
    file.write(final_html)

print("index.html generated successfully using modular files!")