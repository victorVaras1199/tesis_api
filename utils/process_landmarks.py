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

	left_elbow_coords = tuple(np.multiply(left_elbow, [image.shape[1], image.shape[0]]).astype(int))
	right_elbow_coords = tuple(np.multiply(right_elbow, [image.shape[1], image.shape[0]]).astype(int))

	left_shoulder_coords = tuple(np.multiply(left_shoulder, [image.shape[1], image.shape[0]]).astype(int))
	right_shoulder_coords = tuple(np.multiply(right_shoulder, [image.shape[1], image.shape[0]]).astype(int))

	left_wrist_coords = tuple(np.multiply(left_wrist, [image.shape[1], image.shape[0]]).astype(int))
	right_wrist_coords = tuple(np.multiply(right_wrist, [image.shape[1], image.shape[0]]).astype(int))

	return {
		"elbow": {
			"right": {
				"angle": right_elbow_angle,
				"coords": right_elbow_coords
			},
			"left": {
				"angle": left_elbow_angle,
				"coords": left_elbow_coords
			}
		},
		"shoulder": {
			"right": {
				"angle": right_shoulder_angle,
				"coords": right_shoulder_coords
			},
			"left": {
				"angle": left_shoulder_angle,
				"coords": left_shoulder_coords
			}
		},
		"wrist": {
			"right": {
				"angle": right_wrist_angle,
				"coords": right_wrist_coords
			},
			"left": {
				"angle": left_wrist_angle,
				"coords": left_wrist_coords
			}
		}
	}
