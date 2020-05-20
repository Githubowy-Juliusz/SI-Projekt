import numpy as np
import os, gc, re
from PIL import Image
from scaling import scale_and_save_images

def load_images(root_directory, labels_dictionary):
	directory = os.fsencode(root_directory)
	images = []
	labels = []
	for file_ in os.listdir(directory):
		file_path = root_directory + "/" + file_.decode("utf-8")
		if os.path.isdir(file_path):
			images_, labels_ = load_images(file_path, labels_dictionary)
			images += images_
			labels += labels_
		else:
			image = Image.open(file_path)
			image.load()
			data = np.asarray(image, dtype="uint8")
			images.append(data)
			match = re.search(r"/\w+_scaled$", root_directory)
			animal_name = root_directory[match.start() + 1: -7]
			labels.append(labels_dictionary[animal_name])
	return (images, labels)

def read_image_size():
	with open("average", encoding="utf-8") as file:
		line = file.readline().replace("(", "").replace(")", "").replace(" ", "")
		size = line.split(",")
		size[0] = int(size[0])
		size[1] = int(size[1])
		return size

def load_training_testing_images(labels_dictionary):
	training_images, training_labels = load_images("Images_scaled/Training_scaled", labels_dictionary)
	testing_images, testing_labels = load_images("Images_scaled/Testing_scaled", labels_dictionary)

	training_images = np.array(training_images)
	testing_images = np.array(testing_images)
	training_labels = np.array(training_labels)
	testing_labels = np.array(testing_labels)

	#shuffling images around
	randomizing = np.arange(testing_images.shape[0])
	np.random.shuffle(randomizing)
	testing_images = testing_images[randomizing]
	testing_labels = testing_labels[randomizing]

	training_images = training_images / 255.0
	testing_images = testing_images / 255.0
	gc.collect()
	return (training_images, training_labels, testing_images, testing_labels)

def load_custom_images(image_size):
	scale_and_save_images("Custom_testing_images", "Custom_testing_images_scaled", image_size)
	directory = os.fsencode("Custom_testing_images_scaled")
	custom_images = []
	for file_ in os.listdir(directory):
		file_path = "Custom_testing_images_scaled/" + file_.decode("utf-8")
		image = Image.open(file_path)
		image.load()
		data = np.asarray(image, dtype="uint8")
		custom_images.append(data)
	custom_images = np.array(custom_images)
	custom_images = custom_images / 255.0
	gc.collect()
	return custom_images