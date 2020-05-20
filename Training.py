from loading import load_training_testing_images, load_custom_images
import gc


class Training:
	labels_dictionary = {"Deer": 0, "Bear": 1, "Wolf": 2, "Squirrel": 3, "Unknown": 4}
	def __init__(self, image_size, model):
		self.training_images, self.training_labels, self.testing_images, self.testing_labels = load_training_testing_images(Training.labels_dictionary)
		self.image_size = image_size
		self.model = model
		self.epoch = 0
		self.result_file = open(f"./results/{self.model.name}.csv", "w")
		self.result_file.write("epoch,loss,accuracy\n")
	
	def __del__(self):
		self.result_file.close()

	def train(self):
		history = self.model.model.fit(self.training_images, self.training_labels, epochs=1)
		gc.collect()
		loss = history.history["loss"][0]
		acc = history.history["accuracy"][0]
		gc.collect()
		return (loss, acc)
		
	def evaluate(self):
		loss, acc = self.model.model.evaluate(self.testing_images, self.testing_labels)
		results = f"{str(self.epoch)},{loss},{acc}\n"
		self.result_file.write(results)
		gc.collect()
		return (loss, acc)
	