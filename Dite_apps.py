
import pandas as pd
import os

# Load dataset
df = pd.read_csv(r"FOOD-DATA-GROUP5.csv")

# Drop unnecessary columns (e.g., unnamed index columns)
df = df.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], errors="ignore")

# Check for missing values
print(df.isnull().sum())

# Fill missing values (if any)
#df.fillna(df.mean(), inplace=True)

# Display cleaned dataset info
print(df.info())
# Function to calculate daily caloric needs based on user inputs
def calculate_caloric_needs(age, weight, height, activity_level, goal):
    # Basal Metabolic Rate (BMR) Calculation using Mifflin-St Jeor Equation
    bmr = 10 * weight + 6.25 * height - 5 * age + 5  # For males (+5) & females (-161)
    
    # Activity multipliers
    activity_multiplier = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725}
    daily_caloric_needs = bmr * activity_multiplier.get(activity_level, 1.2)

    # Adjust based on goal (weight loss, maintenance, muscle gain)
    if goal == "weight loss":
        daily_caloric_needs *= 0.85  # Reduce calories
    elif goal == "muscle gain":
        daily_caloric_needs *= 1.15  # Increase calories
    
    return daily_caloric_needs

# Example usage
caloric_needs = calculate_caloric_needs(age=25, weight=70, height=175, activity_level="moderate", goal="maintenance")
print(f"Daily Caloric Needs: {caloric_needs:.2f} kcal")
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# Normalize numerical features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df.drop(columns=["food"]))

# Compute cosine similarity between foods
similarity_matrix = cosine_similarity(df_scaled)

# Function to get food recommendations
def recommend_food(food_name, top_n=5):
    if food_name not in df["food"].values:
        return "Food not found in database!"
    
    # Find index of the food
    food_idx = df[df["food"] == food_name].index[0]
    
    # Get similar foods based on cosine similarity
    similar_foods = sorted(list(enumerate(similarity_matrix[food_idx])), key=lambda x: x[1], reverse=True)[1:top_n+1]
    
    # Return recommended food names
    return df.iloc[[idx for idx, score in similar_foods]]["food"].values

# Example usage
recommended_foods = recommend_food("Apple", top_n=5)
print("Recommended Foods:", recommended_foods)
import streamlit as st

# Load model & dataset
df = pd.read_csv(r"FOOD-DATA-GROUP5.csv")

st.title("🥦 AI-Based Personalized Diet Generator")

# User inputs
age = st.number_input("Enter your age", min_value=10, max_value=100)
weight = st.number_input("Enter your weight (kg)", min_value=30, max_value=150)
height = st.number_input("Enter your height (cm)", min_value=100, max_value=220)
activity_level = st.selectbox("Select your activity level", ["sedentary", "light", "moderate", "active"])
goal = st.selectbox("Your goal", ["weight loss", "maintenance", "muscle gain"])

if st.button("Generate Diet Plan"):
    daily_calories = calculate_caloric_needs(age, weight, height, activity_level, goal)
    st.success(f"Your Daily Caloric Needs: {daily_calories:.2f} kcal")
    
    # Recommend 5 foods
    recommended_foods = df.sample(5)["food"].values
    st.write("🥗 Recommended Foods:", recommended_foods)
