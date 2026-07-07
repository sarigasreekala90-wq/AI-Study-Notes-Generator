#  AI Study Notes Generator

An AI-powered web application that generates beginner-friendly study notes using a local Large Language Model (LLM). Built with Flask, SQLite, and Ollama, the application allows users to generate, save, search, and manage study notes through a simple web interface.

---

##  Features

* Secure Password Hashing
*  AI-Powered Study Notes Generation
*  Save Generated Notes
*  Search Previous Notes
*  Delete Notes
*  SQLite Database
*  Clean and Responsive User Interface

---

##  Technologies Used

### Backend

* Python
* Flask
* SQLite

### AI

* Ollama
* Gemma 3 1B

### Frontend

* HTML
* CSS
* JavaScript

### Tools

* Git
* GitHub
* VS Code

---

##  Project Structure

```text
AI-Study-Notes-Generator/
│
├── app.py
├── database.db
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
```

---

##  Installation

### Clone the repository

```bash
git https://github.com/sarigasreekala90-wq/AI-Study-Notes-Generator.git
```

### Go to the project folder

```bash
cd AI-Study-Notes-Generator
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Install Ollama

Download and install Ollama from the official website.

### Download the AI model

```bash
ollama pull gemma3:1b
```

### Run the application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

##  Future Improvements

* Export notes as PDF
* AI Chatbot
* Flashcard Generator
* Quiz Generator
* Dark Mode
* Voice Input
* Study Progress Tracker

---

##  Author

**Sariga**

Engineering Student | Python & AI Enthusiast
