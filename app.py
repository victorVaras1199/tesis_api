import io
import cv2
import numpy as np
import mediapipe as mp

from enum import Enum
from flask import Flask, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

class HttpMethods(Enum):
	"""
	Enumeration for HTTP methods.

	Attributes:
		POST: Represents the HTTP POST method.
	"""
	POST = "POST"

class RequestBody(Enum):
	"""
	Enumeration for request body fields.

	Attributes:
		FILE: Represents the 'file' field in a request body.
	"""
	FILE = "file"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/estimate-pose", methods=[HttpMethods.POST.value])
def estimate_pose():
	"""
	Endpoint to estimate the pose in an image sent via a POST request.

	The image should be sent in a form field named "file".
	The image is processed to estimate pose landmarks and the image with the drawn landmarks is returned.

	Returns:
		- If no file is sent: "No file part", 400
		- If no file is selected: "No selected file", 400
		- Processed image with drawn landmarks in JPEG format.
	"""
	if RequestBody.FILE.value not in request.files:
		return "No file part", 400

	file = request.files[RequestBody.FILE.value]

	if file.filename == "":
		return "No selected file", 400

	mp_drawing = mp.solutions.drawing_utils
	mp_pose = mp.solutions.pose

	file_in_memory = io.BytesIO()
	file.save(file_in_memory)
	file_in_memory.seek(0)

	file_bytes = np.frombuffer(file_in_memory.read(), np.uint8)
	image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

	with mp_pose.Pose(static_image_mode=True) as pose:
		image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		results = pose.process(image_rgb)

		if results.pose_landmarks is not None:
			mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

	_, processed_image = cv2.imencode('.jpg', image)
	processed_image_in_memory = io.BytesIO(processed_image.tobytes())

	return send_file(processed_image_in_memory, mimetype="image/jpeg", as_attachment=True, download_name=secure_filename(file.filename))

if __name__ == "__main__":
	app.run(debug=True)
