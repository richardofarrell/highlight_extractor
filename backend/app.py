from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from image_processing import extract_highlighted_text

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    highlighted_text = extract_highlighted_text(file_path)
    return jsonify(highlighted_text=highlighted_text)

if __name__ == '__main__':
    app.run(debug=True)
