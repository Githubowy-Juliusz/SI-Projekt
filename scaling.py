import cv2 as cv
import os, gc, statistics, math

def get_image_sizes(root_directory):
	directory = os.fsencode(root_directory)
	image_sizes = []
	for file_ in os.listdir(directory):
		file_path = root_directory + "/" + file_.decode("utf-8")
		if os.path.isdir(file_path):
			image_sizes += get_image_sizes(file_path)
		else:
			image = cv.imread(file_path)
			image_sizes.append(image.shape)
	return image_sizes

def calculate_average_image_size(image_sizes):
	widths = []
	heights = []
	for image_size in image_sizes:
		widths.append(image_size[1])
		heights.append(image_size[0])
	average_width = math.floor(statistics.mean(widths))
	average_height = math.floor(statistics.mean(heights))
	return (average_width, average_height)

def scale_and_save_images(original_directory, copy_directory, average_image_size):
	directory = os.fsencode(original_directory)
	if not os.path.isdir(copy_directory):
		os.mkdir(copy_directory)
	for file_ in os.listdir(directory):
		file_path = original_directory + "/" + file_.decode("utf-8")
		if os.path.isdir(file_path):
			scale_and_save_images(file_path, copy_directory + "/" + file_.decode("utf-8") + "_scaled", average_image_size)
		else:
			image = cv.imread(file_path)
			resized_image = cv.resize(image, dsize=(average_image_size[0], average_image_size[1]), interpolation=cv.INTER_CUBIC)
			final_name = copy_directory + "/" + file_.decode("utf-8")
			cv.imwrite(final_name, resized_image)

def get_image_size():
	image_sizes = get_image_sizes("Images")
	average_image_size = calculate_average_image_size(image_sizes)
	gc.collect()
	return average_image_size

def scale_images(image_size):
	#average_image_size = get_image_size()
	#print(average_image_size[0]," ", average_image_size[1])
	scale_and_save_images("Images", "Images_scaled", image_size)
	gc.collect()

