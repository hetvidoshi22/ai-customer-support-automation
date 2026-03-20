# 🚀 AI Customer Support Automation & Intelligence System

An AI-powered system designed to automate customer support by classifying queries, analyzing issue trends, and generating intelligent responses to reduce manual workload.

---

## 🎯 Objective

To build a scalable AI workflow that:

- Automatically analyzes incoming customer queries  
- Classifies them into predefined categories  
- Calculates percentage distribution of issues  
- Visualizes insights in a dashboard  
- Automates responses and reduces support workload  

---

## 🧠 Key Features

### 🤖 AI Query Classification

- Uses **Google Gemini LLM** for natural language understanding  
- Handles real-world queries (including noisy and Hinglish text)  
- Hybrid approach:
  - LLM-based classification  
  - Rule-based fallback for improved reliability  

---

### 📊 Analytics Dashboard

- Displays:
  - % distribution of issues (Pie Chart)  
  - Most common customer problem  
  - Total queries and category count  
- Built using **Chart.js + JavaScript**

---

### 📈 Trend Analysis

- Shows **daily trends of customer queries**  
- Helps identify recurring problems over time  
- Enables data-driven decision-making  

---

### 💬 Automated Response System

- Automatically generates responses based on detected issue  

**Examples:**
- Delivery Delay → “Your order is on the way...”  
- Refund Request → “Your refund is being processed...”  
- Payment Failure → “Try another payment method...”  

---

### ⚙️ Automation Engine

The system not only classifies queries but also **takes automated actions**:

| Category | Automation Action |
|----------|-----------------|
| Order Tracking | Sends tracking link |
| Delivery Delay | Sends delay update |
| Refund Request | Triggers refund workflow |
| Product Issue | Creates support ticket |
| Payment Failure | Suggests retry |
| Subscription Issue | Provides self-service link |
| General Query | Routes to FAQ bot |
| Ambiguous | Requests clarification |

---

### ⚠️ Escalation Mechanism

- Automatically escalates:
  - Ambiguous queries  
  - Low-confidence predictions  
- Ensures critical issues are handled by human agents  

---

## 🧩 Problem Categories

The system classifies queries into:

- Order Tracking  
- Delivery Delay  
- Refund Request  
- Product Issue  
- Payment Failure  
- Subscription Issue  
- General Query  
- Ambiguous  

---

## 🛠️ Tech Stack

| Component       | Technology            |
|----------------|----------------------|
| Backend         | Python, Flask         |
| AI Model        | Google Gemini API     |
| Data Processing | Pandas                |
| Frontend        | HTML, CSS, JavaScript |
| Visualization   | Chart.js              |
| Environment     | Python-dotenv         |

---

## 🧠 AI Categorization Logic

### 1. LLM-Based Classification
- Uses Gemini API to understand intent and context  

### 2. Rule-Based Fallback
- Handles edge cases:
  - Short queries  
  - Typos / noisy input  
  - Ambiguous text  
- Ensures robustness and consistency  

---

## 📊 Sample Output

### Input:

```
My order is late
```


### Output:
- Category: Delivery Delay  
- Confidence: 90%  
- Auto Response: “Your order is on the way...”  
- Automation: Delay update sent  
- Escalation: Fully Automated  

---

## 🔄 Workflow Architecture

```
User Query (WhatsApp / Instagram / Email/ Website)
        ↓
Frontend UI Input 
        ↓
Flask Backend API
        ↓
Gemini AI Classification
        ↓
Category Detection
        ↓
Automation Engine (Response + Action + Escalation)
        ↓
Data Processing (Pandas)
        ↓
Analytics Dashboard (Charts + Trends)
```

---

## 📈 Scalability

The system is designed to handle high query volumes using:

* API-based architecture
* Horizontal scaling with microservices
* Queue systems (Kafka / RabbitMQ)
* Batch processing for analytics
* Cloud deployment (AWS / GCP / Azure)

---

## 🚀 How to Run

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Add API Key

Create `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

### 3. Run Backend

```bash
python -m backend.app
```

### 4. Run Frontend

Open:

```
frontend/index.html
```

---

## 📂 Project Structure

```
ai-customer-support-automation/
│
├── backend/
│   ├── app.py
│   ├── data_processor.py
│   ├── gemini_classifier.py
│
├── data/
│   └── customer_support_dataset.csv
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── styles.css
│
├── .env
├── requirements.txt
└── README.md
```

---

## 💡 Business Impact

This system helps companies:

* Reduce manual support workload
* Improve response time
* Identify top customer issues
* Automate repetitive queries
* Enhance customer satisfaction

---

## 🔮 Future Improvements

* Chatbot UI integration
* Real-time API integration with platforms (WhatsApp, Instagram)
* Deployment on cloud platforms
* Advanced ML model fine-tuning
* User feedback loop for continuous learning
