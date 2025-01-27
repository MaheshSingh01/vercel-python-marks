import json
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Load the data from the JSON file
        file_path = os.path.join(os.path.dirname(__file__), '../q-vercel-python.json')
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Parse query parameters
        query = self.path.split('?')[1] if '?' in self.path else ''
        params = dict(qc.split('=') for qc in query.split('&') if '=' in qc)

        # Get the requested names
        names = params.get('name', '').split(',') if 'name' in params else []

        # Fetch marks for the names
        result = {"marks": [student["marks"] for student in data if student["name"] in names]}

        # Enable CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Respond with the result
        self.wfile.write(json.dumps(result).encode('utf-8'))
