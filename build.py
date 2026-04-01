import json
import os

print("Starting build process...")

# 1. LOAD DATA
with open('Portfolio/portfolio_data.json', 'r') as file:
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

experience_html = ""
for exp in portfolio_data['experience']:
    bullets = "".join([f"<li>{b}</li>" for b in exp['bullets']])
    experience_html += f'<div class="card left" style="border-left: 5px solid {exp["color"]};"><h3 style="color: {exp["color"]};">{exp["role"]}</h3><h4>{exp["company"]}</h4><div class="duration">{exp["duration"]}</div><ul>{bullets}</ul></div>'

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
    projects_html += f'<div class="card-top-bar">'
    projects_html += f'<div class="icon-box"><i class="fa-solid {icon}"></i></div>'
    projects_html += f'<div class="link-icons">{github_html}{website_html}</div>'
    projects_html += f'</div>'
    projects_html += f'<div class="card-content">'
    projects_html += f'<span class="category-badge-text">{cat}</span>'
    projects_html += f'<h3>{proj["title"]}</h3>'
    projects_html += f'<p>{proj["description"]}</p>'
    projects_html += f'</div></div>'
    
# --- NEW: Beautiful Certification Cards ---
certifications_html = '<div class="cert-grid">'
if 'certifications' in portfolio_data:
    for cert in portfolio_data['certifications']:
        certifications_html += f'<div class="card cert-card cert-item" data-img="{cert.get("image", "")}">'
        certifications_html += f'<i class="fa-solid fa-award cert-icon"></i>'
        certifications_html += f'<div><h4 style="margin:0;">{cert["name"]}</h4><p style="margin:0; font-size:0.9rem; color:var(--text-muted);">{cert["issuer"]}</p></div>'
        certifications_html += f'</div>'
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
