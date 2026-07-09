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

# --- NEW EXPERIENCE BLOCK LAYOUT ---
# This injects the new shapes and right-aligned flexbox directly into the HTML
experience_html = """
<style>
    .exp-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 16px; /* New rounded block shape */
        padding: 30px 30px 30px 40px;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .exp-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.1);
    }
    .exp-header {
        display: flex;
        justify-content: space-between; /* Pushes the date to the right */
        align-items: flex-start;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 20px;
        border-bottom: 1px solid var(--border);
        padding-bottom: 20px;
    }
    .exp-title {
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0 0 5px 0;
        letter-spacing: -0.5px;
        font-family: 'Inter', sans-serif;
    }
    .exp-company {
        font-size: 1.15rem;
        font-weight: 600;
        margin: 0;
        color: var(--text-main);
    }
    .exp-date {
        font-family: 'Fira Code', monospace; /* Tech font for dates */
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text-muted);
        background: var(--bg);
        padding: 8px 16px;
        border-radius: 20px; /* Pill shape */
        border: 1px solid var(--border);
        display: flex;
        align-items: center;
        white-space: nowrap;
        height: fit-content;
    }
    .exp-bullets {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .exp-bullets li {
        position: relative;
        padding-left: 25px;
        margin-bottom: 12px;
        color: var(--text-muted);
        font-size: 1.05rem;
        line-height: 1.7;
    }
    .exp-bullets li::before {
        content: '▹';
        position: absolute;
        left: 0;
        top: 0;
        font-weight: bold;
        font-size: 1.2rem;
    }
</style>
"""

for exp in portfolio_data['experience']:
    bullets = "".join([f"<li>{b}</li>" for b in exp['bullets']])
    color = exp.get("color", "var(--accent)")
    
    experience_html += f"""
    <div class="exp-card">
        <div style="position: absolute; top: 0; left: 0; width: 6px; height: 100%; background: {color};"></div>
        
        <div class="exp-header">
            <div>
                <h3 class="exp-title" style="color: {color};">{exp["role"]}</h3>
                <h4 class="exp-company">{exp["company"]}</h4>
            </div>
            <div class="exp-date">{exp["duration"]}</div>
        </div>
        <ul class="exp-bullets">
            {bullets}
        </ul>
    </div>
    """

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