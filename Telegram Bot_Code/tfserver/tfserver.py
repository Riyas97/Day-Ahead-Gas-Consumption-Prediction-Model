import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/predict', methods=['POST'])
def get_next_day_LSTM():
    data = request.json
    X_input = np.array(data['arr'])
    house_id = data['house_id']
    n_steps_in, n_steps_out = 24 * 7, 24 * 7
    checkpoint_path = "./checkpoints/" + str(house_id) +".0/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    model = tf.keras.Sequential()
    model.add(layers.LSTM( 168,return_sequences = True ,input_shape=(n_steps_in, 1)))
    model.add(layers.LSTM( 168))
    model.add(layers.Dense(n_steps_out))
    model.compile(optimizer='adam', loss='mse')
    
    if os.path.exists(checkpoint_dir):
        model.load_weights(checkpoint_path).expect_partial()
    print("model loaded" + checkpoint_path)
    yhat = model.predict(X_input)
    print(yhat)
    res = {'arr': yhat.tolist()}
    return res