# The House of Demos

## 1. Thread and Queue

####  Dependencies:
  ```
  gevent==1.3.7
  greenlet==0.4.15
  pkg-resources==0.0.0
  ```
## 2. Materialize

####   Files used:
   ```
   flask_materialize_demo.py
   templates/includes/_navbar.html
   templates/layout.html
   templates/materialize.html
   ```
## 3. Flask Keras REST API
Thanks to [Adrian Rosebrock](https://github.com/jrosebr1/simple-keras-rest-api)

#### Dependencies
```
packages
  numpy-1.15.3
  Keras
  tensorflow1.5
  pillow
maybe
  request
  gevent
```
#### Uses
```
$ python flask_keras_rest_api.py
  Using TensorFlow backend.
  Loading Keras model, afterwords Flask server will start..Please wait
  2018-10-25 22:15:53.543961: I tensorflow/core/platform/cpu_feature_guard.cc:137] Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1
```
From another terminal submit request using curl:
```
$ curl -X POST -F image=@dog.jpg 'http://localhost:5000/api/predict_dog_breed'

{
  "predictions": [
    {
      "label": "beagle",
      "probability": 0.9877755641937256
    },
    {
      "label": "pot",
      "probability": 0.0020967768505215645
    },
    {
      "label": "Cardigan",
      "probability": 0.0013517026090994477
    },
    {
      "label": "Walker_hound",
      "probability": 0.0012711132876574993
    },
    {
      "label": "Brittany_spaniel",
      "probability": 0.0010085123358294368
    }
  ],
  "success": true
}

```
or check the [request script](https://github.com/cognitiveRobot/simple-keras-rest-api/blob/master/simple_request.py)

#### Issues
* Illegal instruction (core dumped)

  Solution:
```
pip uninstall tensorflow
pip install tensorflow==1.5
```
* ValueError("Tensor %s is not an element of this graph." % obj)
```
return self._as_graph_element_locked(obj, allow_tensor, allow_operation)
File "/home/zhossain/myProjects/third-party-projects/deep-learning/image-classification/simple-keras-rest-api/venv/lib/python3.6/site-packages/tensorflow/python/framework/ops.py", line 3402, in _as_graph_element_locked
raise ValueError("Tensor %s is not an element of this graph." % obj)
ValueError: Tensor Tensor("fc1000/Softmax:0", shape=(?, 1000), dtype=float32) is not an element of this graph.
```
  Solution:

  A global variable graph was created. Thanks to [Richardson-souza](https://github.com/jrosebr1/simple-keras-rest-api/pull/8/commits/083f4fa8635775a12a09710134531bcff6a5c4b4)
  ```
global model, graph
	model = ResNet50(weights="imagenet")
	graph = tf.get_default_graph()
And with default graph predictions were made:
with graph.as_default():
        preds = model.predict(image)
  ```
  or check my [commit](https://github.com/cognitiveRobot/simple-keras-rest-api/commit/725909d262f31ad775723dd12ba55c4ffe257e8a)
