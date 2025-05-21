from flask import Flask, render_template, request, jsonify
from threading import Lock

app = Flask(__name__)

# Student list (fake names)
students = [
    {"name": "22ECR157", "present": False},
    {"name": "22ECR165", "present": False},
    {"name": "22ECR140", "present": False},
    {"name": "STUDENT", "present": False},
    {"name": "STUDENT", "present": False}
]

# Fake UID mapped to student index
rfid_uid_map = {
    "443749339426": 0,   # Alice
    "987654321000": 1,   # Bob
    "123456789111": 2,   # Charlie
    "555555555555": 3,   # David
    "999999999999": 4    # Eve
}

lock = Lock()

@app.route('/')
def index():
    return render_template('index.html', students=students)

@app.route('/status')
def status():
    return jsonify({"students": students})

@app.route('/scan', methods=['POST'])
def scan_rfid():
    data = request.get_json()
    uid = data.get('uid')
    student_index = rfid_uid_map.get(uid)

    if student_index is not None:
        with lock:
            students[student_index]["present"] = True
        return jsonify({"success": True, "name": students[student_index]["name"]})
    return jsonify({"success": False, "error": "UID not recognized"})

@app.route('/reset', methods=['POST'])
def reset_attendance():
    with lock:
        for student in students:
            student["present"] = False
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
