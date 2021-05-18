import numpy
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense
from keras_vggface.vggface import VGGFace
import matplotlib.pyplot as plt

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
config.log_device_placement = True

sess = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session(sess)

# catalog with training data
train_dir = 'train'
# catalog with check data
val_dir = 'val'
# catalog with test data
test_dir = 'test'
# image size
img_width, img_height = 150, 150
# the size of the tensor on the basis of the input image
input_shape = (img_width, img_height, 3)
# number of training epochs
epochs = 100
# mini-sample size
batch_size = 10
# number of images for training
nb_train_samples = 3920
# number of images to check
nb_validation_samples = 490
# number of images to test
nb_test_samples = 490

vgg_face = VGGFace(include_top=False, input_shape=input_shape, pooling='None')
vgg_face.trainable = False
vgg_face.summary()

# set seed for repeatability of results
numpy.random.seed(42)

model = Sequential()

model.add(vgg_face)
model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(7))
model.add(Activation('softmax'))

# set optimization parameters
model.summary()
model.compile(loss='categorical_crossentropy',
              optimizer='SGD',
              metrics=['categorical_accuracy'])

data_generator = ImageDataGenerator(rescale=1. / 255)

train_generator = data_generator.flow_from_directory(
    train_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

val_generator = data_generator.flow_from_directory(
    val_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

test_generator = data_generator.flow_from_directory(
    test_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

# train the model
history = model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=val_generator,
    validation_steps=nb_validation_samples // batch_size)

model_json = model.to_json()
json_file = open("emotion_recognition.json", "w")
json_file.write(model_json)
json_file.close()
model.save_weights("emotion_recognition.h5")

(eval_loss, eval_accuracy) = model.evaluate_generator(test_generator, nb_test_samples // batch_size)
print("Accuracy based on test data: %.2f%%" % (eval_accuracy * 100))
print("Error on test data: %.2f%%" % eval_loss)
plt.figure(1)

# summarize history for accuracy
plt.subplot(212)
plt.plot(history.history['categorical_accuracy'])
plt.plot(history.history['val_categorical_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

# summarize history for loss
plt.subplot(212)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()
