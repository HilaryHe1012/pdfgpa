from flask import Flask, request, jsonify
from convert_gpa_from_pdf import extract_course, grade_converter
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = ['pdf']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/gpa', methods=['POST'])
def gpa():
    INPUT_TAG = 'transcript_file'
    # check that the request actually contains a file to parse over
    if INPUT_TAG not in request.files:
        return jsonify({"error":"no file part"}),400
    transcript_file = request.files[INPUT_TAG]

    # check if file is valid pdf type
    if allowed_file(transcript_file.filename):
        data = extract_course(transcript_file)
        return jsonify(data),201
    else:
        return jsonify({'error': 'Invalid file type'}),400

if __name__ == '__main__': # used to run and debug the api
    app.run(debug=True) 
