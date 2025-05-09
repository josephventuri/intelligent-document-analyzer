# 📘 Intelligent Document Analyzer – AWS AI Project

This project uses AWS AI and ML services to automate the process of extracting text, analyzing sentiment, and generating human-like summaries from physical or digital documents. It’s ideal for converting content from books, post-it notes, ID cards, or product reviews into structured insights using Textract, Comprehend, and Bedrock.

## 🚀 Features

- 📄 **Extract Text** from document images (OCR with Textract)
- 🧠 **Understand Meaning** with NLP (Comprehend for sentiment and key phrases)
- 🤖 **Summarize Content** using Claude 3 via Bedrock (Generative AI)
- 🧪 **Run in SageMaker** with full code in Jupyter Notebook
- 🔐 IAM roles and Boto3 for secure, programmatic access

---

## 🛠️ Tech Stack

| Service         | Purpose                                                           |
|-----------------|-------------------------------------------------------------------|
| **Textract**     | OCR - Extracts text from images                                  |
| **Comprehend**   | NLP - Finds sentiment, key phrases, and named entities          |
| **Bedrock**      | Accesses Claude 3 Haiku for image+text summarization            |
| **Claude 3 Haiku**| LLM for summarizing visual and textual content                  |
| **SageMaker**    | Jupyter environment to run and test code                         |
| **IAM Roles**    | Secures notebook access to AWS services                          |
| **Boto3 (Python)**| Interacts with AWS services in code                             |

---

## 📷 Example Use Cases

- 🏥 Healthcare – Extract info from ID cards or forms  
- 💼 Finance – Summarize contracts or legal docs  
- 🛒 E-commerce – Analyze customer reviews at scale  
- 📚 Education – Convert handwritten notes to summaries  

---

## 🏗️ How to Build This

### Step 1 – Set Up Notebook  
- Open SageMaker → Create `ml.t3.medium` instance  
- Assign IAM Role (no S3 needed)  
- Wait for `InService`, then open JupyterLab  

### Step 2 – Attach Policies  
- Go to IAM → Find the SageMaker role  
- Attach: `AmazonTextractFullAccess`, `ComprehendFullAccess`, `BedrockFullAccess`  

### Step 3 – Extract Text with Textract  
- Upload `.jpg` or `.png` to SageMaker  
- Use Boto3 to call `detect_document_text()`  
- Save the output as `.txt`

### Step 4 – Analyze with Comprehend  
- Analyze top 5 key phrases  
- Detect sentiment  
- Save output as `_summary.txt`

### Step 5 – Generate Summary with Claude 3  
- Base64-encode the image  
- Prompt Claude: `"Explain the content of this image"`  
- Use Boto3 to call Bedrock and return the summary  

---

## ✅ Results

| Layer       | Output Type                             |
|-------------|------------------------------------------|
| Textract    | Raw text from the image (OCR)           |
| Comprehend  | Keywords + Sentiment                    |
| Claude 3    | Summary + Insight beyond basic text     |

---

## 🎥 Video Walkthrough

▶️ [Watch the whiteboard video](https://josephventuri.io/document_analyzer.mp4)



