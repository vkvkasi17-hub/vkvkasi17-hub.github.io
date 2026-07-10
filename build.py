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
experience_html = '<div class="experience-container">'
for exp in portfolio_data['experience']:
    bullets = "".join([f"<li style='margin-bottom: 14px; position: relative; padding-left: 24px;'><span style='position: absolute; left: 0; top: 0; font-size: 1.3rem; font-weight: bold;'>•</span>{b}</li>" for b in exp['bullets']])
    color = "var(--accent)"
    
    # --- OPTION 1: MINIMALIST TIMELINE LOOP ---
experience_html = '<div class="experience-container" style="position: relative; padding-left: 20px; border-left: 2px solid var(--border); margin-left: 10px;">'
for exp in portfolio_data['experience']:
    bullets = "".join([f"<li style='margin-bottom: 12px; position: relative; padding-left: 20px;'><span style='position: absolute; left: 0; color: var(--accent);'>•</span>{b}</li>" for b in exp['bullets']])
    
    # --- OPTION 2: SPLIT-GRID LAYOUT LOOP ---
experience_html = '<div class="experience-container" style="display: flex; flex-direction: column; gap: 35px;">'
for exp in portfolio_data['experience']:
    bullets = "".join([f"<li style='margin-bottom: 14px; position: relative; padding-left: 20px;'><span style='position: absolute; left: 0; color: var(--accent);'>•</span>{b}</li>" for b in exp['bullets']])
    
    # --- ENHANCED SPLIT-GRID LAYOUT LOOP (FILLED LEFT COLUMN) ---
experience_html = '<div class="experience-container" style="display: flex; flex-direction: column; gap: 35px;">'
for exp in portfolio_data['experience']:
    bullets = "".join([f"<li style='margin-bottom: 14px; position: relative; padding-left: 20px;'><span style='position: absolute; left: 0; color: var(--accent);'>•</span>{b}</li>" for b in exp['bullets']])
    
    # 1. Dynamically pull or fallback tech tags to fill the empty space
    # (If your json has a 'tech' key for experience, it uses it; otherwise it defaults to these)
    tech_tags = exp.get("tech", ["Python", "Snowflake", "SQL", "ETL", "AWS"])
    tech_badges = "".join([f"<span style='display: inline-block; background: rgba(255,255,255,0.03); border: 1px solid var(--border); color: var(--text-muted); font-size: 0.8rem; font-weight: 500; padding: 4px 10px; border-radius: 6px; margin: 0 6px 6px 0;'>{t}</span>" for t in tech_tags])
    
    # --- EXPERIENCE LOOP WITH DYNAMIC BRAND ICONS ---
experience_html = '<div class="experience-container" style="display: flex; flex-direction: column; gap: 35px;">'
for exp in portfolio_data['experience']:
    bullets = "".join([f"<li style='margin-bottom: 14px; position: relative; padding-left: 24px;'><span style='position: absolute; left: 0; color: var(--accent);'>•</span>{b}</li>" for b in exp['bullets']])
    
    # Check the company name to set up custom branding graphics/icons
    company_lower = exp["company"].lower()
    brand_graphic_html = ""
    
    if "disney" in company_lower:
        # High-end FontAwesome Mickey/Glow structure or themed icon
        brand_graphic_html = """
        <div style="position: absolute; bottom: -10px; left: 20px; font-size: 7.5rem; color: var(--accent); opacity: 0.08; pointer-events: none; transform: rotate(-10deg);">
            <i class="fa-solid fa-wand-magic-sparkles"></i>
        </div>
        """
    elif "aeronautics" in company_lower or "hal" in company_lower:
        brand_graphic_html = """
        <div style="position: absolute; bottom: -10px; left: 20px; font-size: 7.5rem; color: var(--accent); opacity: 0.08; pointer-events: none; transform: rotate(-15deg);">
            <i class="fa-solid fa-plane-jet"></i>
        </div>
        """
    else:
        brand_graphic_html = """
        <div style="position: absolute; bottom: -10px; left: 20px; font-size: 7.5rem; color: var(--accent); opacity: 0.05; pointer-events: none;">
            <i class="fa-solid fa-briefcase"></i>
        </div>
        """

    # --- EXPERIENCE LOOP WITH TRUE BRAND VECTOR WATERMARKS ---
# --- EXPERIENCE LOOP WITH LOCAL BRAND WATERMARKS ---
# --- EXPERIENCE LOOP WITH CENTERED SOLID IMAGES ---
# --- CLEAN SPLIT-GRID LAYOUT LOOP WITH LARGE BLENDED IMAGE ---
experience_html = '<div class="experience-container" style="display: flex; flex-direction: column; gap: 35px;">'
for exp in portfolio_data['experience']:
    bullets = "".join([f"<li style='margin-bottom: 14px; position: relative; padding-left: 24px;'><span style='position: absolute; left: 0; color: var(--accent);'>•</span>{b}</li>" for b in exp['bullets']])
    
    company_lower = exp["company"].lower()
    brand_graphic_html = ""
    
    # Target only the Disney role to inject the large, seamless image
    if "disney" in company_lower:
        brand_graphic_html = """
        <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-top: auto; margin-bottom: auto; padding-top: 20px; z-index: 1;">
            <img src="disney-logo.jpeg" 
                 style="width: 220px; height: auto; pointer-events: none; mix-blend-mode: multiply;" />
        </div>
        """
    # Other experiences are now completely empty on the left side as requested
    else:
        brand_graphic_html = ""

    experience_html += f"""
    <div class="card exp-card-grid" style="padding: 40px; background: var(--card-bg); border-radius: 20px; border: 1px solid var(--border); display: grid; grid-template-columns: 32% 68%; gap: 35px; align-items: start; position: relative; overflow: hidden;">
        
        <div style="border-right: 1px solid var(--border); padding-right: 25px; height: 100%; display: flex; flex-direction: column; min-height: 340px; position: relative; z-index: 1;">
            <div style="position: relative; z-index: 2;">
                <h3 style="margin: 0; font-size: 1.65rem; font-weight: 800; color: var(--text-main); line-height: 1.2;">{exp["role"]}</h3>
                
                <h4 style="margin: 8px 0 15px 0; font-size: 1.2rem; color: var(--accent); font-weight: 600;">{exp["company"]}</h4>
                
                <div style="display: inline-flex; align-items: center; font-size: 0.9rem; font-weight: 600; color: var(--text-muted); background: rgba(49, 130, 206, 0.06); padding: 6px 14px; border-radius: 8px; border: 1px solid rgba(49, 130, 206, 0.15);">
                    <i class="fa-regular fa-calendar" style="margin-right: 8px; color: var(--accent);"></i> {exp["duration"]}
                </div>
            </div>
            
            {brand_graphic_html}
        </div>
        
        <div style="margin: 0; padding-left: 5px; position: relative; z-index: 2;">
            <ul style="margin: 0; padding: 0; list-style: none; color: var(--text-muted); font-size: 1.1rem; line-height: 1.8;">
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