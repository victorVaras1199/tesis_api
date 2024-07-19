# Flask Pose Estimation API

This project is a Flask-based web API for pose estimation using MediaPipe and OpenCV. It processes images to detect and draw pose landmarks.

## Table of Contents

- [Flask Pose Estimation API](#flask-pose-estimation-api)
	- [Table of Contents](#table-of-contents)
	- [Introduction](#introduction)
	- [Requirements](#requirements)
	- [Installation](#installation)
	- [Usage](#usage)
		- [Example](#example)

## Introduction

The Flask Pose Estimation API allows you to upload an image, processes it to detect human pose landmarks, and returns the image with the landmarks drawn.

## Requirements

- Python 3.7+
- Flask
- Flask-CORS
- OpenCV
- NumPy
- MediaPipe

## Installation

1. Clone the repository:

 ```sh
 git clone https://github.com/joshcast777/pose-estimation-api.git

 cd flask-pose-estimation-api
 ```

2. Create and activate a virtual environment:

 ```sh
 python3 -m venv venv

 # For Windows
 venv\Scripts\activate

 # For Linux and macOS
 source venv/bin/activate
 ```

3. Install the required packages:

 ```sh
 pip install -r requirements.txt
 ```

## Usage

1. Start the Flask server:

 ```sh
 python app.py
 ```

2. Send a POST request to the `/estimate-pose` endpoint with an image file:

 ```sh
 curl -X POST -F "file=@path_to_your_image.jpg" http://127.0.0.1:5000/estimate-pose --output output.jpg
 ```

3. The server will process the image and return it with the pose landmarks drawn.

### Example

Here's an example of how to send a request using `curl`:

```sh
curl -X POST -F "file=@/path/to/your/image.jpg" http://127.0.0.1:5000/estimate-pose --output output.jpg
```
