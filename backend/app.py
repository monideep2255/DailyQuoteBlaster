from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage for email subscriptions and recent quotes
subscriptions = []
recent_quotes = [
    {"text": "The best way to predict the future is to create it.", "author": "Abraham Lincoln"},
    {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"}
]

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email')
    if email and email not in subscriptions:
        subscriptions.append(email)
        return jsonify({"success": True, "message": "Subscription successful!"}), 200
    return jsonify({"success": False, "message": "Subscription failed. Email may already be subscribed."}), 400

@app.route('/recent-quotes', methods=['GET'])
def get_recent_quotes():
    return jsonify({"quotes": recent_quotes}), 200

if __name__ == '__main__':
    app.run(debug=True)
