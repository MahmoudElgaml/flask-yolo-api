from flask import Flask, request, jsonify, send_file
from ultralytics import YOLO
import cv2
import os

app = Flask(__name__)
model = YOLO("best.pt")  # Your trained model

@app.route('/detect', methods=['POST'])
def detect_objects():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    image_file = request.files['image']
    image_path = "input.jpg"
    image_file.save(image_path)

    results = model(image_path)
    result = results[0]
    
    # Save the annotated image
    annotated_img = result.plot()
    output_path = "annotated.jpg"
    cv2.imwrite(output_path, annotated_img)

    # Prepare detection data
    objects = []
    for box in result.boxes:
        objects.append({
            'class': int(box.cls[0]),  # Class index
            'confidence': float(box.conf[0]),
            'bbox': [float(x) for x in box.xyxy[0]]  # [xmin, ymin, xmax, ymax]
        })

    # Return JSON and image
    return_data = {
        "detections": objects
    }

    # Flask way to return both JSON and image
    from flask import make_response
    import base64

    # Encode image to base64
    with open(output_path, "rb") as img_file:
        encoded_img = base64.b64encode(img_file.read()).decode('utf-8')

    return jsonify({
        "detections": objects,
        "image_base64": encoded_img
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Use host='0.0.0.0' to make it accessible on LAN