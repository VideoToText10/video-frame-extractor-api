from flask import Flask, request, jsonify
import cv2
import os

app = Flask(__name__)

@app.route('/extract_frames', methods=['POST'])
def extract_frames_api():
    try:
        # Log the incoming request headers and data
        print("Incoming request headers:", request.headers)
        print("Incoming request data:", request.data)

        # Parse JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        # Log the parsed JSON data
        print("Parsed JSON data:", data)

        # Validate required fields
        if 'video_path' not in data:
            return jsonify({"error": "Missing 'video_path' in request"}), 400

        # Extract parameters from the JSON payload
        video_path = data.get('video_path')
        output_folder = data.get('output_folder', 'output_frames')
        frame_interval = data.get('frame_interval', 1)

        # Call the frame extraction function
        result = extract_frames(video_path, output_folder, frame_interval)
        return jsonify({"message": result})

    except Exception as e:
        # Log any exceptions
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 400

def extract_frames(video_path, output_folder, frame_interval=1):
    try:
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return f"Error: Could not open video at {video_path}"

        # Extract frames
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if count % frame_interval == 0:
                frame_path = os.path.join(output_folder, f"frame_{count:04d}.jpg")
                cv2.imwrite(frame_path, frame)
            count += 1

        # Release the video capture object
        cap.release()
        return f"Extracted {count} frames and saved to {output_folder}"

    except Exception as e:
        # Log any exceptions during frame extraction
        print("Frame extraction error:", str(e))
        return f"Error during frame extraction: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)