# ⚡ High-Frequency E-Commerce Tracker (ETL Pipeline)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge\&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge\&logo=playwright\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge\&logo=postgresql\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge\&logo=pandas\&logoColor=white)

An end-to-end ETL solution designed to collect, process, store, and visualize real-time pricing data from e-commerce platforms.

The project combines browser automation, data transformation, relational database storage, and interactive dashboards to provide actionable market insights.

---

## 🎯 Project Overview

Monitoring competitor prices and market trends is a critical task in modern e-commerce.

Traditional scraping approaches based solely on HTTP requests often struggle with dynamic websites, lazy-loaded content, and anti-bot protections. This project addresses these challenges using browser automation with Playwright, enabling reliable extraction of real-world pricing data.

The pipeline follows a complete ETL architecture:

* **Extract:** Automated data collection from dynamic web pages.
* **Transform:** Data cleaning, normalization, and price conversion.
* **Load:** Persistent storage in PostgreSQL and visualization through Streamlit.

---

## 🏗️ Architecture

### 1. Extract

The extraction layer uses **Playwright (Async API)** to:

* Navigate dynamic websites.
* Handle infinite scrolling and lazy-loaded content.
* Wait for JavaScript-rendered elements.
* Simulate realistic browser behavior.

### 2. Transform

The transformation layer uses **Pandas** to:

* Clean extracted data.
* Normalize product information.
* Convert price strings into numeric values.
* Prepare datasets for analysis and storage.

### 3. Load

The processed data is stored and visualized through:

#### PostgreSQL

* Automatic database initialization.
* Automatic table creation.
* Historical price tracking.
* Structured relational storage.

#### Streamlit Dashboard

Interactive dashboard providing:

* Lowest price available.
* Average market price.
* Product listings.
* Real-time data refresh.

---

## 🚀 Technologies Used

* Python 3.10+
* Playwright
* Pandas
* PostgreSQL
* Psycopg2
* Streamlit
* Asyncio

---

## 📦 Installation

### Prerequisites

* Python 3.10+
* Microsoft Edge or Chromium-based browser
* PostgreSQL running locally

### Clone the Repository

```bash
git clone https://github.com/WaynerMoraes12/ecommerce-tracker-etl.git

cd ecommerce-tracker-etl
```

### Create a Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright Browsers

```bash
playwright install
```

### Configure Database Credentials

Update the PostgreSQL connection settings in `dashboard.py`:

```python
DB_NAME = "ecommerce_db"
DB_USER = "postgres"
DB_PASS = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
```

### Run the Application

```bash
streamlit run dashboard.py
```

---

## 📊 Database Schema

| Column      | Type      | Description          |
| ----------- | --------- | -------------------- |
| id          | SERIAL    | Unique identifier    |
| equipamento | TEXT      | Product name         |
| preco       | NUMERIC   | Product price        |
| url         | TEXT      | Product URL          |
| data_coleta | TIMESTAMP | Collection timestamp |

---

## 🛠️ Resilience Features

The scraper was designed to handle common challenges found in modern e-commerce websites:

* Dynamic content rendering.
* Lazy loading.
* Infinite scrolling.
* Temporary anti-bot challenges.
* Retry and wait strategies during extraction.

---

## 📈 Future Improvements

* Docker containerization.
* Scheduled ETL execution.
* Price variation alerts.
* Historical trend analysis.
* REST API integration.
* Cloud deployment.

---

## 👨‍💻 Author

**Wayner Moraes**

QA Engineer | Automation Engineer | Python Developer

GitHub: https://github.com/WaynerMoraes12
