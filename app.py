from flask import Flask, render_template, request
from flask_cors import CORS  # Import CORS here
import mysql.connector  # Import mysql.connector here

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'Hemu',
    'user': 'root',  # Replace with your MySQL username
    'password': 'root',  # Replace with your MySQL password
    'database': 'feedback_db'  # Replace with your database name
}

@app.route('/')
def index():
    # Render the HTML form
    return render_template('clg_task1.html')  # Ensure 'clg_task1.html' is in the 'templates' folder

@app.route('/submit', methods=['POST'])
def submit_feedback():
    try:
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        restaurant_name = request.form['restaurant_name']
        rating = request.form['rating']
        rate_us = request.form['rateUS']
        comments = request.form['comments']

        # Validate form data (optional but recommended)
        if not name or not email or not restaurant_name or not rating or not rate_us:
            return "Please fill in all required fields."

        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert the form data into the feedback table
        query = """
        INSERT INTO feedback (name, email, restaurant_name, rating, rate_us, comments)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, restaurant_name, int(rating), rate_us, comments))
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        return "Feedback submitted successfully!"

    except mysql.connector.Error as db_error:
        return f"Database error: {db_error}"

    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
