# -*- coding: utf-8 -*-
"""problem2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hWlsaYs2JrQxONsvFbRifZrvZaZi3z0C
"""

# Harrison Black
# HA435377
# CAP 5610
# UCF Spring 2019

# Problem 2
# Use logistic regression with binary cross entropy loss

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Seed random number
np.random.seed()

# Sigma Function
def sig_func(z):
  s = 1.0 / (1.0 + np.exp(-z))
  return s

# Calculate Sigma Prime
def sig_prime(z):
  sig_prime = sig_func(z) * (1 - sig_func(z))
  return sig_prime

# Calculate Binary Cross Entropy Loss
def bin_cross_ent(a, y):
  ent = (-1.0 * (y * np.log(a))) - ((1 - y) * np.log(y - a))
  return ent

# Load data set. 60000 training images, 10000 testing images
mnist = tf.keras.datasets.mnist
(training_imgs, training_labels), (test_imgs_og, test_labels) = mnist.load_data()

number_of_imgs, num_rows, num_columns = training_imgs.shape

# Image Classifier class
class ImageClassifier:
  def __init__(self, number):
    self.number = number
    self.weight = np.random.randn(num_rows * num_columns, 1)
    self.bias = 0
  
  def model_training(self):
    
#     0.01 = 83.29 
#     0.005 = 0.8449
    learning_rate = 0.005

    for i in range(number_of_imgs):
      x = training_imgs[i]
      y = 0
      
      if training_labels[i] == self.number:
        y = 1
 
      z = self.weight.T.dot(x) + self.bias
      a = sig_func(z)
      loss = bin_cross_ent(a, y)
      prime_a = sig_prime(a)
      
      self.weight -= learning_rate * (a - y) * x
      self.bias -= (a - y) * learning_rate
      
  def prediction(self, x):
    prediction = sig_func(self.weight.T.dot(x) + self.bias)
    return prediction

# Reshape data set to vectors
training_imgs = (training_imgs.reshape(number_of_imgs, num_rows * num_columns, 1)).astype('float32') / 255
test_imgs = (test_imgs_og.reshape(10000, num_rows * num_columns)).astype('float32') / 255

# Create and train each classifier
models = []
for digit in range(10):
  models.append(ImageClassifier(digit))
  models[digit].model_training()

# Test accuracy on test images
predictions = []
answer = 0
num_right = 0

for i in range ( len(test_imgs) ):
  for j in range(len(models)):
     predictions.append(models[j].prediction(test_imgs[i]))
      
  answer = np.argmax(predictions)
  predictions.clear()
  
  if(answer == test_labels[i]):
    num_right += 1    

# Example predictions
print("Example prediction: ")
test_index = np.random.randint(0, len(test_imgs), size=None)
example_predictions = []

for k in range(len(models)):
  example_predictions.append(models[k].prediction(test_imgs[test_index]))
      
example_answer = np.argmax(example_predictions) 
  
plt.imshow(test_imgs_og[test_index])
plt.show()

print("Actual number: ", test_labels[test_index])
print("Predicted number: ", example_answer)

# Print accuracy
print("\nOverall model accuracy in decimal format: ", num_right/len(test_imgs))