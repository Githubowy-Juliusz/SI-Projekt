from PyQt5 import QtCore, QtGui, QtWidgets
from MainView import MainView
from PredictView import PredictView
import sys
#pip install tensorflow opencv-python pillow


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.main_view = MainView()
		self.predict_view = PredictView()
		self.model = None
		
		#center window
		qtRectangle = self.frameGeometry()
		centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())
		self.show_main_view()
	
	def create_popup_window(self, title, message):
		popup_window = QtWidgets.QMessageBox()
		popup_window.setWindowTitle(title)
		popup_window.setText(message)
		popup_window.exec_()
	
	def create_question_window(self, title, message):
		question_window = QtWidgets.QMessageBox()
		question_window.setIcon(QtWidgets.QMessageBox.Question)
		question_window.setWindowTitle(title)
		question_window.setText(message)
		question_window.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		yes_button = question_window.button(QtWidgets.QMessageBox.Yes)
		yes_button.setText("Tak")
		no_button = question_window.button(QtWidgets.QMessageBox.No)
		no_button.setText("Nie")
		question_window.exec_()

		if question_window.clickedButton() == yes_button:
			return True
		elif question_window.clickedButton() == no_button:
			return False
		return None
	
	def show_main_view(self):
		self.main_view.setupUi(self, self.model)
		self.model = None
		self.show()
	
	def show_predict_view(self, predictions, model):
		self.model = model
		self.predict_view.setupUi(self, predictions)
		self.show()

app = QtWidgets.QApplication(sys.argv)
ui = MainWindow()
sys.exit(app.exec_())