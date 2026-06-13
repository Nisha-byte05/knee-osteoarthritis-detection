import sys
import torch
import torch.nn as nn
from torchvision.models import resnet18
from torchvision import transforms
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QMovie
from win32com.client import Dispatch

# ---------------- DEVICE ----------------
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
NUM_CLASSES = 5

# ---------------- LOAD MODEL ----------------
model = resnet18(weights=None)
model.fc = nn.Sequential(
    nn.Dropout(0.3),
    nn.Linear(model.fc.in_features, NUM_CLASSES)
)
net = model.to(DEVICE)
net.load_state_dict(torch.load("knee_oa_model.pth", map_location=DEVICE))
net.eval()

# ---------------- CLASS LABELS ----------------
def get_label(class_idx):
    return [
        "Grade 0 - Normal",
        "Grade 1 - Doubtful ",
        "Grade 2 - Mild ",
        "Grade 3 - Moderate ",
        "Grade 4 - Severe "
    ][class_idx]

# ---------------- IMAGE TRANSFORM ----------------
val_tfms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ---------------- SPEAK ----------------
def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# ---------------- PREDICTION ----------------
def predict_image(img_path):
    img = Image.open(img_path).convert("RGB")
    img_tensor = val_tfms(img).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        outputs = net(img_tensor)
        _, pred_class = torch.max(outputs, 1)
        predicted = pred_class.item()
        label = get_label(predicted)
    return predicted, label

# ---------------- GUI ----------------
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 650)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        # Frame
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 701, 651))
        self.frame.setStyleSheet("background-color: #f2f2f2;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        
        # GIF
        self.label_gif = QtWidgets.QLabel(self.frame)
        self.label_gif.setGeometry(QtCore.QRect(150, 20, 400, 300))
        self.gif = QMovie("knee_gif.gif")  # Your knee GIF file
        self.label_gif.setMovie(self.gif)
        self.gif.start()

        # Title
        self.label_title = QtWidgets.QLabel(self.frame)
        self.label_title.setGeometry(QtCore.QRect(50, 330, 600, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setText("Knee Osteoarthritis Detection")

        # Upload Button
        self.btn_upload = QtWidgets.QPushButton(self.frame)
        self.btn_upload.setGeometry(QtCore.QRect(50, 400, 200, 40))
        self.btn_upload.setText("Upload X-ray")
        self.btn_upload.setStyleSheet("background-color: #117A65; color: white; border-radius: 10px;")
        self.btn_upload.clicked.connect(self.upload_image)

        # Predict Button
        self.btn_predict = QtWidgets.QPushButton(self.frame)
        self.btn_predict.setGeometry(QtCore.QRect(450, 400, 200, 40))
        self.btn_predict.setText("Predict")
        self.btn_predict.setStyleSheet("background-color: #1F618D; color: white; border-radius: 10px;")
        self.btn_predict.clicked.connect(self.predict_result)

        # Result Label
        self.label_result = QtWidgets.QLabel(self.frame)
        self.label_result.setGeometry(QtCore.QRect(50, 470, 600, 50))
        font2 = QtGui.QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        self.label_result.setFont(font2)
        self.label_result.setText("Select an X-ray to predict")
        self.label_result.setAlignment(QtCore.Qt.AlignCenter)

        MainWindow.setCentralWidget(self.centralwidget)

        # Selected image path
        self.selected_image_path = None
        self.result_label_text = ""

    # ---------------- BUTTON FUNCTIONS ----------------
    def upload_image(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        if path:
            self.selected_image_path = path
            self.label_result.setText("Image selected. Click 'Predict' to see result.")

    def predict_result(self):
        if self.selected_image_path:
            pred_class, condition = predict_image(self.selected_image_path)
            self.label_result.setText(f"Prediction: Class {pred_class} → {condition}")
            speak(f"Result is {condition}")
        else:
            self.label_result.setText("Please select an image first!")
            speak("Please select an image first")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


