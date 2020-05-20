import tensorflow as tf
from tensorflow import keras
import os, gc

class Model:
	def __init__(self, name, model_function):
		self.name = name
		self.model_function = model_function
		self.model = None
	
	def description(self, image_size):
		model = self.model_function(image_size)
		stringlist = []
		model.summary(print_fn=lambda x: stringlist.append(x))
		model_description = "\n".join(stringlist)
		del model
		gc.collect()
		keras.backend.clear_session()
		tf.compat.v1.reset_default_graph()
		return model_description
	
	def load_model(self, image_size, load_saved_model=None):
		model_file_name = f"./Saved_Models/{self.name}_{image_size[0]}_{image_size[1]}.h5"
		if os.path.isfile(model_file_name):
			if load_saved_model is None:
				print("Found saved model!")
				return "Found saved model!"
			if load_saved_model == True:
				self.model = keras.models.load_model(model_file_name)
				print("Loaded!")
				return "Loaded!"
		if (not os.path.isfile(model_file_name)) and load_saved_model == True:
			print("None")
			return None
		self.model = self.model_function(image_size)
		print("Created!")
		return "Created!"
	
	def clear_model(self):
		try:
			del self.model
			gc.collect()
			keras.backend.clear_session()
			tf.compat.v1.reset_default_graph()
			self.model = None
		except:
			print(f"Error clearing model: {self.name}")
	
	def save(self, image_size):
		model_file_name = f"./Saved_Models/{self.name}_{image_size[0]}_{image_size[1]}.h5"
		self.model.save(model_file_name)
	
	def __str__(self):
		return self.name

def model_cnn_a(image_size):
	model = keras.Sequential([
		keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(image_size[1], image_size[0], 3)),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(32, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(32, (3, 3), activation="relu"),
		keras.layers.Flatten(),
		keras.layers.Dense(64, activation="relu"),
		keras.layers.Dense(5, activation="softmax")
	])
	model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
	return model


def model_cnn_b(image_size):
	model = keras.Sequential([
		keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(image_size[1], image_size[0], 3)),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(64, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(64, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(64, (3, 3), activation="relu"),
		keras.layers.Flatten(),
		keras.layers.Dense(64, activation="relu"),
		keras.layers.Dense(5, activation="softmax")
	])
	model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
	return model

def model_cnn_c(image_size):
	model = keras.Sequential([
		keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(image_size[1], image_size[0], 3)),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(32, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(16, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(16, (3, 3), activation="relu"),
		keras.layers.Flatten(),
		keras.layers.Dense(64, activation="relu"),
		keras.layers.Dense(5, activation="softmax")
	])
	model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
	return model

def model_cnn_d(image_size):
	model = keras.Sequential([
		keras.layers.Conv2D(16, (3, 3), activation="relu", input_shape=(image_size[1], image_size[0], 3)),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(16, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(16, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(8, (3, 3), activation="relu"),
		keras.layers.Flatten(),
		keras.layers.Dense(32, activation="relu"),
		keras.layers.Dense(5, activation="softmax")
	])
	model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
	return model

def model_cnn_e(image_size):
	model = keras.Sequential([
		keras.layers.Conv2D(16, (3, 3), activation="relu", input_shape=(image_size[1], image_size[0], 3)),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(16, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(16, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(8, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(8, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(8, (3, 3), activation="relu"),
		keras.layers.Flatten(),
		keras.layers.Dense(32, activation="relu"),
		keras.layers.Dense(5, activation="softmax")
	])
	model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
	return model

def model_cnn_f(image_size):
	model = keras.Sequential([
		keras.layers.Conv2D(64, (3, 3), activation="relu", input_shape=(image_size[1], image_size[0], 3)),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(64, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(32, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(32, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(16, (3, 3), activation="relu"),
		keras.layers.Flatten(),
		keras.layers.Dense(64, activation="relu"),
		keras.layers.Dense(5, activation="softmax")
	])
	model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
	return model

def model_cnn_g(image_size):
	model = keras.Sequential([
		keras.layers.Conv2D(64, (3, 3), activation="relu", input_shape=(image_size[1], image_size[0], 3)),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(64, (3, 3), activation="relu"),
		keras.layers.MaxPooling2D((2, 2)),
		keras.layers.Conv2D(64, (3, 3), activation="relu"),
		keras.layers.Flatten(),
		keras.layers.Dense(64, activation="relu"),
		keras.layers.Dense(5, activation="softmax")
	])
	model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
	return model