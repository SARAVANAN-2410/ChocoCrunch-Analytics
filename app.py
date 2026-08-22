import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
load_dotenv()

# Connect DB
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
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
        SELECT brand, COUNT(*) AS product_count FROM product_info WHERE brand <> 'Missing' 
        GROUP BY brand ORDER BY product_count DESC ;
        """,

        "Count unique products per brand": """
        SELECT brand, COUNT(DISTINCT product_code) AS unique_product_count FROM product_info
        WHERE brand <> 'Missing' GROUP BY brand
        ORDER BY unique_product_count DESC ;
        """,

        "Top 5 brands by product count": """
        SELECT brand, COUNT(*) AS product_count FROM product_info WHERE brand <> 'Missing'
        GROUP BY brand ORDER BY product_count DESC LIMIT 5 ;
        """,

        "Products with missing product name": """
        SELECT product_code, product_name, brand
        FROM product_info WHERE product_name = 'Missing';
        """,

        "Number of unique brands": """
        SELECT COUNT(DISTINCT brand) AS unique_brand_count
        FROM product_info WHERE brand <> 'Missing';
        """,

        "Products with code starting with '3'": """
        SELECT product_code, product_name, brand
        FROM product_info WHERE product_code LIKE '3%';
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
        SELECT p.product_code, p.product_name, p.brand, n.energy_kcal_value
        FROM product_info p JOIN nutrient_info n ON p.product_code = n.product_code
        ORDER BY n.energy_kcal_value DESC LIMIT 10;
        """,

        " Average sugars_value per nova-group": """
        SELECT nova_group, AVG(sugars_value) AS average_sugar FROM nutrient_info
        GROUP BY nova_group ORDER BY nova_group;
        """,

        "Count products with fat_value > 20g": """
        SELECT COUNT(*) AS product_count FROM nutrient_info
        WHERE fat_value > 20;
        """,

        "Average carbohydrates_value per product": """
            SELECT product_code, AVG(carbohydrates_value) AS average_carbohydrates
            FROM nutrient_info
            GROUP BY product_code
            ORDER BY product_code ;
        """,

        "Products with sodium_value > 1g": """
            SELECT p.product_code,p.product_name,p.brand,n.sodium_value
            FROM product_info AS p
            JOIN nutrient_info AS n
            ON p.product_code = n.product_code
            WHERE n.sodium_value > 1
            ORDER BY n.sodium_value DESC ;
        """,

        "Count products with non-zero fruits-vegetables-nuts content": """
            SELECT COUNT(*) AS product_count FROM nutrient_info
            WHERE fruits_vegetables_nuts_estimate_from_ingredients_100g > 0 ;
        """,

        "Products with energy-kcal_value > 500": """
            SELECT p.product_code,p.product_name,p.brand,n.energy_kcal_value
            FROM product_info AS p
            JOIN nutrient_info AS n
            ON p.product_code = n.product_code
            WHERE n.energy_kcal_value > 500
            ORDER BY n.energy_kcal_value DESC ;
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
            ORDER BY product_count DESC ;
        """,

        "Count of High Sugar products": """
            SELECT COUNT(*) AS high_sugar_count FROM derived_metrics
            WHERE sugar_category = 'High Sugar' ;
        """,

        "Average sugar_to_carb_ratio for High Calorie products": """
        SELECT AVG(sugar_to_carb_ratio) AS average_ratio FROM derived_metrics
        WHERE calorie_category = 'High Calorie' AND sugar_to_carb_ratio NOT IN ('Infinity', '-Infinity');
        """,

        " Products that are both High Calorie and High Sugar": """
            SELECT product_code,calorie_category,sugar_category
            FROM derived_metrics WHERE calorie_category = 'High'
            AND sugar_category = 'High Sugar' ;
        """,

        "Number of products marked as ultra-processed": """
            SELECT COUNT(*) AS ultra_processed_count FROM derived_metrics
            WHERE is_ultra_processed = 'Yes' ;
        """,

        " Products with sugar_to_carb_ratio > 0.7": """
            SELECT product_code, sugar_to_carb_ratio FROM derived_metrics WHERE sugar_to_carb_ratio > 0.7
            AND sugar_to_carb_ratio NOT IN ('Infinity', '-Infinity')
            ORDER BY sugar_to_carb_ratio DESC ;
        """,

        " Average sugar_to_carb_ratio per calorie_category": """
        SELECT calorie_category, AVG(sugar_to_carb_ratio) AS average_ratio
        FROM derived_metrics WHERE sugar_to_carb_ratio NOT IN ('Infinity', '-Infinity')
        GROUP BY calorie_category ORDER BY average_ratio DESC;
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
            LIMIT 5 ;
        """,

        "Average energy-kcal_value for each calorie_category": """
            SELECT d.calorie_category,AVG(n.energy_kcal_value) AS average_energy_kcal
            FROM derived_metrics AS d
            JOIN nutrient_info AS n
            ON d.product_code = n.product_code
            GROUP BY d.calorie_category
            ORDER BY d.calorie_category ;
        """,

        "Count of ultra-processed products per brand": """
            SELECT p.brand, COUNT(*) AS ultra_processed_count FROM product_info p
            JOIN derived_metrics d ON p.product_code = d.product_code
            WHERE d.is_ultra_processed = 'Yes' AND p.brand <> 'Missing' GROUP BY p.brand
            ORDER BY ultra_processed_count DESC ; 
        """,

        "Products with High Sugar and High Calorie along with brand": """
            SELECT p.product_code,p.product_name,p.brand,d.calorie_category,d.sugar_category
            FROM product_info AS p JOIN derived_metrics AS d
            ON p.product_code = d.product_code
            WHERE d.calorie_category = 'High'
            AND d.sugar_category = 'High Sugar' AND p.brand <> 'Missing';
        """,

        "Average sugar content per brand for ultra-processed products": """
            SELECT p.brand,AVG(n.sugars_value) AS average_sugar_content
            FROM product_info AS p JOIN nutrient_info AS n
            ON p.product_code = n.product_code JOIN derived_metrics AS d
            ON p.product_code = d.product_code
            WHERE d.is_ultra_processed = 'Yes'
            AND p.brand <> 'Missing'
            GROUP BY p.brand
            ORDER BY average_sugar_content DESC ;
        """,

        "Number of products with fruits/vegetables/nuts content in each calorie_category": """
            SELECT d.calorie_category, COUNT(*) AS product_count
            FROM derived_metrics AS d JOIN nutrient_info AS n
            ON d.product_code = n.product_code
            WHERE n.fruits_vegetables_nuts_estimate_from_ingredients_100g > 0
            GROUP BY d.calorie_category
            ORDER BY product_count DESC ;
        """,

        "Top 5 products by sugar_to_carb_ratio with their calorie and sugar category": """
            SELECT p.product_code,p.product_name,p.brand,d.sugar_to_carb_ratio,d.calorie_category,d.sugar_category
            FROM product_info p JOIN derived_metrics d ON p.product_code = d.product_code
            WHERE d.sugar_to_carb_ratio NOT IN ('Infinity', '-Infinity') ORDER BY d.sugar_to_carb_ratio DESC
            LIMIT 5 ;
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

    # Load required data using JOIN
    query = """
    SELECT
        p.product_code,
        p.product_name,
        p.brand,
        n.energy_kcal_value,
        n.sugars_value,
        n.carbohydrates_value,
        n.nova_group,
        d.sugar_to_carb_ratio,
        d.calorie_category,
        d.sugar_category,
        d.is_ultra_processed
    FROM product_info p
    JOIN nutrient_info n
        ON p.product_code = n.product_code
    JOIN derived_metrics d
        ON p.product_code = d.product_code;
    """

    df = pd.read_sql(query, conn)

    # -----------------------------
    # Dataset Overview
    # -----------------------------
    st.subheader("Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Products", len(df))

    with col2:
        st.metric("Features", len(df.columns))

    with col3:
        st.metric("Unique Brands", df["brand"].nunique())

    with col4:
        st.metric(
            "Average Calories",
            f"{df['energy_kcal_value'].mean():.2f}"
        )

    # -----------------------------
    # Distribution of Key Variables
    # -----------------------------
    st.subheader("Distribution of Key Variables")

    # Calories Distribution
    st.markdown("**Calories Distribution**")

    calories_data = df["energy_kcal_value"].replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    fig, ax = plt.subplots()
    ax.hist(calories_data, bins=30)
    ax.set_xlabel("Energy (kcal)")
    ax.set_ylabel("Number of Products")
    ax.set_title("Distribution of Energy")
    st.pyplot(fig)

    # Sugar Distribution
    st.markdown("**Sugar Distribution**")

    sugar_data = df["sugars_value"].replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    fig, ax = plt.subplots()
    ax.hist(sugar_data, bins=30)
    ax.set_xlabel("Sugar (g)")
    ax.set_ylabel("Number of Products")
    ax.set_title("Distribution of Sugar")
    st.pyplot(fig)

    # Carbohydrates Distribution
    st.markdown("**Carbohydrates Distribution**")

    carb_data = df["carbohydrates_value"].replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    fig, ax = plt.subplots()
    ax.hist(carb_data, bins=30)
    ax.set_xlabel("Carbohydrates (g)")
    ax.set_ylabel("Number of Products")
    ax.set_title("Distribution of Carbohydrates")
    st.pyplot(fig)

    # Sugar-to-Carbohydrate Ratio Distribution
    st.markdown("**Sugar-to-Carbohydrate Ratio Distribution**")

    ratio_data = df["sugar_to_carb_ratio"].replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    fig, ax = plt.subplots()
    ax.hist(ratio_data, bins=30)
    ax.set_xlabel("Sugar-to-Carbohydrate Ratio")
    ax.set_ylabel("Number of Products")
    ax.set_title("Distribution of Sugar-to-Carbohydrate Ratio")
    st.pyplot(fig)

    # -----------------------------
    # Category Analysis
    # -----------------------------
    st.subheader("Product Category Analysis")

    # Calorie Category
    st.markdown("**Calorie Category Distribution**")

    calorie_counts = df["calorie_category"].value_counts()

    fig, ax = plt.subplots()
    calorie_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Calorie Category")
    ax.set_ylabel("Number of Products")
    ax.set_title("Products by Calorie Category")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

    # Sugar Category
    st.markdown("**Sugar Category Distribution**")

    sugar_counts = df["sugar_category"].value_counts()

    fig, ax = plt.subplots()
    sugar_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Sugar Category")
    ax.set_ylabel("Number of Products")
    ax.set_title("Products by Sugar Category")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

    # NOVA Group
    st.markdown("**NOVA Group Distribution**")

    nova_counts = df["nova_group"].value_counts().sort_index()

    fig, ax = plt.subplots()
    nova_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("NOVA Group")
    ax.set_ylabel("Number of Products")
    ax.set_title("Products by NOVA Group")
    st.pyplot(fig)

    # -----------------------------
    # Processing Level
    # -----------------------------
    st.subheader("Food Processing Analysis")

    processed_counts = df["is_ultra_processed"].value_counts()

    fig, ax = plt.subplots()
    processed_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Processing Category")
    ax.set_ylabel("Number of Products")
    ax.set_title("Ultra-Processed vs Other Products")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

    # -----------------------------
    # Relationship Analysis
    # -----------------------------
    st.subheader("Relationship Analysis")

    # Calories vs Sugar
    st.markdown("**Calories vs Sugar**")

    scatter_df = df[
        ["energy_kcal_value", "sugars_value"]
    ].replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    fig, ax = plt.subplots()

    ax.scatter(
        scatter_df["energy_kcal_value"],
        scatter_df["sugars_value"],
        alpha=0.5
    )

    ax.set_xlabel("Energy (kcal)")
    ax.set_ylabel("Sugar (g)")
    ax.set_title("Calories vs Sugar")

    st.pyplot(fig)

    # Energy vs NOVA Group
    st.markdown("**Energy vs NOVA Group**")

    nova_df = df[
        ["nova_group", "energy_kcal_value"]
    ].replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    fig, ax = plt.subplots()

    ax.scatter(
        nova_df["nova_group"],
        nova_df["energy_kcal_value"],
        alpha=0.5
    )

    ax.set_xlabel("NOVA Group")
    ax.set_ylabel("Energy (kcal)")
    ax.set_title("Energy vs NOVA Group")

    st.pyplot(fig)