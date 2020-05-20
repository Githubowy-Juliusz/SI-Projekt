from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import random

class PredictView(object):
	def setupUi(self, MainWindow, predictions):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(600, 622)
		self.central_widget = QtWidgets.QWidget(MainWindow)
		self.central_widget.setObjectName("central_widget")
		self.next_button = QtWidgets.QPushButton(self.central_widget)
		self.next_button.setGeometry(QtCore.QRect(330, 470, 250, 35))
		self.next_button.setObjectName("next_button")
		self.return_button = QtWidgets.QPushButton(self.central_widget)
		self.return_button.setGeometry(QtCore.QRect(175, 520, 250, 35))
		self.return_button.setAutoRepeatDelay(304)
		self.return_button.setObjectName("return_button")
		self.previous_button = QtWidgets.QPushButton(self.central_widget)
		self.previous_button.setGeometry(QtCore.QRect(20, 470, 250, 35))
		self.previous_button.setObjectName("previous_button")
		self.image_label = QtWidgets.QLabel(self.central_widget)
		self.image_label.setGeometry(QtCore.QRect(10, 20, 580, 380))
		self.image_label.setText("")
		self.image_label.setObjectName("image_label")
		self.prediction_label = QtWidgets.QLabel(self.central_widget)
		self.prediction_label.setGeometry(QtCore.QRect(20, 420, 560, 30))
		self.prediction_label.setAlignment(QtCore.Qt.AlignCenter)
		self.prediction_label.setObjectName("prediction_label")
		MainWindow.setCentralWidget(self.central_widget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		#
		self.next_button.clicked.connect(self.next_image)
		self.previous_button.clicked.connect(self.previous_image)
		self.return_button.clicked.connect(self.return_to_main_view)
		self.image_label.setScaledContents(True)
		self.parent = MainWindow
		self.predictions = predictions
		self.image_index = 0
		image = self.numpyQImage(self.predictions[self.image_index][0])
		image = QtGui.QPixmap.fromImage(image)
		description = self.description() + self.predictions[self.image_index][1]
		self.image_label.setPixmap(image)
		self.prediction_label.setText(description)
		self.previous_button.setDisabled(True)
		if len(self.predictions) == 1:
			self.next_button.setDisabled(True)
		#
		QtCore.QMetaObject.connectSlotsByName(self.parent)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.next_button.setText(_translate("MainWindow", "Następny"))
		self.return_button.setText(_translate("MainWindow", "Powrót"))
		self.previous_button.setText(_translate("MainWindow", "Poprzedni"))
		self.prediction_label.setText(_translate("MainWindow", "To pewnie"))
	
	def description(self):
		rand = random.randint(1, 4)
		if rand == 1:
			return "To pewnie: "
		if rand == 2:
			return "To chyba: "
		if rand == 3:
			return "Wygląda na: "
		return "Prawdopodobnie to: "
		
	
	def numpyQImage(self, image):
		qImg = QtGui.QImage()
		if image.dtype == np.uint8:
			if len(image.shape) == 2:
				channels = 1
				height, width = image.shape
				bytesPerLine = channels * width
				qImg = QtGui.QImage(
					image.data, width, height, bytesPerLine, QtGui.QImage.Format_Indexed8
				)
				qImg.setColorTable([QtGui.qRgb(i, i, i) for i in range(256)])
			elif len(image.shape) == 3:
				if image.shape[2] == 3:
					height, width, channels = image.shape
					bytesPerLine = channels * width
					qImg = QtGui.QImage(
						image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888
					)
				elif image.shape[2] == 4:
					height, width, channels = image.shape
					bytesPerLine = channels * width
					fmt = QtGui.QImage.Format_ARGB32
					qImg = QtGui.QImage(
						image.data, width, height, bytesPerLine, fmt
					)
		return qImg
	
	def next_image(self):
		print("next_image")
		self.previous_button.setDisabled(False)
		self.image_index += 1
		image = self.numpyQImage(self.predictions[self.image_index][0])
		image = QtGui.QPixmap.fromImage(image)
		description = self.description() + self.predictions[self.image_index][1]
		self.image_label.setPixmap(image)
		self.prediction_label.setText(description)
		if self.image_index >= len(self.predictions) - 1:
			self.next_button.setDisabled(True)

	def previous_image(self):
		print("previous_image")
		self.next_button.setDisabled(False)
		self.image_index -= 1
		image = self.numpyQImage(self.predictions[self.image_index][0])
		image = QtGui.QPixmap.fromImage(image)
		description = self.description() + self.predictions[self.image_index][1]
		self.image_label.setPixmap(image)
		self.prediction_label.setText(description)
		if self.image_index == 0:
			self.previous_button.setDisabled(True)
	
	def return_to_main_view(self):
		print("return_to_main_view")
		self.parent.show_main_view()