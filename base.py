from flask import Flask
from flask import render_template, jsonify, request
import json
import os
from PIL import Image


def create_app():  # factory pattern
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.settings")
    # override the settings in production with the settings.py
    app.config.from_pyfile('settings.py', silent=True)


    @app.route('/')
    def index():
        """
        Render a Hello World response.

        :return: Flask response
        """
        return render_template('index.html')

    @app.route('/myAge', methods=['GET', 'POST'])
    def myAge():
        if request.method == 'GET':
            return jsonify({'Age': app.config["MY_AGE"]})

        if request.method == 'POST':
            received_data = json.loads(request.data)
            app.config["MY_AGE"] = received_data.get("newAge")
            return jsonify({'log': "success"})



    @app.route('/nextImageAndText', methods=['GET', 'POST'])
    def nextImageAndText():
        # Logic to determine the next image and text
        # For simplicity, you can cycle through the images in order
        received_data = json.loads(request.data)

        img_counter = int(received_data.get("image_counter"))
        img_counter += 1
        # Get the list of images and texts
        image_files = [f for f in os.listdir('static/src') if f.endswith('.jpg')]
        image_files.sort()

        if img_counter > len(image_files)-1:
            img_counter = 0

        # Get the paths for the next image and text
        next_image_path = f'static/src/{image_files[img_counter]}'
        next_text_path = next_image_path.replace('.jpg', '.txt')
        image = Image.open(next_image_path)
        w, h = image.size

        # Read the text content
        with open(next_text_path, 'r') as text_file:
            text_content = text_file.read()

        original_list = [line.strip() for line in open(next_text_path, 'r')]
        result_list = []
        labels = {"0": "base", "1": "outer", "2": "inner"}
        outer_px = None
        print("-"*20)
        print(next_image_path)
        print("-"*20)
        for item in original_list:
            values = item.split()


            #print(int(float(values[3])*w), int(float(values[4])*h))
            ft = [labels[values[0]], "radius(px)=", (int(float(values[3])*w) +  int(float(values[4])*h))/4 , "radius(cm)="]
            # append meters data
            if labels[values[0]] == "base":
                ft.append("25")
                base_px = (int(float(values[3])*w) +  int(float(values[4])*h))/2
            elif labels[values[0]] == "outer":
                ft.append("25")
                reference_pixel = (int(float(values[3])*w) + int(float(values[4])*h))/4    #same depth
                outer_px = (int(float(values[3]) * w) + int(float(values[4]) * h)) / 2
            else:
                r = (int(float(values[3])*w) + int(float(values[4])*h))/4
                estimated_radius = (r*0.262)/ reference_pixel
                ft.append(round(estimated_radius*100,1))

            result_list.append(ft)

        if outer_px:
            x = base_px - outer_px
            remaining_height = 0.0108*x-8.428
            filled_height = 4.2 - remaining_height
            rrt = f"diff =  {x} (pixel) , height = {round(remaining_height,2)} meter , filled ={round(filled_height,2)} meter"
        else:
            rrt = f"Warning : It is full"

        result_strings = [' '.join(map(str, values)) for values in result_list]
        result_strings.append(rrt)
        result = '\n'.join(result_strings)



        return jsonify({'Age': img_counter, 'imagePath': next_image_path, 'textContent': result})

    return app