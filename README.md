# Smart Email Generator

An AI-powered email generation platform built using LLMs, Prompt Engineering, LangChain, FastAPI, and React. The system helps users generate professional, context-aware emails with customizable tones and styles including corporate, friendly, sales, and technical communication.

---

## Features

### Core Features
- Professional email generation
- Few-shot prompt engineering
- Prompt template system
- Auto subject generation
- AI-powered reply generation

### Tone & Style Support
- Professional
- Friendly
- Formal
- Casual
- Persuasive
- Corporate
- Sales
- Technical

### Frontend & Backend
- React + Vite frontend
- FastAPI backend
- REST API integration
- Interactive UI
- Copy-to-clipboard support

---

## Tech Stack

### Frontend
- React
- Vite
- Tailwind CSS

### Backend
- FastAPI
- Python
- LangChain

### AI / LLM
- Gemini API
- Prompt Engineering
- Few-shot Prompting

---

## Project Structure

```bash
smart-email-generator/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   └── services/
│
├── frontend/
│   ├── src/
│   ├── components/
│   └── pages/
│
├── prompts/
│   ├── email_prompt.py
│   ├── fewshot_examples.py
│   └── styles/
│
├── tests/
├── requirements.txt
└── README.md
````

---

## User Stories Implemented

| User Story | Description                  | Status    |
| ---------- | ---------------------------- | --------- |
| US-01      | Project Setup                | Completed |
| US-02      | Prompt Templates             | Completed |
| US-03      | Few-Shot Prompting           | Completed |
| US-04      | Professional Email Generator | Completed |
| US-05      | Tone Selection               | Completed |
| US-06      | Auto Subject Generation      | Completed |
| US-07      | Reply Generation             | Completed |
| US-08      | Corporate Style Emails       | Completed |
| US-09      | Friendly Style Emails        | Completed |
| US-10      | Sales Style Emails           | Completed |
| US-11      | Technical Style Emails       | Completed |
| US-12      | Frontend UI                  | Completed |
| US-13      | API Integration              | Completed |
| US-14      | Testing & Validation         | Completed |
| US-15      | Deployment Preparation       | Completed |

---

## Installation

### Clone Repository

```bash
git clone https://github.com/SrinidhiPRao/smart-email-generator.git
cd smart-email-generator
```

---

## Backend Setup

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / MacOS

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```bash
http://localhost:5173
```

---

## API Endpoints

### Generate Email

```http
POST /generate-email
```

Request Body:

```json
{
  "prompt": "Write a leave request email",
  "tone": "professional"
}
```

---

### Generate Subject

```http
POST /generate-subject
```

---

### Generate Reply

```http
POST /generate-reply
```

---

## Example Use Cases

### Business Communication

Generate:

* Client emails
* HR emails
* Meeting requests
* Follow-ups

### Customer Support

Generate:

* Support responses
* Apology emails
* Resolution emails

### Sales Outreach

Generate:

* Product promotion emails
* Lead outreach
* Follow-up campaigns

### Technical Communication

Generate:

* Bug reporting emails
* Technical updates
* Engineering communication

---

## Problems Solved

* Reduces manual email drafting time
* Improves professional communication
* Maintains tone consistency
* Simplifies business communication workflows
* Automates repetitive email writing tasks

---

## Challenges Faced

* Prompt consistency issues
* Tone control refinement
* Few-shot optimization
* LLM formatting cleanup
* Frontend-backend synchronization
* API integration debugging

---

## Future Scope

* Gmail integration
* Outlook integration
* Multi-language support
* Voice-to-email generation
* Email analytics dashboard
* User authentication
* Conversation memory
* Fine-tuned custom models
* Browser extension support
* Cloud deployment on Azure

---

## Deployment

Deployed on Azure

---

## Contributors

| Name          | Role                        |
| ------------- | --------------------------- |
| Srinidhi Rao  | Prompt Engineering, Backend |
| Aditya Sharma | Subject & Style Features    |
| Mehul Agarwal | Frontend, API, Deployment   |

---

## License

This project is developed for educational and research purposes.

---

## Repository

GitHub Repository:

[https://github.com/SrinidhiPRao/smart-email-generator](https://github.com/SrinidhiPRao/smart-email-generator)
