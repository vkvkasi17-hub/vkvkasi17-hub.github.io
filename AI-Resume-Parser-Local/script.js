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
        fileNameDisplay.style.color = 'var(--text-primary)';
        submitBtn.disabled = false;
        resultsPanel.style.display = 'none'; 
    }
});

submitBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if(!file) return;

    btnText.textContent = "Processing...";
    spinner.style.display = "block";
    submitBtn.disabled = true;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch('http://127.0.0.1:8000/parse-resume/', { 
            method: 'POST', 
            body: formData 
        });
        
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
                    <div class="card scroll-animate">
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
                for (const [sectionName, sectionContent] of Object.entries(otherSections)) {
                    let html = `
                    <div class="section-divider scroll-animate">
                        <span>${sectionName}</span>
                    </div>
                    <div class="card scroll-animate">
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
        alert("Failed to connect to server. Ensure main.py is running on port 8000.");
        console.error(error);
    }

    btnText.textContent = "Parse Document";
    spinner.style.display = "none";
    submitBtn.disabled = false;
});