class IrisFlowerClassifier:
    NEIGHBORS = 1

    def __init__(self):
        self.dataset = self.load_dataset()
        self.model = self.get_trained_model(self.dataset.data, self.dataset.target)

    def load_dataset(self):
        from sklearn.datasets import load_iris
        return load_iris()

    def get_trained_model(self, observation, response):
        knn_classifier = self.get_knn_classifier()
        return knn_classifier.fit(observation, response)

    def classify(self, sepal_length, sepal_width, petal_length, petal_width):
        predictions = self.model.predict([[sepal_length, sepal_width, petal_width, petal_width]])
        return self.get_species_by_index(predictions[0])

    def get_knn_classifier(self):
        from sklearn.neighbors import KNeighborsClassifier
        return KNeighborsClassifier(n_neighbors=self.NEIGHBORS)

    def get_species_by_index(self, index):
        return self.dataset.target_names[index]
