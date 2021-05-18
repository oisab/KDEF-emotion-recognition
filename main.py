import sys
import cv2
import numpy as np
from PIL import Image as ImagePIL
from keras.models import model_from_json
from keras.preprocessing import image
from usr_interface import *

img_path = 'none'


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = MainWindow()
        self.ui.setup_ui(self)
        self.setStyleSheet("background-color: #A9A9A9;")
        self.ui.push_browse.clicked.connect(self.SetPath)
        self.ui.pushRecognize.clicked.connect(self.MyFunction)

    # called when the button is clicked
    def MyFunction(self):
        global img_path
        json_file = open("emotion_recognition.json", "r")
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights("emotion_recognition.h5")
        loaded_model.compile(loss="categorical_crossentropy", optimizer="SGD", metrics=["accuracy"])
        classes = ['Afraid', 'Angry', 'Disgusted', 'Happy', 'Neutral', 'Sad', 'Surprised']
        img = image.load_img(img_path, target_size=(150, 150))
        x = image.img_to_array(img)
        x /= 255
        x = np.expand_dims(x, axis=0)
        prediction = loaded_model.predict(x)
        self.ui.label_result.setText('Recognition result:' + '\n' + classes[int(np.argmax(prediction))])

    def SetPath(self):
        self.ui.label_result.setText("")
        global img_path
        img_path, clear = QtWidgets.QFileDialog.getOpenFileName(self, 'Open image', '',
                                                                "Image Files (*.jpg)")
        img = ImagePIL.open(img_path)
        width = 281
        height = 381
        resized_img = img.resize((width, height), ImagePIL.ANTIALIAS)
        pic_path = img_path + 'resized_copy.jpg'
        resized_img.save(pic_path)
        self.ui.label_path.setText(str(img_path))
        img = cv2.imread(pic_path)
        qformat = QtGui.QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888
        img = QtGui.QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        img = img.rgbSwapped()
        self.ui.label_pic.setPixmap(QtGui.QPixmap.fromImage(img))
        self.ui.label_pic.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
