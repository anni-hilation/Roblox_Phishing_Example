from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, json
from datetime import datetime

app = Flask(__name__, static_folder='public')
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    if path != "" and os.path.exists(os.path.join('public', path)):
        return send_from_directory('public', path)
    return send_from_directory('public', 'index.html')

@app.route('/senden', methods=['POST'])
def senden():
    data = request.get_json()
    message1 = data.get('message1')
    message2 = data.get('message2')

    file_path = 'messages.json'
    new_message = {
        'message1': message1,
        'message2': message2,
        'timestamp': datetime.utcnow().isoformat()
    }

    messages = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                messages = json.load(f)
        except Exception as e:
            print('Error reading file:', e)

    messages.append(new_message)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print('Error writing file:', e)
        return 'Error saving message', 500

    return 'Message saved', 200

if __name__ == '__main__':
    app.run(port=3000)
