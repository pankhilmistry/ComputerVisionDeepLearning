# -*- coding: utf-8 -*-
"""cifar10_monitor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iJfwiQvIuTGafY1J_GgtDQ53ZvkELGBk
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x
import sys
sys.path.append('/content/drive/My Drive/Colab_Work/PPM/nn/conv')
from minivggnet import MiniVGGNet
sys.path.append('/content/drive/My Drive/Colab_Work/PPM/callbacks')
from trainingmonitor import TrainingMonitor
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
from keras.optimizers import SGD
from keras.datasets import cifar10
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import numpy as np
import os

print("[INFO] process ID: {}".format(os.getpid()))

print("[INFO] loading CIFAR-10 data...")

((trainX, trainY), (testX, testY)) = cifar10.load_data()

trainX = trainX.astype("float")/255.0
testX = testX.astype("float")/255.0

trainY = LabelBinarizer().fit_transform(trainY)
testY = LabelBinarizer().fit_transform(testY)

labelNames = ["airplane","automobile","bird","cat","deer","dog","frog","horse","ship","truck"]

print("[INFO] compiling model...")
opt = SGD(lr=0.01, momentum=0.9, nesterov=True)
model = MiniVGGNet.build(width=32, height=32, depth=3, classes=10)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/My\ Drive/Colab_Work/monitor_output
print("[INFO] process ID: {}".format(os.getpid()))
figPath = os.path.sep.join(['figs', "{}.png".format(os.getpid())])
#jsonPath = os.path.sep.join(['json_files', "{}.json".format(os.getpid())])

callbacks = [TrainingMonitor(figPath, jsonPath=jsonPath)]

print("[INFO] training network...")
H = model.fit(trainX,  trainY, validation_data=(testX, testY), batch_size=64, epochs=100, callbacks=callbacks, verbose=1)