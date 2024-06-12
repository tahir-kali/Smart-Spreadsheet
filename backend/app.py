from flask import Flask, request, jsonify, send_from_directory
from utils import  read_pandas
from gemini import answer_question
from flask_cors import CORS
from pathlib import Path
import os
import json
from datetime import datetime
app = Flask(__name__,static_folder='static')
CORS(app)
# Define your custom file upload path
custom_upload_path = 'uploads/'
@app.route("/")
def serve():
    """Serve Vue"""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def static_proxy(path):
    """static folder serve"""
    file_name = path.split("/")[-1]
    dir_name = os.path.join(app.static_folder, "/".join(path.split("/")[:-1]))
    return send_from_directory(dir_name, file_name)


# @app.errorhandler(404)
# def handle_404(e):
#     if request.path.startswith("/api/"):
#         return jsonify(message="Resource not found"), 404
#     return send_from_directory(app.static_folder, "index.html")


# @app.errorhandler(405)
# def handle_405(e):
#     if request.path.startswith("/api/"):
#         return jsonify(message="Mehtod not allowed"), 405
#     return e



@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Create the uploads directory if it doesn't exist
    os.makedirs(custom_upload_path, exist_ok=True)
    # Append timestamp to filename to make it unique
    filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + file.filename
    file_path = os.path.join(custom_upload_path, filename)
    # Save the file to the custom path
    file.save(file_path)
   
    return jsonify({"path":filename}), 200

@app.route('/api/ask', methods=['POST'])
def query():
    data = request.json
    question = data.get('question')
    files = data.get('files')
    excel_data = []
    for file in files:
        path = os.path.join(custom_upload_path,file)
        table = read_pandas(path)
        excel_data.append(table)
    print(f"Asking: {str(excel_data)}")
    answer = answer_question(question, str(excel_data))
    return jsonify({"answer": answer}), 200

if __name__ == '__main__':
    app.run(debug=True)
