from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

@app.route('/transcribe', methods=['GET'])
def transcribe():
    # Get the URL from the query parameter
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required."}), 400

    headers = {"x-gladia-key": "14906f01-6eb4-4b0a-8cc6-3f734493c43a"}

    try:
        # Initial request to get the transcription status
        response = requests.get(url, headers=headers)
        data = response.json()

        # Check the status and wait if it's queued
        status = data.get('status')
        while status == 'queued':
            response = requests.get(url, headers=headers)
            data = response.json()
            status = data.get('status')
            print(status)  # Optional: Print status updates

        # Return the final response
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to decode JSON response."}), 500

if __name__ == '__main__':
    app.run(debug=True)