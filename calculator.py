# Import required libraries
from flask import Flask, request, jsonify  # Flask for web server
import mysql.connector                     # For database connection
from flask_cors import CORS               # To allow web browser access
from dotenv import load_dotenv            # For loading environment variables
import os                                # For accessing environment variables

# Load environment variables from .env file
load_dotenv()

# Create a Flask web application
app = Flask(__name__)
CORS(app)  # Allow web browser to access this server

# Function to connect to MySQL database
def connect_to_database():
    # Database connection settings from environment variables
    database_settings = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    # Return database connection
    return mysql.connector.connect(**database_settings)

# Function to save calculation to database
def save_to_database(math_expression, answer):
    try:
        # Connect to database
        database = connect_to_database()
        cursor = database.cursor()

        # Save calculation to database
        save_query = "INSERT INTO calculations (expression, result) VALUES (%s, %s)"
        cursor.execute(save_query, (math_expression, str(answer)))
        
        # Commit changes and close connection
        database.commit()
        cursor.close()
        database.close()
        return True
    
    except Exception as error:
        # If there's an error, print it
        print(f"Could not save to database: {error}")
        return False

# Handle calculation requests from the web calculator
@app.route('/calculate', methods=['POST'])
def process_calculation():
    try:
        # Get the calculation from the web calculator
        data = request.get_json()
        math_expression = data.get('expression')
        
        # Convert calculator symbols to Python math symbols
        math_expression = math_expression.replace('×', '*').replace('÷', '/')
        
        # Calculate the answer
        answer = eval(math_expression)
        
        # Round decimal numbers to 2 places
        if isinstance(answer, float):
            answer = round(answer, 2)
        
        # Save the calculation in database
        save_to_database(math_expression, answer)
        
        # Send the answer back to calculator
        return jsonify({
            'success': True,
            'result': answer
        })
    
    except Exception as error:
        # If there's an error in calculation
        return jsonify({
            'success': False,
            'error': str(error)
        }), 400

# Start the web server
if __name__ == '__main__':
    app.run(debug=True, port=5000)
