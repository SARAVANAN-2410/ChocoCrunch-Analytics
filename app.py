import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# Connect DB
conn = conn = psycopg2.connect(
    host="localhost",  
    port=5432,         
    database="CHOCO_CRUNCH",
    user="postgres",
    password= ''
)

st.title("🍫 Chocolate Data Analysis Dashboard")

# Sidebar
option = st.sidebar.selectbox(
    "Select Section",
    ["Product Info", "Nutrient Info", "Derived Metrics", "Join Queries", "EDA Visualizations"]
)

# Function to run query
def run_query(query):
    return pd.read_sql(query, conn)

# -----------------------------
# 📑 PRODUCT INFO
# -----------------------------
if option == "Product Info":

    st.header("Product Info Queries")

    queries = {
        "Count products per brand": """
            SELECT brand, COUNT(*) AS product_count FROM product_info
            GROUP BY brand ORDER BY product_count DESC
        """,

        "Count unique products per brand": """
            SELECT brand, COUNT(DISTINCT product_code) AS unique_product_count
            FROM product_info GROUP BY brand
            ORDER BY unique_product_count DESC
        """,

        "Top 5 brands by product count": """
            SELECT brand,COUNT(*) AS product_count FROM product_info
            WHERE brand <> 'Missing'
            GROUP BY brand
            ORDER BY product_count DESC
            LIMIT 5
        """,

        "Products with missing product name": """
            SELECT product_code , product_name, brand FROM product_info
            WHERE product_name = 'Missing'
        """,

        "Number of unique brands": """
            SELECT COUNT(DISTINCT brand) AS unique_brand_count
            FROM product_info
        """,

        "Products with code starting with '3'": """
            SELECT product_code, product_name, brand FROM product_info
            WHERE product_code LIKE '3%'
        """
    }

    selected = st.selectbox("Choose Query", list(queries.keys()))
    df = run_query(queries[selected])
    st.dataframe(df)


# -----------------------------
# 📑 NUTRIENT INFO
# -----------------------------
elif option == "Nutrient Info":

    st.header("Nutrient Queries")

    queries = {
        "Top 10 products with highest energy-kcal_value": """
            SELECT p.product_name, p.brand, n.energy_kcal_value
            FROM product_info AS p
            JOIN nutrient_info AS n
            ON p.product_code = n.product_code
            ORDER BY n.energy_kcal_value DESC
            LIMIT 10
        """,

        " Average sugars_value per nova-group": """
            SELECT nova_group, AVG(sugars_value) AS average_sugar
            FROM nutrient_info
            GROUP BY nova_group
            ORDER BY nova_group
        """,

        "Count products with fat_value > 20g": """
            SELECT COUNT(*) AS product_count FROM nutrient_info
            WHERE fat_value > 20
        """,

        "Average carbohydrates_value per product": """
            SELECT product_code, AVG(carbohydrates_value) AS average_carbohydrates
            FROM nutrient_info
            GROUP BY product_code
            ORDER BY product_code
        """,

        "Products with sodium_value > 1g": """
            SELECT p.product_code,p.product_name,p.brand,n.sodium_value
            FROM product_info AS p
            JOIN nutrient_info AS n
            ON p.product_code = n.product_code
            WHERE n.sodium_value > 1
            ORDER BY n.sodium_value DESC
        """,

        "Count products with non-zero fruits-vegetables-nuts content": """
            SELECT COUNT(*) AS product_count FROM nutrient_info
            WHERE fruits_vegetables_nuts_estimate_from_ingredients_100g > 0
        """,

        "Products with energy-kcal_value > 500": """
            SELECT p.product_code,p.product_name,p.brand,n.energy_kcal_value
            FROM product_info AS p
            JOIN nutrient_info AS n
            ON p.product_code = n.product_code
            WHERE n.energy_kcal_value > 500
            ORDER BY n.energy_kcal_value DESC
        """
    }

    selected = st.selectbox("Choose Query", list(queries.keys()))
    df = run_query(queries[selected])
    st.dataframe(df)


# -----------------------------
# 📑 DERIVED METRICS
# -----------------------------
elif option == "Derived Metrics":

    st.header("Derived Metrics Queries")

    queries = {
        "Count products per calorie_category": """
            SELECT calorie_category,COUNT(*) AS product_count
            FROM derived_metrics
            GROUP BY calorie_category
            ORDER BY product_count DESC
        """,

        "Count of High Sugar products": """
            SELECT COUNT(*) AS product_count FROM derived_metrics
            WHERE sugar_category = 'High Sugar'
        """,

        "Average sugar_to_carb_ratio for High Calorie products": """
            SELECT AVG(sugar_to_carb_ratio) AS average_sugar_to_carb_ratio
            FROM derived_metrics
            WHERE calorie_category = 'High'
        """,

        " Products that are both High Calorie and High Sugar": """
            SELECT product_code,calorie_category,sugar_category
            FROM derived_metrics WHERE calorie_category = 'High'
            AND sugar_category = 'High Sugar'
        """,

        "Number of products marked as ultra-processed": """
            SELECT COUNT(*) AS ultra_processed_count FROM derived_metrics
            WHERE is_ultra_processed = 'Yes'
        """,

        " Products with sugar_to_carb_ratio > 0.7": """
            SELECT product_code,sugar_to_carb_ratio FROM derived_metrics
            WHERE sugar_to_carb_ratio > 0.7
            ORDER BY sugar_to_carb_ratio ASC
        """,

        " Average sugar_to_carb_ratio per calorie_category": """
            SELECT calorie_category,AVG(sugar_to_carb_ratio) AS average_sugar_to_carb_ratio
            FROM derived_metrics
            GROUP BY calorie_category
            ORDER BY calorie_category
        """
    }

    selected = st.selectbox("Choose Query", list(queries.keys()))
    df = run_query(queries[selected])
    st.dataframe(df)


# -----------------------------
# 🔗 JOIN QUERIES
# -----------------------------
elif option == "Join Queries":

    st.header("Join Queries")

    queries = {
        "Top 5 brands with most High Calorie products": """
            SELECT p.brand, COUNT(*) AS high_calorie_product_count FROM product_info AS p
            JOIN derived_metrics AS d ON p.product_code = d.product_code
            WHERE d.calorie_category = 'High' AND p.brand <> 'Missing'
            GROUP BY p.brand ORDER BY high_calorie_product_count DESC
            LIMIT 5
        """,

        "Average energy-kcal_value for each calorie_category": """
            SELECT d.calorie_category,AVG(n.energy_kcal_value) AS average_energy_kcal
            FROM derived_metrics AS d
            JOIN nutrient_info AS n
            ON d.product_code = n.product_code
            GROUP BY d.calorie_category
            ORDER BY d.calorie_category
        """,

        "Count of ultra-processed products per brand": """
            SELECT p.brand, COUNT(*) AS ultra_processed_product_count
            FROM product_info AS p JOIN derived_metrics AS d
            ON p.product_code = d.product_code
            WHERE d.is_ultra_processed = 'Yes'
            GROUP BY p.brand
            ORDER BY ultra_processed_product_count DESC
        """,

        "Products with High Sugar and High Calorie along with brand": """
            SELECT p.product_code,p.product_name,p.brand,d.calorie_category,d.sugar_category
            FROM product_info AS p JOIN derived_metrics AS d
            ON p.product_code = d.product_code
            WHERE d.calorie_category = 'High'
            AND d.sugar_category = 'High Sugar'
        """,

        "Average sugar content per brand for ultra-processed products": """
            SELECT p.brand,AVG(n.sugars_value) AS average_sugar_content
            FROM product_info AS p JOIN nutrient_info AS n
            ON p.product_code = n.product_code JOIN derived_metrics AS d
            ON p.product_code = d.product_code
            WHERE d.is_ultra_processed = 'Yes'
            GROUP BY p.brand
            ORDER BY average_sugar_content DESC
        """,

        "Number of products with fruits/vegetables/nuts content in each calorie_category": """
            SELECT d.calorie_category, COUNT(*) AS product_count
            FROM derived_metrics AS d JOIN nutrient_info AS n
            ON d.product_code = n.product_code
            WHERE n.fruits_vegetables_nuts_estimate_from_ingredients_100g > 0
            GROUP BY d.calorie_category
            ORDER BY product_count DESC
        """,

        "Top 5 products by sugar_to_carb_ratio with their calorie and sugar category": """
            SELECT p.product_name, p.brand,d.sugar_to_carb_ratio,d.calorie_category,d.sugar_category
            FROM product_info AS p JOIN derived_metrics AS d
            ON p.product_code = d.product_code
            ORDER BY d.sugar_to_carb_ratio DESC
            LIMIT 5
        """
    }

    selected = st.selectbox("Choose Query", list(queries.keys()))
    df = run_query(queries[selected])
    st.dataframe(df)


# -----------------------------
# 📊 EDA VISUALIZATION
# -----------------------------
elif option == "EDA Visualizations":

    st.header("EDA Visualizations")

    df = pd.read_sql("SELECT * FROM nutrient_info", conn)

    # Histogram
    st.subheader("Calories Distribution")
    fig, ax = plt.subplots()
    ax.hist(df['energy_kcal_value'].dropna())
    st.pyplot(fig)

    # Scatter
    st.subheader("Calories vs Sugar")
    fig, ax = plt.subplots()
    ax.scatter(df['energy_kcal_value'], df['sugars_value'])
    ax.set_xlabel("Calories")
    ax.set_ylabel("Sugar")
    st.pyplot(fig)

    # Bar
    st.subheader("NOVA Group Count")
    nova = df['nova_group'].value_counts()
    fig, ax = plt.subplots()
    nova.plot(kind='bar', ax=ax)
    st.pyplot(fig)