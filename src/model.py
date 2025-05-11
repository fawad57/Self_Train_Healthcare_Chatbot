from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import preprocessing
import pandas as pd
import numpy as np

class DiseasePredictor:
    """Predicts diseases using a decision tree classifier trained on symptom data."""
    def __init__(self):
        """Initialize the classifier, encoder, and data attributes."""
        self.model = DecisionTreeClassifier(random_state=42)  # Decision tree with fixed seed
        self.label_encoder = preprocessing.LabelEncoder()     # Encoder for disease labels
        self.feature_names = None  # Symptom feature names
        self.X_train = None        # Training features
        self.X_test = None         # Testing features
        self.y_train = None        # Training labels
        self.y_test = None         # Testing labels
        self.y_pred = None         # Predicted labels

    def train(self, X, y):
        """Train the model and evaluate with cross-validation.
        Args:
            X (pandas.DataFrame): Symptom features (binary).
            y (pandas.Series): Disease labels (strings).
        Returns:
            dict: Evaluation metrics (cross-validation score).
        """
        self.feature_names = X.columns  # Store symptom names
        self.label_encoder.fit(y)       # Fit encoder to disease labels
        y_encoded = self.label_encoder.transform(y)  # Convert labels to integers
        # Split data into training and testing sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y_encoded, test_size=0.33, random_state=42
        )
        self.model.fit(self.X_train, self.y_train)  # Train decision tree
        self.y_pred = self.model.predict(self.X_test)  # Predict on test set
        # Evaluate with 3-fold cross-validation
        scores = cross_val_score(self.model, self.X_test, self.y_test, cv=3)
        metrics = {
            'cross_val_score': scores.mean()  # Average cross-validation score
        }
        return metrics

    def predict(self, symptoms_exp):
        """Predict disease from a list of symptoms.
        Args:
            symptoms_exp (list): List of symptom strings.
        Returns:
            str: Predicted disease name.
        """
        # Create binary input vector (1 for present symptoms, 0 otherwise)
        input_vector = np.zeros(len(self.feature_names))
        for item in symptoms_exp:
            if item in self.feature_names:
                input_vector[list(self.feature_names).index(item)] = 1
        # Convert to DataFrame for prediction
        input_df = pd.DataFrame([input_vector], columns=self.feature_names)
        prediction = self.model.predict(input_df)[0]  # Predict encoded label
        # Decode to disease name
        return self.label_encoder.inverse_transform([prediction])[0]

    def get_feature_names(self):
        """Return the list of symptom feature names.
        Returns:
            list: Symptom names from training data.
        """
        return self.feature_names

    def print_disease(self, node):
        """Decode disease names from decision tree node values.
        Args:
            node: Node value array from decision tree.
        Returns:
            list: Decoded disease names.
        """
        node = node[0]
        val = node.nonzero()  # Get indices of non-zero values
        disease = self.label_encoder.inverse_transform(val[0])  # Decode to names
        return list(map(lambda x: x.strip(), list(disease)))