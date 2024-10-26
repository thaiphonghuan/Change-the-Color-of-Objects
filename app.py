import os
import numpy as np
import cv2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['OUTPUT_FOLDER'] = 'static/output/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def midRangeGrayscaleAndColor(rgb_image, color_choice):
    gray_image = np.zeros((rgb_image.shape[0], rgb_image.shape[1]), dtype=np.uint8)
    color_image = np.zeros((rgb_image.shape[0], rgb_image.shape[1], 3), dtype=np.uint8)

    color_map = {
        "đỏ": (0, 0, 255),
        "xanh": (255, 0, 0),
        "lục": (0, 255, 0),
        "tím": (255, 0, 255),
        "vàng": (0, 255, 255),
        "cam": (0, 165, 255),
        "hồng": (255, 192, 203),
        "nâu": (42, 42, 165),
        "xám": (128, 128, 128),
        "đen": (0, 0, 0)
    }
    
    chosen_color = color_map.get(color_choice.lower(), (128, 128, 128))

    for i in range(rgb_image.shape[0]):
        for j in range(rgb_image.shape[1]):
            r = rgb_image[i, j, 0]
            g = rgb_image[i, j, 1]
            b = rgb_image[i, j, 2]

            c = [r, g, b]
            c.sort()
            min_val = c[0]
            max_val = c[-1]
            
            gray_value = int(min_val * 0.5 + max_val * 0.5)
            gray_image[i, j] = gray_value

            if gray_value < 240:  
                color_image[i, j] = chosen_color
            else:
                color_image[i, j] = (gray_value, gray_value, gray_value)  

    return gray_image, color_image

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    output_image_path = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        color_choice = request.form.get('color')

        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            input_image = cv2.imread(file_path)
            _, colored_image = midRangeGrayscaleAndColor(input_image, color_choice)

            output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'colored_image.jpg')
            cv2.imwrite(output_file_path, colored_image)

            # Đường dẫn tới ảnh kết quả
            output_image_path = 'output/colored_image.jpg'

    return render_template('index.html', output_image=output_image_path)

if __name__ == '__main__':
    app.run(debug=True)
