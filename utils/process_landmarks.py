import numpy as np

from .calculate_angle import calculate_angle


def process_landmarks(landmarks, mp_pose, image):
	left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
	right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

	left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
	right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

	left_pinky = [landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value].x, landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value].y]
	right_pinky = [landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value].y]

	left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
	right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

	left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
	right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

	right_shoulder_angle = calculate_angle(right_elbow, right_shoulder, right_hip)
	left_shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow)

	right_elbow_angle = calculate_angle(right_wrist, right_elbow, right_shoulder)
	left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

	right_wrist_angle = calculate_angle(right_pinky, right_wrist, right_elbow)
	left_wrist_angle = calculate_angle(left_elbow, left_wrist, left_pinky)

	return {
		"elbow": {
			"right": int(right_elbow_angle),
			"left": int(left_elbow_angle)
		},
		"shoulder": {
			"right": int(right_shoulder_angle),
			"left": int(left_shoulder_angle)
		},
		"wrist": {
			"right": int(right_wrist_angle),
			"left": int(left_wrist_angle)
		}
	}
