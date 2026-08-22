# 🍫 Choco Crunch Analytics

### End-to-End Chocolate Product Analytics using Python, PostgreSQL, SQL & Streamlit

Choco Crunch Analytics is an end-to-end data analytics project built to collect, clean, transform, store, analyze, and visualize real-world chocolate product data.

The project uses the **Open Food Facts API** as the data source, **Python and Pandas** for data processing, **PostgreSQL** for relational data storage, **SQL** for business analysis, and **Streamlit** for an interactive analytics dashboard.

The project answers **27 business-oriented SQL questions** and presents the results through interactive tables and EDA visualizations.

---

## 🚀 Project Highlights

- 🌐 Collected approximately **12,000 chocolate product records**
- 🐍 Built the data pipeline using **Python & Pandas**
- 🧹 Performed data exploration and cleaning
- 🔧 Created nutritional and product-level features
- 🗄️ Designed a relational **PostgreSQL database**
- 🔗 Created relationships using primary and foreign keys
- 🧮 Developed **27 SQL business queries**
- 📊 Built an interactive **Streamlit dashboard**
- 📈 Presented SQL results using interactive tables
- 📉 Created EDA visualizations for nutritional and product analysis
- 🔄 Built a complete **API → Database → Analytics → Dashboard** workflow

---

# 📌 Project Overview

Chocolate products contain a wide range of nutritional and product characteristics.

This project analyzes chocolate products based on:

- Brand
- Product name
- Calories
- Carbohydrates
- Sugar
- Fat
- Saturated fat
- Protein
- Fiber
- Salt
- Sodium
- Nutrition score
- NOVA processing group
- Fruits, vegetables and nuts content

The goal is to transform raw API data into a structured analytical system that can answer real-world business questions.

---

# 🔄 End-to-End Architecture

```text
                ┌────────────────────────┐
                │   Open Food Facts API  │
                └────────────┬───────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │    Data Collection     │
                │      Python            │
                └────────────┬───────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │ Data Exploration &     │
                │      Cleaning          │
                │   Pandas / NumPy       │
                └────────────┬───────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │ Feature Engineering    │
                │        Python          │
                └────────────┬───────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │      PostgreSQL        │
                │    Relational DB       │
                └────────────┬───────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │   27 SQL Queries       │
                │ Business Analysis      │
                └────────────┬───────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │   Streamlit Dashboard  │
                └────────────┬───────────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
        ┌─────────────────┐     ┌─────────────────┐
        │ Interactive     │     │ EDA             │
        │ Tables          │     │ Visualizations  │
        └─────────────────┘     └─────────────────┘