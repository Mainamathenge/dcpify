# pip install flask flask-cors

from flask import Flask, Response, request
from flask_cors import CORS
import logging
import socket
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging to display incoming connection details
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Auto-detect IP address
def get_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    finally:
        sock.close()

ip = get_ip()
port = 5001

# ----------- Route to Serve Data -------------
@app.route("/data", methods=['GET'])
def serve_data():
    print(f"[DATA] /data from {request.remote_addr}")
    data = {
        "St-Marys-General-Hospital": 2142,
        "Belleville-General": 3423,
        "Thunder-Bay-Regional": 2354
    }
    json_str = json.dumps(data)
    return Response(json_str, content_type='text/plain; charset=utf-8')


# ----------- Route to Receive Results -------------
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
results_file = f"results_{timestamp}.txt"


@app.route("/results", methods=['POST'])
def receive_results():
    result = request.form.get('content')
    sliceNumber = request.form.get('element')

    print(f"[RESULT] /results from {request.remote_addr}")
    print(result)

    with open(results_file, 'a', encoding='utf-8') as f:
        f.write(f"{sliceNumber}\t{result}\n")

    return Response("Result remotely received", status=200)


if __name__ == "__main__":
    print(f" * Serving data from: http://{ip}:{port}/data")
    print(f" * Listening results at: http://{ip}:{port}/results")
    print(f" * Workers must allow origin: http://{ip}:{port}")
    app.run(host="0.0.0.0", port=port)



# Example of request.form returned from a POST request (i.e., what DCP sends as a result  
# when using job.setResultStorage('http://192.168.6.49:8001/remote_results', {'elementType': 'results'}))  
# ImmutableMultiDict([
#   ('elementType', 'results'), 
#   ('contentType', 'application/json'), 
#   ('element', 1), 
#   ('content', 3.1416)
# ])