from importlib import import_module
from keras.models import load_model

NumpyModule = import_module("numpy")
NumpyModule.set_printoptions(suppress=True)
OpenCVModule = import_module("cv2")

class CameraAppAI:
    def __init__(self, CameraStyle):
        self.Title = "Yeu Tieng Anh"
        kerasModule = import_module("keras.models")
        h5pyModule = import_module("h5py")

        with open("AIMain/keras_Model.h5", "rb") as file:
            with h5pyModule.File(file, "r") as f:
                self.model = kerasModule.load_model(f, compile=False)

        # Load the labels
        self.class_names = open("AIMain/labels.txt", "r").readlines()

        # CAMERA can be 0 or 1 based on default camera of your computer
        self.camera = OpenCVModule.VideoCapture(CameraStyle)
        OpenCVModule.namedWindow(self.Title, OpenCVModule.WINDOW_NORMAL)  # WINDOW_NORMAL cho phép thay đổi kích thước cửa sổ
    
    def EndApp(self):
        self.camera.release()
        OpenCVModule.destroyAllWindows()
    
    def run(self):
        while True:
            # Grab the webcamera's image.
            ret, image = self.camera.read()

            # Resize the raw image into (224-height,224-width) pixels
            img = OpenCVModule.resize(image, (224, 224), interpolation=OpenCVModule.INTER_AREA)

            # Show the image in a window

            # Make the image a numpy array and reshape it to the models input shape.
            image = NumpyModule.asarray(img, dtype=NumpyModule.float32).reshape(1, 224, 224, 3)

            # Normalize the image array
            image = (image / 127.5) - 1

            # Predicts the model
            prediction = self.model.predict(image, verbose=0)
            
            for conf in list(prediction[0]):
                if conf > 0.50:
                    text = self.class_names[NumpyModule.argmax(prediction)]
                    text = text[2:]
                    text = text[:-1]
                    OpenCVModule.putText(img, text, (20, 50), OpenCVModule.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # cv2.imshow("Hello World",image)
            OpenCVModule.imshow(self.Title, img)


            # Listen to the keyboard for presses.
            keyboard_input = OpenCVModule.waitKey(1)

            # 27 is the ASCII for the esc key on your keyboard.
            if keyboard_input == 27:
                break