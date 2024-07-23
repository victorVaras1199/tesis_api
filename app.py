import io

import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from enums.http_methods import HttpMethods
from enums.request_body import RequestBody
from utils.process_landmarks import process_landmarks

app = Flask(__name__)
CORS(app)

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

			landmarks = results.pose_landmarks.landmark

			coords_and_angles = process_landmarks(landmarks, mp_pose, image)

			cv2.putText(image, str(int(coords_and_angles["shoulder"]["right"]["angle"])), coords_and_angles["shoulder"]["right"]["coords"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
			cv2.putText(image, str(int(coords_and_angles["shoulder"]["left"]["angle"])), coords_and_angles["shoulder"]["left"]["coords"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

			cv2.putText(image, str(int(coords_and_angles["elbow"]["right"]["angle"])), coords_and_angles["elbow"]["right"]["coords"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
			cv2.putText(image, str(int(coords_and_angles["elbow"]["left"]["angle"])), coords_and_angles["elbow"]["left"]["coords"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

			cv2.putText(image, str(int(coords_and_angles["wrist"]["right"]["angle"])), coords_and_angles["wrist"]["right"]["coords"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
			cv2.putText(image, str(int(coords_and_angles["wrist"]["left"]["angle"])), coords_and_angles["wrist"]["left"]["coords"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

	_, processed_image = cv2.imencode('.jpg', image)
	processed_image_in_memory = io.BytesIO(processed_image.tobytes())

	return send_file(processed_image_in_memory, mimetype="image/jpeg", as_attachment=True, download_name=secure_filename(file.filename))

if __name__ == "__main__":
	app.run(debug=True)
