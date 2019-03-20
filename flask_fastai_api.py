from flask import Flask, render_template, Response
from queue import Queue
import threading
import gevent
import os, sys, time

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


q = Queue()

path = 'model'

print('\nloading up the saved model weights...')

defaults.device = torch.device('cpu') # run inference on cpu
learn = load_learner(path)

@app.route('/predict')
def predict():
    print('Working on to predict...')
    url = request.args.get('a', 0, type=str)
    app.logger.info("Classifying image %s" % (url),)
    response = requests.get(url)
    img = open_image(BytesIO(response.content))
    t = time.time() # get execution time
    pred_class, pred_idx, outputs = learn.predict(img)
    dt = time.time() - t
    app.logger.info("Execution time: %0.02f seconds" % (dt))
    app.logger.info("Image %s classified as %s" % (url, pred_class))
    return jsonify(result=str(pred_class))



@app.route('/')
def index():
    return render_template('fastai_api.html')

if __name__ == "__main__":
    try:
        app.run()
    except:
        print ("Something wrong..")
        os._exit(1)
