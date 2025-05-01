

from flask import Flask, render_template, request, jsonify,abort
from deepface import DeepFace
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename
import csv
from datetime import datetime, timedelta
from your_email_script import send_attendance_email
from logger import txt_to_pdf
import ssl

app = Flask(__name__)

# Configuration
face_db_path = "images"  # Folder with images of 50 people
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ATTENDANCE_FOLDER = 'attendance'
TEACHER_EMAIL = ""
today_str = datetime.now().strftime("%Y-%m-%d")
txt_filepath = f"attendance/attendance_{today_str}.txt"
# Ensure upload and attendance folders exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(ATTENDANCE_FOLDER):
    os.makedirs(ATTENDANCE_FOLDER)

# @app.before_request
# def check_referrer():
#     # Allow if the referrer contains "127"
#     if not request.referrer or "127" not in request.referrer:
#         abort(403)  # Forbidden
@app.before_request
def check_referrer():
    ref = request.referrer
    print("Referrer:", ref)
    if not ref or ("127.0.0.1" not in ref and "localhost" not in ref):
        abort(403)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/teacher')
def email():
    return render_template('email.html')

def is_within_one_hour(name, filepath):
    """
    Check if the last attendance for this person was within the last hour.
    """
    if not os.path.isfile(filepath):
        return False

    with open(filepath, mode='r') as f:
        reader = csv.reader(f)
        header = next(reader, None)  # Skip header
        for row in reader:
            if row and row[0] == name:  # If this person exists in the file
                last_time_str = row[1] #changed row index from 2 to 1 for time
  # Time from CSV
                last_time = datetime.strptime(last_time_str, "%H:%M:%S")
                current_time = datetime.now().replace(minute=0, second=0, microsecond=0)
                time_diff = current_time - last_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
                return time_diff.total_seconds() < 3600  # Less than 1 hour (3600 seconds)
    return False

@app.route('/process_frame', methods=['POST'])
def process_frame():
    if 'frame' not in request.files:
        return jsonify({'error': 'No frame part'}), 400

    file = request.files['frame']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Read the image
    frame = cv2.imread(file_path)

    try:
        # Perform face recognition with stricter settings
        result = DeepFace.find(
            img_path=frame,
            db_path=face_db_path,
            model_name='ArcFace',
            detector_backend='opencv',
            enforce_detection=False,  # Require face detection
            distance_metric='cosine',  # Use cosine distance
            threshold=0.6  # Adjust this threshold (lower for stricter matching)
        )

        today = datetime.now().strftime("%Y-%m-%d")
        csv_filename = f"attendance_{today}.csv"
        csv_filepath = os.path.join(ATTENDANCE_FOLDER, csv_filename)

        if len(result) > 0 and len(result[0]) > 0:  # Ensure there are results and matches
            # identity = result[0].iloc[0]['identity']
            # distance = result[0].iloc[0]['distance']  # Check matching distance

            # # Only consider a match if the distance is below the threshold
            # if distance < 0.6:  # Stricter matching
            #     name_roll = os.path.splitext(filename_only)[0]  # Remove extension
            #     parts = name_roll.rsplit('_', 1)  # Split into name and roll
            #     if len(parts) == 2:
            #         name, roll_number = parts
            #     else:
            #         name, roll_number = name_roll, "Unknown"
            #     # message = f"Matched: {name} (Distance: {distance:.4f})"
            #     message = f"Matched: {name} (Distance: {distance:.4f})"

            #     # Check if this person was already marked within the last hour
            #     if not is_within_one_hour(name, csv_filepath):
            #         # Log the match to a CSV file
            #         file_exists = os.path.isfile(csv_filepath)
            #         if not file_exists:
            #             with open(csv_filepath, mode='w', newline='') as f:
            #                 writer = csv.writer(f)
            #                 writer.writerow(["Name", "Roll Number", "Time", "Distance"])


            #         with open(csv_filepath, mode='a', newline='') as f:
            #             time_now = datetime.now().strftime("%H:%M:%S")
            #             writer = csv.writer(f)
            #             writer.writerow([name, roll_number, time_now, distance])


            #         response = {'status': 'success', 'message': message}
            #     else:
            #         response = {'status': 'success', 'message': f"Already marked within last hour: {name}"}
            # else:
            #     response = {'status': 'success', 'message': "Unknown Face (Distance too high)"}
            match = result[0].iloc[0]
            identity = match['identity']
            distance = match['distance']

            if distance < 0.6:
                filename_only = os.path.basename(identity)
                name_roll = os.path.splitext(filename_only)[0]
                parts = name_roll.split('_')

                if len(parts) >= 3:
                    filename_only = os.path.basename(identity)
                    name = filename_only   # Join everything before roll number if name has underscores
                    roll_number = parts[-2]
                    roll_number = f"1MV24RI{roll_number}"
                else:
                    name = name_roll
                    roll_number = "Unknown"

                message = f"Matched: {name} ({roll_number}) (Distance: {distance:.4f})"

                if not is_within_one_hour(name, txt_filepath):
                    file_exists = os.path.isfile(txt_filepath)
                    if not file_exists:
                        with open(txt_filepath, mode='w') as f:
                            f.write("Name,Time,Distance\n")

                    with open(txt_filepath, mode='a') as f:
                        time_now = datetime.now().strftime("%H:%M:%S")
                        f.write(f"{name},{time_now},{distance}\n")

                    response = {'status': 'success', 'message': message}
                else:
                    response = {
                        'status': 'success',
                        'message': f"Already marked within last hour: {name} (Roll No: {roll_number})"
                    }


        else:
            response = {'status': 'success', 'message': "No Face Detected or Unknown Face"}

    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    # Clean up
    if os.path.exists(file_path):
        os.remove(file_path)

    return jsonify(response)

@app.route('/send_email', methods=['POST'])
def send_email():
    today = datetime.now().strftime("%Y-%m-%d")
    txt_to_pdf(txt_filepath, f"attendance/attendance_{today}.pdf")
    attendance_file = os.path.join(ATTENDANCE_FOLDER, f"attendance_{today}.pdf") #changed csv to txt

    if os.path.exists(attendance_file):
        send_attendance_email(TEACHER_EMAIL, attendance_file)
        return jsonify({'message': 'Attendance Email Sent!'})
    else:
        return jsonify({'message': 'Attendance file not found!'})

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5008)
    # app.run(debug=True, host='0.0.0.0', port=5008, ssl_context=('cert.pem', 'key.pem'))
    # app.run(debug=True, host='0.0.0.0', port=5008, ssl_context='adhoc')
    app.run(host='0.0.0.0', port=5008)
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
    # app.run(host='0.0.0.0', port=5008, debug=True, ssl_context=context)

