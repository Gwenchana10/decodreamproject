from flask import Flask, request, jsonify
import os
import cv2
import numpy as np
import json
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

def extract_walls_and_corners(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(binary, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

    corners = set()
    walls = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            corners.add((x1, y1))
            corners.add((x2, y2))
            walls.append({"corner1": (x1, y1), "corner2": (x2, y2)})

    return list(corners), walls

def format_for_blueprint3d(corners, walls):
    corner_ids = {corner: f"corner-{i}" for i, corner in enumerate(corners)}
    blueprint_data = {
        "floorplan": {
            "corners": {corner_ids[corner]: {"x": int(corner[0]), "y": int(corner[1])} for corner in corners},
            "walls": [
                {
                    "corner1": corner_ids[wall["corner1"]],
                    "corner2": corner_ids[wall["corner2"]],
                    "frontTexture": {"url": "rooms/textures/wallmap.png", "stretch": True, "scale": 1},
                    "backTexture": {"url": "rooms/textures/wallmap.png", "stretch": True, "scale": 1}
                }
                for wall in walls
            ]
        },
        "items": []
    }
    return json.dumps(blueprint_data, indent=2)

@app.route('/process-file', methods=['POST'])
def process_file():
    uploaded_file = request.files.get('file')

    if uploaded_file:
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)

        corners, walls = extract_walls_and_corners(file_path)
        blueprint_json = format_for_blueprint3d(corners, walls)

        output_json_path = os.path.join('uploads', 'floorplan.json')
        with open(output_json_path, 'w') as f:
            f.write(blueprint_json)

        return jsonify({"message": "File processed", "json_path": output_json_path}), 200
    else:
        return jsonify({"error": "No file uploaded"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)
