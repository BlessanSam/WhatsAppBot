from flask import Flask, request, jsonify
import json,os,psycopg2

app = Flask(__name__)

# Get the database URL from the environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to the database
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Example: Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS phone_numbers (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(15),
    message TEXT
)
""")
conn.commit()

# Configuration
VERIFY_TOKEN = 'whatsapp_1234'  # Token to verify webhook

# Path to JSON file
JSON_FILE = "phone_numbers.json"

# Function to check if a phone number already exists
def is_phone_number_exists(phone_number):
    cursor.execute("SELECT id FROM phone_numbers WHERE phone_number = %s", (phone_number,))
    return cursor.fetchone() is not None
    
# Example: Function to save phone number and message
def save_phone_number(phone_number):
    if not is_phone_number_exists(phone_number):
            cursor.execute("INSERT INTO phone_numbers (phone_number) VALUES (%s)", (phone_number,))
            conn.commit()
            print(f"Phone number {phone_number} added to the database.")
    else:
        print(f"Phone number {phone_number} is already in the database.")
'''    
# Function to save a phone number to the JSON file
def save_phone_number(phone_number):
    try:
        # Load existing phone numbers from the JSON file
        with open(JSON_FILE, mode="r", newline="") as file:
            data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist yet, start with an empty list
        data = []

    # Check if the phone number already exists in the list
    if phone_number not in [entry['phone_number'] for entry in data]:
        # Add the phone number to the data list
        data.append({"phone_number": phone_number})
        
        # Write the updated data back to the JSON file
        with open(JSON_FILE, mode="w", newline="") as file:
            json.dump(data, file, indent=4)
        
        print(f"Phone number {phone_number} saved to {JSON_FILE}.")
    else:
        print(f"Phone number {phone_number} is already in the file, skipping.")
'''
@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        # Webhook verification with Meta
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403
        
    # Handle incoming messages
    if request.method == 'POST':
        data = request.json
        print("Received data: ", data)
        try:
            phone_number = data['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']  # Extract the phone number
            save_phone_number(phone_number)  # Save it to the JSON file
            view_numbers()
        except Exception as e:
            print(f"Error processing webhook data: {e}")
    return "OK",200

if __name__ == "__main__":
    app.run()

@app.route("/view-numbers", methods=["GET"])
def view_numbers():
    return "Hello world"
