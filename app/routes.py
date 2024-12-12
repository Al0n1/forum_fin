from flask import render_template, request, jsonify
from app import app

import os
import json

from app.messageSender import MessageSender


@app.route('/')
def home_page():
    return render_template(
        'index.html',
        title='Форум Веб-разработка',
        content="This is content",
    )


@app.route('/get-messages', methods=['GET'])
def get_messages():
    try:
        with open(os.getcwd() + '\messages.json') as json_file:
            messages = json.load(json_file)
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        message_sender = MessageSender()
        data = request.get_json()

        message = data.get('message')
        timestamp = data.get('timestamp')
        data = json.dumps({'message': message, "timestamp": timestamp})

        if not message or not timestamp:
            return jsonify({"error": "Message and timestamp are required."}), 400

        result = message_sender.send_message(data)

        if not result['status']:
            return jsonify({"error": "Failed to send message.", "error_message": result['error_message']}), 500

        return jsonify({"status": "success", "message": "Message sent successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
