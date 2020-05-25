from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from scaling import scale_images
from Training import Training
from predict import predict
import models, time


class AtomicAnswer():
	def __init__(self):
		self.answer = "waiting"
	
	def get(self):
		return self.answer
	
	def set_(self, answer):
		self.answer = answer


class TrainingThread(QObject):
	add_to_text_edit = pyqtSignal(str)
	create_question_window = pyqtSignal(str, str)
	set_model = pyqtSignal(object)
	enable_controls = pyqtSignal()
	finish_thread = pyqtSignal()

	def __init__(self, epochs, image_size, model, current_model, question_answer, parent=None):
		super(TrainingThread, self).__init__(parent)
		self.epochs = epochs
		self.image_size = image_size
		self.model = model
		self.current_model = current_model
		self.question_answer = question_answer
		print("Created thread")
	
	@pyqtSlot()
	def run(self):
		scale_images(self.image_size)
		if self.current_model is None:
			self.add_to_text_edit.emit("Ładowanie modelu...")
			if self.model.load_model(self.image_size) == "Found saved model!":
				self.create_question_window.emit("Wczytanie", "Model został już wcześniej zapisany, wczytać go?")
				#WAITING FOR USER INPUT
				while self.question_answer.get() == "waiting":
					#print("Waiting!")
					time.sleep(0.1)
				if self.question_answer.get() == "yes":
					self.model.load_model(self.image_size, True)
				else:
					self.model.load_model(self.image_size, False)
				self.question_answer.set_("waiting")
		else:
			self.model = self.current_model
		
		self.add_to_text_edit.emit("Wczytywanie zdjęć...")
		self.add_to_text_edit.emit("")
		training = Training(self.image_size, self.model)
		for epoch in range(1, self.epochs + 1):
			self.add_to_text_edit.emit(f"Epoka: {epoch}")
			self.add_to_text_edit.emit("Trenowanie...")
			loss, acc = training.train()
			self.add_to_text_edit.emit("Wynik trenowania:")
			self.add_to_text_edit.emit(f"Strata: {loss}")
			self.add_to_text_edit.emit(f"Dokładność: {acc}")
			self.add_to_text_edit.emit("Testowanie...")
			loss, acc = training.evaluate()
			self.add_to_text_edit.emit("Wynik testowania:")
			self.add_to_text_edit.emit(f"Strata: {loss}")
			self.add_to_text_edit.emit(f"Dokładność: {acc}")
			self.add_to_text_edit.emit("")
		
		self.create_question_window.emit("Zapis", "Zapisać model?")
		#WAITING FOR USER INPUT
		while self.question_answer.get() == "waiting":
			#print("Waiting!")
			time.sleep(0.1)
		
		if self.question_answer.get() == "yes":
			self.add_to_text_edit.emit("Zapisywanie...")
			self.model.save(self.image_size)
		self.question_answer.set_("waiting")

		self.set_model.emit(self.model)
		self.add_to_text_edit.emit("Zakończenie treningu.")
		self.enable_controls.emit()
		self.finish_thread.emit()

class MainView(QObject):
	def __init__(self, parent=None):
		super(MainView, self).__init__(parent)

	def setupUi(self, MainWindow, model=None):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(600, 600)
		self.central_widget = QtWidgets.QWidget(MainWindow)
		self.central_widget.setObjectName("central_widget")
		self.models_combobox = QtWidgets.QComboBox(self.central_widget)
		self.models_combobox.setGeometry(QtCore.QRect(170, 50, 251, 41))
		self.models_combobox.setObjectName("models_combobox")
		self.models_combobox.addItem("")
		self.train_button = QtWidgets.QPushButton(self.central_widget)
		self.train_button.setGeometry(QtCore.QRect(170, 440, 251, 36))
		self.train_button.setObjectName("train_button")
		self.test_button = QtWidgets.QPushButton(self.central_widget)
		self.test_button.setGeometry(QtCore.QRect(170, 540, 251, 36))
		self.test_button.setObjectName("test_button")
		self.model_info_text_edit = QtWidgets.QTextEdit(self.central_widget)
		self.model_info_text_edit.setGeometry(QtCore.QRect(10, 110, 580, 260))
		self.model_info_text_edit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.model_info_text_edit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.model_info_text_edit.setAutoFormatting(QtWidgets.QTextEdit.AutoNone)
		self.model_info_text_edit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
		self.model_info_text_edit.setReadOnly(True)
		self.model_info_text_edit.setObjectName("model_info_text_edit")
		self.epoch_number = QtWidgets.QLineEdit(self.central_widget)
		self.epoch_number.setGeometry(QtCore.QRect(170, 390, 251, 34))
		self.epoch_number.setObjectName("epoch_number")
		self.load_button = QtWidgets.QPushButton(self.central_widget)
		self.load_button.setGeometry(QtCore.QRect(170, 490, 251, 36))
		self.load_button.setObjectName("load_button")
		MainWindow.setCentralWidget(self.central_widget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.retranslateUi(MainWindow)
		#
		self.parent = MainWindow
		self.test_button.setDisabled(True)
		self.train_button.setDisabled(True)
		self.load_button.setDisabled(True)
		
		self.train_button.clicked.connect(self.train_model)
		self.test_button.clicked.connect(self.test_model)
		self.load_button.clicked.connect(self.load_model)
		self.add_readme()

		self.image_size = (487, 340)
		#self.image_size = (244, 170)
		self.models = []
		self.add_models_to_combobox()
		self.current_model = model
		if self.current_model is not None:
			index = self.models_combobox.findText(self.current_model.name)
			self.models_combobox.setCurrentIndex(index)
			self.model_info_text_edit.setText(f"Załadowany model: {self.current_model.name}")
			self.test_button.setDisabled(False)
			self.train_button.setDisabled(False)
			self.load_button.setDisabled(False)

		self.models_combobox.currentIndexChanged.connect(self.show_model_details)
		
		self.question_answer = AtomicAnswer()
		self.thread = None
		self.training_thread = None
		#
		QtCore.QMetaObject.connectSlotsByName(self.parent)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.models_combobox.setCurrentText(_translate("MainWindow", "Modele"))
		self.models_combobox.setItemText(0, _translate("MainWindow", "Modele"))
		self.train_button.setText(_translate("MainWindow", "Trenuj"))
		self.test_button.setText(_translate("MainWindow", "Przetestuj"))
		self.model_info_text_edit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>"))
		self.epoch_number.setPlaceholderText(_translate("MainWindow", "Liczba epok"))
		self.load_button.setText(_translate("MainWindow", "Załaduj zapisany model"))

	def add_models_to_combobox(self):
		self.models.append(models.Model("model_a", models.model_cnn_a))
		self.models.append(models.Model("model_b", models.model_cnn_b))
		self.models.append(models.Model("model_c", models.model_cnn_c))
		self.models.append(models.Model("model_d", models.model_cnn_d))
		self.models.append(models.Model("model_e", models.model_cnn_e))
		self.models.append(models.Model("model_f", models.model_cnn_f))
		self.models.append(models.Model("model_g", models.model_cnn_g))
		for model in self.models:
			self.models_combobox.addItem(model.name)
		self.models[0].description(self.image_size)
	
	def add_readme(self):
		self.model_info_text_edit.clear()
		self.add_to_text_edit("Obrazy do testowania muszą znaleźć się w foldere \"Custom_testing_images\".")
		self.add_to_text_edit("By można było testować model, musi on być załadowany i wytrenowany.")

	def show_model_details(self):
		index = self.models_combobox.currentIndex()
		if index > 0:
			self.test_button.setDisabled(False)
			self.train_button.setDisabled(False)
			self.load_button.setDisabled(False)
			try:
				self.current_model.clear_model()
			except:
				pass
			self.current_model = None
			model_details = self.models[index - 1].description(self.image_size)
			self.model_info_text_edit.setText(model_details)
		else:
			self.test_button.setDisabled(True)
			self.train_button.setDisabled(True)
			self.load_button.setDisabled(True)
			self.add_readme()
	
	def add_to_text_edit(self, string):
		old_text = self.model_info_text_edit.toPlainText()
		print(string)
		if old_text != "":
			new_text = f"{old_text}\n{string}"
			self.model_info_text_edit.setText(new_text)
		else:
			self.model_info_text_edit.setText(string)

	def disable_controls(self):
		self.test_button.setDisabled(True)
		self.train_button.setDisabled(True)
		self.load_button.setDisabled(True)
		self.models_combobox.setDisabled(True)
		self.model_info_text_edit.clear()
	
	def enable_controls(self):
		self.test_button.setDisabled(False)
		self.train_button.setDisabled(False)
		self.load_button.setDisabled(False)
		self.models_combobox.setDisabled(False)
	
	def create_question_window(self, title, message):
		print(f"Creating question window: {title}; {message}")
		if self.parent.create_question_window(title, message):
			print("emitting yes")
			self.question_answer.set_("yes")
		else:
			print("emitting no")
			self.question_answer.set_("no")
	
	def set_model(self, model):
		self.current_model = model
	
	def load_model(self):
		index = self.models_combobox.currentIndex()
		model = self.models[index - 1]
		if model.load_model(self.image_size, load_saved_model=True) != "Loaded!":
			self.parent.create_popup_window("Error", "Nie znaleziono zapisanego modelu.")
			return
		self.current_model = model
		self.model_info_text_edit.clear()
		self.add_to_text_edit("Model załadowany")

	def train_model(self):
		#DATA VALIDATION
		epochs = self.epoch_number.text()
		if epochs == "":
			self.parent.create_popup_window("Error", "Podaj ilość epok.")
			return
		try:
			epochs = int(epochs)
		except:
			self.parent.create_popup_window("Error", "Ilość epok musi być liczbą.")
			return
		if epochs > 100 or epochs <= 0:
			self.parent.create_popup_window("Error", "Ilość epok musi mieścić się w zakresie od 1 do 100.")
			return
		
		self.disable_controls()

		index = self.models_combobox.currentIndex()
		model = self.models[index - 1]
		self.add_to_text_edit(f"Rozpoczęcie treningu {model.name}.")
		self.add_to_text_edit(f"Ilość epok: {epochs}.")
		self.add_to_text_edit("Skalowanie zdjęć...")

		#CLOSING OLD THREADS
		if self.thread is not None:
			self.thread.quit()
			self.thread.wait()

		#CREATING THREAD
		self.training_thread = TrainingThread(epochs, self.image_size, model, self.current_model, self.question_answer)
		self.thread = QThread()
		self.training_thread.moveToThread(self.thread)

		self.training_thread.add_to_text_edit.connect(self.add_to_text_edit)
		#self.training_thread.create_popup_window.connect(self.parent.create_popup_window)
		self.training_thread.create_question_window.connect(self.create_question_window)
		self.training_thread.enable_controls.connect(self.enable_controls)
		self.training_thread.set_model.connect(self.set_model)
		self.training_thread.finish_thread.connect(self.finish_thread)

		self.thread.started.connect(self.training_thread.run)
		self.thread.start()
	
	def test_model(self):
		if self.current_model is None:
			self.parent.create_popup_window("Error", "Brak wytrenowanego modelu!")
			return
		predictions = predict(self.image_size, self.current_model)
		self.parent.show_predict_view(predictions, self.current_model)
	
	pyqtSlot()
	def finish_thread(self):
		self.thread.quit()
		self.thread.wait()