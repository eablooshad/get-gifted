from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('path/to/your/inventory.csv')

# Extract unique keywords and categories
all_keywords = set()
all_categories = df['Category'].unique()

for tags in df['Keywords/Tags']:
    all_keywords.update(tags.split(','))

@app.route('/')
def index():
    return render_template('index.html', keywords=all_keywords, categories=all_categories)

@app.route('/recommend', methods=['POST'])
def recommend():
    age = request.form['age']
    selected_keywords = request.form.getlist('keywords')
    selected_categories = request.form.getlist('categories')

    # Filter based on age, keywords, and categories
    recommendations = df[
        (df['Age Range'].apply(lambda x: age_in_range(age, x))) &
        (df['Category'].isin(selected_categories)) &
        (df['Keywords/Tags'].apply(lambda x: any(kw.strip() in x for kw in selected_keywords)))
    ]

    return render_template('results.html', recommendations=recommendations)

# Helper function for age range
def age_in_range(age, age_range):
    try:
        if '+' in age_range:
            min_age = int(age_range.replace('+', '').strip())
            return int(age) >= min_age
        min_age, max_age = map(int, age_range.split('-'))
        return min_age <= int(age) <= max_age
    except ValueError:
        return False
