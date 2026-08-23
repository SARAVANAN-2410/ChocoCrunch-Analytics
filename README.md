# 🍫 ChocoCrunch Analytics

An end-to-end **food product analytics project** built using **Python, PostgreSQL, SQL, Pandas, and Streamlit**.

The project transforms food product data into a structured PostgreSQL database, performs data cleaning and feature engineering, answers **27 analytical SQL questions**, and presents the results through an interactive Streamlit dashboard with EDA visualizations.

---

## 📊 Dashboard Preview

![ChocoCrunch Analytics Dashboard](screenshots/join-queries-brands.png)

## 🔗 SQL Join Query Results

![Top 5 Products by Sugar-to-Carb Ratio](screenshots/join-queries-ratio.png)

![Top 5 Brands by High Calorie Products](screenshots/dashboard.png)

---

## 🎯 Project Objectives

The main objectives of this project are to:

- Clean and prepare food product data for analysis.
- Design and populate a relational PostgreSQL database.
- Separate product, nutrient, and derived analytical information into structured tables.
- Perform feature engineering for calorie, sugar, and food-processing analysis.
- Solve 27 business-oriented SQL questions.
- Use SQL JOINs to combine information across multiple tables.
- Build an interactive Streamlit dashboard.
- Perform exploratory data analysis (EDA) using statistical summaries and visualizations.
- Demonstrate an end-to-end data analytics workflow.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and application development |
| Pandas | Data cleaning and data manipulation |
| NumPy | Numerical operations and feature engineering |
| PostgreSQL | Relational database and SQL analysis |
| SQL | Data querying and analytical calculations |
| Streamlit | Interactive dashboard |
| Matplotlib | EDA visualizations |
| python-dotenv | Secure environment variable management |
| Jupyter Notebook | Data preparation and SQL development |

---

## 🗄️ Database Design

The project uses PostgreSQL with three main tables:

### `product_info`

Contains product-level information such as:

- `product_code`
- `product_name`
- `brand`

### `nutrient_info`

Contains nutritional information such as:

- `energy_kcal_value`
- `sugars_value`
- `carbohydrates_value`
- `fat_value`
- `sodium_value`
- `nova_group`
- fruits/vegetables/nuts content

### `derived_metrics`

Contains engineered analytical features such as:

- `calorie_category`
- `sugar_category`
- `sugar_to_carb_ratio`
- `is_ultra_processed`

### Relationship

The tables are connected using:

```text
product_info
     │
     │ product_code
     ▼
nutrient_info
     │
     │ product_code
     ▼
derived_metrics
```

This structure allows the project to demonstrate both **single-table SQL analysis and multi-table JOIN operations**.

---

## 🧹 Data Preparation

The data preparation workflow includes:

1. Loading the source dataset.
2. Cleaning product information.
3. Handling missing product and brand values.
4. Standardizing missing product/brand values as `Missing`.
5. Preparing nutritional attributes.
6. Creating derived analytical metrics.
7. Loading the cleaned data into PostgreSQL.
8. Validating the database tables before analysis.

---

## 🧮 Feature Engineering

Several features were created to support analytical questions.

### Calorie Category

Products are classified into calorie categories based on their energy content.

### Sugar Category

Products are categorized according to their sugar content.

### Sugar-to-Carbohydrate Ratio

```text
sugar_to_carb_ratio =
sugars_value / carbohydrates_value
```

The ratio helps identify products where sugar represents a large proportion of their carbohydrate content.

### Ultra-Processed Classification

Products are categorized according to their food-processing classification.

---

# 📑 SQL Analysis

The project contains **27 SQL analytical questions** divided into four sections.

## `product_info` Queries

1. Count products per brand
2. Count unique products per brand
3. Find the top 5 brands by product count
4. Find products with missing product names
5. Count the number of unique brands
6. Find products with product codes starting with `3`

## `nutrient_info` Queries

7. Find the top 10 products with the highest energy value
8. Calculate average sugar value per NOVA group
9. Count products with fat greater than 20g
10. Calculate average carbohydrate value
11. Find products with sodium greater than 1g
12. Count products with non-zero fruits/vegetables/nuts content
13. Find products with energy greater than 500 kcal

## `derived_metrics` Queries

14. Count products per calorie category
15. Count High Sugar products
16. Calculate average sugar-to-carbohydrate ratio for High Calorie products
17. Find products that are both High Calorie and High Sugar
18. Count ultra-processed products
19. Find products with a sugar-to-carbohydrate ratio greater than 0.7
20. Calculate average sugar-to-carbohydrate ratio per calorie category

## JOIN Queries

21. Find the top 5 brands with the most High Calorie products
22. Calculate average energy value for each calorie category
23. Count ultra-processed products per brand
24. Find High Sugar and High Calorie products along with their brands
25. Calculate average sugar content per brand for ultra-processed products
26. Count fruits/vegetables/nuts products in each calorie category
27. Find the top 5 products by sugar-to-carbohydrate ratio with calorie and sugar categories

---

# 📊 Exploratory Data Analysis

The Streamlit dashboard includes EDA for:

### Dataset Overview

- Total number of products
- Number of features
- Unique brands
- Average calorie value

### Variable Distributions

- Energy (`energy_kcal_value`)
- Sugar (`sugars_value`)
- Carbohydrates (`carbohydrates_value`)
- Sugar-to-carbohydrate ratio

### Category Analysis

- Calorie categories
- Sugar categories
- NOVA groups

### Food Processing Analysis

- Ultra-processed products
- Other products

### Relationship Analysis

- Calories vs Sugar
- Energy vs NOVA Group

The dashboard also handles invalid infinite ratio values during visualization so that EDA remains robust.

---

# 🖥️ Streamlit Dashboard

The Streamlit application provides:

- Interactive SQL query selection
- SQL result tables
- Product-level analysis
- Brand-level analysis
- JOIN query results
- EDA visualizations
- Database-backed analysis

The application connects directly to PostgreSQL rather than relying only on static CSV files.

---

# 🔐 Environment Variables

Database credentials are stored locally using a `.env` file and are **not committed to GitHub**.

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=CHOCO_CRUNCH
DB_USER=postgres
DB_PASSWORD=your_password_here
```

A `.env.example` file can be included in the repository as a template.

> Never commit your actual `.env` file or database password to GitHub.

---

# 📁 Project Structure

```text
ChocoCrunch-Analytics/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── SQL Queries.ipynb
├── SQL Table Design.ipynb
│
├── screenshots/
│   ├── dashboard.png
│   ├── join-queries-ratio.png
│   └── join-queries-brands.png
│
└── data/
    └── ...
```

> Local environment files such as `.env` and `.venv/` are excluded from Git using `.gitignore`.

---

# 🚀 Installation & Setup

## 1. Clone the repository

```bash
git clone https://github.com/SARAVANAN-2410/ChocoCrunch-Analytics.git
cd ChocoCrunch-Analytics
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

## 3. Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure PostgreSQL

Create the `CHOCO_CRUNCH` database in PostgreSQL and create/populate the required tables using the SQL table-design notebook.

## 6. Configure environment variables

Create `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=CHOCO_CRUNCH
DB_USER=postgres
DB_PASSWORD=your_password_here
```

## 7. Run the Streamlit application

```bash
python -m streamlit run app.py
```

---

# 🔒 Security

Sensitive configuration is intentionally excluded from version control.

The repository ignores:

```text
.env
.venv/
.streamlit/secrets.toml
__pycache__/
```

This prevents local credentials and virtual-environment files from being uploaded to GitHub.

---

# 📌 Key Skills Demonstrated

- Python
- SQL
- PostgreSQL
- Data Cleaning
- Data Transformation
- Feature Engineering
- Exploratory Data Analysis
- SQL Aggregations
- GROUP BY
- ORDER BY
- Filtering
- JOINs
- Database Design
- Pandas
- NumPy
- Streamlit
- Data Visualization
- Environment Variable Management
- Git & GitHub

---

# 💡 Project Workflow

```text
Raw Food Product Data
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
PostgreSQL Database
        ↓
┌───────────────────────────────┐
│ product_info                  │
│ nutrient_info                 │
│ derived_metrics               │
└───────────────────────────────┘
        ↓
27 SQL Analytical Queries
        ↓
Streamlit Dashboard
        ↓
Interactive Tables + EDA
```

---

## 👨‍💻 Author

**Saravanan M**

Data Science & Python Enthusiast  
Chennai, Tamil Nadu, India

GitHub: [SARAVANAN-2410](https://github.com/SARAVANAN-2410)

---

## ⭐ If you find this project useful

Feel free to explore the repository and review the SQL queries, database design, and Streamlit dashboard.