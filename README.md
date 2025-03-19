# Abschlussprojekt-cnn-digit-recognition
Marc 12
I've watched videos about neural networks.

Marc 13
I installed everything I need for the project. 
I created the virtual environment and the data structure. You have to pay attention to version control, because not all versions support the other.
I'm using older Python because of Tensorflow (Python 3.10)
-requirements.txt

Marc 14
Getting to know the Mnist dataset and Classification. Representation, properties.
Mnist documentacion and Aurélien Gérion: Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow
notebooks -> mnist.ipynb (jupyter notebook)

Marc 17
I learned the convolutional neural network CNN basic. (Aurélien Gérion: Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow)
-Convolutional Layer with Keras
-2D convolutional layer
-Pooling Layers: max and average pooling
-Basic CNN
notebooks -> CNN.basic.ipyb

Marc 18
I wrote and trained 2 CNN models. 
-number_recignition_model.h5 normal Mnist images + weights
-number_recignition_model_noisy.h5 Salt_pepper noise Mnist images (wiew in mnist.ipynb) + weights

Marc 19
I make a new modell, baceuse the label conversation.
modell_2
Epoch 1/6
788/788 ━━━━━━━━━━━━━━━━━━━━ 11s 13ms/step - accuracy: 0.6394 - loss: 1.0543 - val_accuracy: 0.9780 - val_loss: 0.0856
Epoch 2/6
788/788 ━━━━━━━━━━━━━━━━━━━━ 10s 12ms/step - accuracy: 0.9616 - loss: 0.1572 - val_accuracy: 0.9836 - val_loss: 0.0666
Epoch 3/6
788/788 ━━━━━━━━━━━━━━━━━━━━ 10s 13ms/step - accuracy: 0.9747 - loss: 0.0967 - val_accuracy: 0.9852 - val_loss: 0.0712
Epoch 4/6
788/788 ━━━━━━━━━━━━━━━━━━━━ 10s 12ms/step - accuracy: 0.9826 - loss: 0.0765 - val_accuracy: 0.9909 - val_loss: 0.0404
Epoch 5/6
788/788 ━━━━━━━━━━━━━━━━━━━━ 10s 12ms/step - accuracy: 0.9856 - loss: 0.0580 - val_accuracy: 0.9902 - val_loss: 0.0502
Epoch 6/6
788/788 ━━━━━━━━━━━━━━━━━━━━ 10s 12ms/step - accuracy: 0.9850 - loss: 0.0640 - val_accuracy: 0.9873 - val_loss: 0.0542
438/438 ━━━━━━━━━━━━━━━━━━━━ 1s 3ms/step - accuracy: 0.9889 - loss: 0.0567

Modell_noisy_2
Epoch 1/6
788/788 ━━━━━━━━━━━━━━━━━━━━ 11s 13ms/step - accuracy: 0.6706 - loss: 0.9621 - val_accuracy: 0.9766 - val_loss: 0.0845
Epoch 2/6
788/788 ━━━━━━━━━━━━━━━━━━━━ 10s 12ms/step - accuracy: 0.9704 - loss: 0.1144 - val_accuracy: 0.9825 - val_loss: 0.0710
Epoch 3/6
788/788 ━━━━━━━━━━━━━━━━━━━━ 10s 13ms/step - accuracy: 0.9827 - loss: 0.0740 - val_accuracy: 0.9879 - val_loss: 0.0461
Epoch 4/6
788/788 ━━━━━━━━━━━━━━━━━━━━ 10s 13ms/step - accuracy: 0.9852 - loss: 0.0592 - val_accuracy: 0.9889 - val_loss: 0.0426
Epoch 5/6
788/788 ━━━━━━━━━━━━━━━━━━━━ 10s 13ms/step - accuracy: 0.9879 - loss: 0.0476 - val_accuracy: 0.9896 - val_loss: 0.0447
Epoch 6/6
788/788 ━━━━━━━━━━━━━━━━━━━━ 10s 12ms/step - accuracy: 0.9910 - loss: 0.0381 - val_accuracy: 0.9912 - val_loss: 0.0421
438/438 ━━━━━━━━━━━━━━━━━━━━ 1s 3ms/step - accuracy: 0.9883 - loss: 0.0486
Test accuracy: 0.9900

Try and test the modells (keras documantacion)