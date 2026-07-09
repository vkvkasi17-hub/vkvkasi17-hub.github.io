import json
import os

print("Starting build process...")

# 1. LOAD DATA
with open('portfolio_data.json', 'r') as file:
    portfolio_data = json.load(file)

# 2. GENERATE DYNAMIC HTML CHUNKS
education_html = "" 
for edu in portfolio_data['education']:
    education_html += f'<div class="card right"><h3 style="color: var(--accent);">{edu["degree"]}</h3><h4>{edu["school"]}</h4><div class="duration">{edu["duration"]}</div></div>'

skills_html = "<div class='skills-grid'>"
for cat, items in portfolio_data['skills'].items():
    skill_tags = "".join([f"<span class='tag skill-tag'>{i}</span>" for i in items])
    skills_html += f"<div class='card bottom'><h3>{cat}</h3><div class='tag-container'>{skill_tags}</div></div>"
skills_html += "</div>"

# --- THE ALL-NEW VERTICAL TIMELINE DESIGN ---
experience_html = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

.new-timeline-container { position: relative; margin: 40px 0 40px 20px; padding-left: 40px; font-family: 'Outfit', sans-serif; }
.new-timeline-container::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: linear-gradient(to bottom, var(--accent), transparent); border-radius: 4px; }
.timeline-item { position: relative; margin-bottom: 40px; }
.timeline-dot { position: absolute; left: -50px; top: 0; width: 24px; height: 24px; background: var(--bg); border: 4px solid var(--accent); border-radius: 50%; box-shadow: 0 0 15px var(--accent); z-index: 2; }
.timeline-content { background: var(--card-bg); border: 1px solid var(--border); border-radius: 16px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); transition: transform 0.3s ease, border-color 0.3s ease; }
.timeline-content:hover { transform: translateY(-5px); border-color: var(--accent); }
.timeline-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px; border-bottom: 1px solid var(--border); padding-bottom: 15px; margin-bottom: 15px; }
.timeline-role { font-size: 1.6rem; font-weight: 800; margin: 0; color: var(--text-main); }
.timeline-company { font-size: 1.2rem; font-weight: 600; margin: 5px 0 0 0; }
.timeline-date { font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; background: rgba(100, 100, 100, 0.1); padding: 6px 12px; border-radius: 6px; color: var(--text-muted); border: 1px dashed var(--border); }
.timeline-bullets { list-style-type: none; padding: 0; margin: 0; }
.timeline-bullets li { position: relative; padding-left: 20px; margin-bottom: 12px; color: var(--text-muted); line-height: 1.6; font-size: 1.05rem; }
.timeline-bullets li::before { content: '▹'; position: absolute; left: 0; color: var(--accent); font-weight: bold; font-size: 1.2rem; }
</style>
<div class="new-timeline-container">
"""

for exp in portfolio_data['experience']:
    bullets = "".join([f"<li>{b}</li>" for b in exp['bullets']])
    color = exp.get("color", "var(--accent)")
    
    experience_html += f"""
    <div class="timeline-item">
        <div class="timeline-dot" style="border-color: {color}; box-shadow: 0 0 12px {color};"></div>
        <div class="timeline-content">
            <div class="timeline-header">
                <div>
                    <h3 class="timeline-role">{exp["role"]}</h3>
                    <h4 class="timeline-company" style="color: {color};">{exp["company"]}</h4>
                </div>
                <div class="timeline-date">{exp["duration"]}</div>
            </div>
            <ul class="timeline-bullets">
                {bullets}
            </ul>
        </div>
    </div>
    """
experience_html += "</div>"

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

    projects_html += f'<div class="card new-project-card modal-trigger" style="cursor: pointer;" data-category="{cat}" data-title="{proj["title"]}" data-tech="{proj["tech"]}" data-overview="{overview}" data-github="{github}" data-website="{website}">'
    projects_html += f'<div class="card-top-bar"><div class="icon-box"><i class="fa-solid {icon}"></i></div><div class="link-icons">{github_html}{website_html}</div></div>'
    projects_html += f'<div class="card-content"><span class="category-badge-text">{cat}</span><h3>{proj["title"]}</h3><p>{proj["description"]}</p></div></div>'
    
certifications_html = '<div class="cert-grid">'
if 'certifications' in portfolio_data:
    for cert in portfolio_data['certifications']:
        certifications_html += f'<div class="card cert-card cert-item" data-img="{cert.get("image", "")}"><i class="fa-solid fa-award cert-icon"></i><div><h4 style="margin:0;">{cert["name"]}</h4><p style="margin:0; font-size:0.9rem; color:var(--text-muted);">{cert["issuer"]}</p></div></div>'
certifications_html += '</div>'

publications_html = ""
for pub in portfolio_data['publications']:
    publications_html += f'<div class="card right"><a href="{pub["link"]}" target="_blank" style="text-decoration: none;"><h3 class="pub-title" style="color: var(--accent); cursor: pointer;">{pub["title"]} ↗</h3></a><div class="tech">{pub["journal"]} ({pub["year"]})</div><p style="font-size: 0.95rem; color: var(--text-muted);">{pub["authors"]}</p></div>'

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