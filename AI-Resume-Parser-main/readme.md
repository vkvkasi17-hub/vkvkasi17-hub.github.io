# 🚀 AI Resume Parser

An intelligent, high-precision ATS resume parsing engine built with Python and FastAPI, featuring a modern, interactive frontend.

## ✨ Features
* **Smart Extraction:** Automatically identifies and extracts Emails, Phone Numbers, and Professional Summaries.
* **Skill Classification:** Scans for over 60+ technical skills (Python, AWS, React, etc.) and tags them visually.
* **Work Experience Parsing:** Uses date-anchored regex to separate job titles, companies, dates, and bulleted responsibilities.
* **Text Corruption Patching:** Automatically fixes common PDF extraction errors (e.g., fixing broken ligatures).
* **Interactive UI:** A highly responsive, glassmorphism-inspired web interface with hover animations and clean data visualization.

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Uvicorn, Regex, `pdfplumber`, `python-docx`
* **Frontend:** HTML5, CSS3 (Custom animations/gradients), Vanilla JavaScript
* **Architecture:** RESTful API with CORS middleware

## 🚀 How to Run Locally

**1. Start the Backend Server**
Ensure you have the required Python libraries installed, then run the FastAPI server:
```bash
uvicorn main:app --reload