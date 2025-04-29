from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Boomi API endpoint and authentication headers
BOOMI_URL = "http://apibaseqa.easystepin.com:9091/ws/rest/teams_webhook/Teams_Response/"
BOOMI_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ZWFzeXN0ZXBpbml0c2VydmljZXNsbGMtNFpOWUdPOmQ4Mzg1OGUxLWFjYTktNDFiZS1iZDA5LTVmMTQ1Njg2YmIxZA=='
}

@app.route('/forward', methods=['POST'])
def forward_request():
    try:
        # Get the incoming data from the POST request
        incoming_data = request.get_json()
        if incoming_data is None:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

        print("Incoming request data:", incoming_data)

        # Convert incoming data to JSON string
        payload = json.dumps(incoming_data)

        # Send the same payload to Boomi API
        response = requests.post(BOOMI_URL, headers=BOOMI_HEADERS, data=payload)

        # Get the response from Boomi
        target_response_data = response.text
        target_status_code = response.status_code

        # Return the response from Boomi
        return jsonify({
            "status": "success",
            "target_status_code": target_status_code,
            "target_response": target_response_data
        }), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
