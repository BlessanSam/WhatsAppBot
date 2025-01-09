from flask import Flask, request
import json

app = Flask(__name__)

# Configuration
# VERIFY_TOKEN = 'whatsapp_1234'  # Token to verify webhook

# Path to JSON file
JSON_FILE = "phone_numbers.json"

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

@app.route('/webhook', methods=['POST'])
def webhook():
    '''
    if request.method == 'GET':
        # Webhook verification with Meta
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403
    '''
    # Handle incoming messages
    if request.method == 'POST':
        data = request.json
        print("Received data: ", data)
        try:
            phone_number = data['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']  # Extract the phone number
            save_phone_number(phone_number)  # Save it to the JSON file
        except Exception as e:
            print(f"Error processing webhook data: {e}")
    return "OK",200

if __name__ == "__main__":
    app.run(port=5000)