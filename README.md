# Silvernova Assessment Task

Thank you for applying for a job at **silvernova**. We are excited to talk to you about working together.

We at silvernova think that creativity and new solutions when developing are hindered by a time constraint. Coding interviews can thus misrepresent your true skills. This is why we are using an asynchronous asseesment task concept. This task will help us understand how you go about solving problems without having to breathe down your neck. 😉

When working on this task either
  * fork this repo and submit a link to your submission via mail
  * clone the repo and send a zipped version via mail

## Your info (please fill out)

Try to answer as thruthfully as possible.

| Name                     | Arpit Kuamr Pandey          |
|--------------------------|-----------------------------|
| E-Mail:                  | arpitpandey351999@gamil.com |
| Approx. Time To Complete | 40 hours                    |
| My github:               | https://github.com/arpit35  |

## The task

Your task is to build a very simple [RAG](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) that is able to answer questions on the provided demo documents. The documents represent what a lawyer will be working with on a day-to-day basis - although some will be harder to parse than others.

> The final application should provide an interface to talk to the assistant about the documents, ask questions, and retreive facts. For a lawyer's  job it's important that every piece of information they work with should be backed by sources, so every answer should be as specific as possible, pointing not only to the source document, but ideally to the sentence or paragraph where the information is located.

This repository already has a basic structure to help you get started and point you in the right direction. Your tasks are to:

- [ ] Familiarize yourself with the codebase and the parts that need changes 
- [ ] Complete the **extraction script** to embed the information from the documents in markdown format
- [ ] Complete the **embedding script** to embed the documents' information for later retreival
- [ ] Complete the **search script** to retreive the embedded documents that most closely resemble the search query
- [ ] Complete the **ask script** to ask questions about the documents
- [ ] Complete the **tests** and make sure they run

## Setup

```bash
pip install -r requirements.txt
```

## API

We've provided an API access for you that allows you to embed text and prompt an LLM. The API is running at [https://assessment.silvrnova.ai](https://assessment.silvrnova.ai). 

You can find the OpenAPI specification here: [OpenAPI Specification](https://assessment.silvernova.ai/swagger).

You have to authenticate at the API. Use your assigned **API Key** for that purpose. Put it into a `.env` file located in the root of the project.

---

## 🚀 Setup & Usage Guide

### **📦 Prerequisites**

Ensure you have the following installed on your system:

- Docker

- Docker Compose

### **1️⃣ Build the Docker Image**
Navigate to the project directory and build the Docker image using:

```bash
docker-compose up -d
```

### **2️⃣ Access the Running Container**
Once the container is up, you can access it via an interactive shell:

```bash
docker-compose exec app /bin/bash
```


### **🛠 Running the Application**
After entering the container, you can run the associate script in different modes:

```bash
# Get the file's content as markdown
./associate --mode=get-markdown

# Index the documents
./associate --mode=index-files

# Search for documents based on similarity
./associate --mode=search "[question]"

# Ask a question about the documents
./associate "[question]"
```

### **🧪 Running Tests**
You can run the test cases using pytest as follows:

**Run tests from your host machine:**

```bash
docker-compose exec app pytest
```

**Run tests from inside the Docker container:**
```bash
pytest
```
