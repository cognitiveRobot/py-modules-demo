from flask import Flask, render_template, Response
import os, sys, time

import datetime
import hashlib

print('importing libraries...')
from flask import request, jsonify #for fastai
import logging
import random

from PIL import Image
# import requests, os
from io import BytesIO
# import fastai stuff
from fastai import *
from fastai.vision import *
import fastai

app = Flask(__name__)
app.debug = True

path = 'model'
image_path = 'static/uploaded_images'

print('\nloading up the saved model weights...')

defaults.device = torch.device('cpu') # run inference on cpu
# learn = load_learner(path)
learn = load_learner(path, fname='bear-classifier-resnet50-4classes.pkl')

file_extension = ''
ALLOWED_FILES = set(['png', 'jpg', 'jpeg'])
def file_allowed(filename):
    file_extension = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and  file_extension in ALLOWED_FILES

def classify(img):
    pred_class, pred_idx, outputs = learn.predict(img)


    probs_in_percentage = [x.numpy() * 100 for x in torch.nn.functional.softmax(np.log(outputs), dim=0)]

    final_result = sorted(
        zip(learn.data.classes, probs_in_percentage ),
        key=lambda p: p[1],
        reverse=True)

    predicted_item = final_result[0][0]
    if final_result[0][1] < 50.0:
        predicted_item = "Confused"

    return (probs_in_percentage, final_result, predicted_item)

@app.route('/upload_image', methods = ['POST'])
def upload_image():
    print("uploading an image")
    if 'file' not in request.files:
        print("No file found")
        url = request.form.get("url")
        print(url)
        app.logger.info("Classifying image %s" % (url),)
        response = requests.get(url)
        img = open_image(BytesIO(response.content))

        print(file_allowed(url))

        print(url.rsplit('.', 1)[1].lower())

        filename = os.path.join(image_path, 'last.') + url.rsplit('.', 1)[1].lower()
        img.save(filename)

        print(filename)

        probs_in_percentage, final_result, predicted_item = classify(img)
        return render_template('pytorch_fastai_classifier.html',
                                img_file = filename,
                                final_result=final_result,
                                classes = learn.data.classes,
                                probs_in_percentage = probs_in_percentage,
                                predicted_item = predicted_item)

    file = request.files['file']

    print(file.filename)

    if file and file_allowed(file.filename):
        print("file is saving for display for future improvement")
        # hashlib.sha256(str(datetime.datetime.now()).encode('utf-8')).hexdigest()
        filename = os.path.join(image_path,file.filename)
        file.save(filename)

        img = open_image(filename)


        probs_in_percentage, final_result, predicted_item = classify(img)
        # final_result=json.dumps(final_result, sort_keys = True, indent = 4, separators = (',', ': '))

        print(filename)

        return render_template('pytorch_fastai_classifier.html',
                                img_file = filename,
                                final_result=final_result,
                                classes = learn.data.classes,
                                probs_in_percentage = probs_in_percentage,
                                predicted_item = predicted_item)

    print("Please select an image file in .jpg or .png or .jpeg")
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('pytorch_fastai_classifier.html')

if __name__ == "__main__":
    try:
        app.run()
    except:
        print ("Something wrong..")
        os._exit(1)
