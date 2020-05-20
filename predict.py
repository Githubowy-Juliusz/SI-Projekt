import numpy as np
from loading import load_custom_images
import gc

def predict(image_size, model):
	#inverted_labels_dictionary = {v: k for k, v in Training.labels_dictionary.items()}
	dictionary = {0: "sarna/jeleń", 1: "niedźwiedź", 2: "wilk", 3: "wiewiórka", 4: "coś innego"}
	
	custom_images = load_custom_images(image_size)
	prediction = model.model.predict(custom_images)
	custom_images, prediction
	prediction_list = []
	for i in range(0, len(prediction)):
		image = (custom_images[i] * 255).astype(np.uint8)
		predicted_object = dictionary[np.argmax(prediction[i])]
		tupl = (image, predicted_object)
		prediction_list.append(tupl)
	gc.collect()
	return prediction_list