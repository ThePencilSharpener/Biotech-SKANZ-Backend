# Import necessary libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

import joblib
import os

# Paths to saved model files
MODEL_PATH = 'models_weights/science_model.joblib'
VECTORIZER_PATH = 'models_weights/science_vectorizer.joblib'
DTREE_PATH = 'models_weights/science_decision_tree.joblib'


class ScienceQuestionModel:
    """A class to represent the Science Question Classifier Model."""

    _instance = None

    def __init__(self):
        self.model = None
        self.dt = None
        self.vectorizer = TfidfVectorizer()
        self.features = None  # Will hold the feature names after vectorization
        self.target = 'topic'
        self.df = pd.read_parquet('traincleaned_file.parquet')  # <-- Load your cleaned parquet file

    def _clean(self):
        """Prepare data for training."""
        # Only keep 'question' and 'topic' columns (should already be clean)
        self.df = self.df[['question', 'topic']]

    def _train(self):
        """Train the classification model."""
        X_text = self.df['question']
        y = self.df['topic']

        # Vectorize the questions
        X = self.vectorizer.fit_transform(X_text)
        self.features = self.vectorizer.get_feature_names_out()

        # Train the logistic regression model
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X, y)

        # Also train a decision tree to get feature importances
        self.dt = DecisionTreeClassifier()
        self.dt.fit(X, y)

    @classmethod
    def get_instance(cls):
        """Gets and builds the singleton instance of the ScienceQuestionModel."""
        if cls._instance is None:
            cls._instance = cls()

            # Load if all saved model files exist
            if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH) and os.path.exists(DTREE_PATH):
                cls._instance.model = joblib.load(MODEL_PATH)
                cls._instance.vectorizer = joblib.load(VECTORIZER_PATH)
                cls._instance.dt = joblib.load(DTREE_PATH)
                cls._instance.features = cls._instance.vectorizer.get_feature_names_out()
            else:
                # First-time run: clean, train, save
                cls._instance._clean()
                cls._instance._train()

                # Save trained objects to disk
                joblib.dump(cls._instance.model, MODEL_PATH)
                joblib.dump(cls._instance.vectorizer, VECTORIZER_PATH)
                joblib.dump(cls._instance.dt, DTREE_PATH)

        return cls._instance

    def predict(self, question):
        """Predict the topic of a given question.

        Args:
            question (str): The question text.

        Returns:
            dict: Probabilities for each topic.
        """
        question_vec = self.vectorizer.transform([question])
        proba = self.model.predict_proba(question_vec)[0]
        classes = self.model.classes_
        # Create a dictionary of topic probabilities
        predictions = dict(zip(classes, proba))
        
        # Get the topic with the highest probability
        predicted_topic = max(predictions, key=predictions.get)
        return {
        "predicted_topic": predicted_topic,
        "probabilities": predictions
    }

    def feature_weights(self):
        """Get feature importances from the decision tree.

        Returns:
            dict: Feature names with their importance scores.
        """
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)}

def initScienceModel():
    """Initialize the Science Question Model."""
    ScienceQuestionModel.get_instance()

def testScienceModel():
    """Test the Science Question Model."""
    print(" Step 1:  Define a sample science question for prediction: ")
    question = "Which solution contains a greater number of blue particles per unit volume?"
    print("\t", question)
    print()

    model = ScienceQuestionModel.get_instance()

    print(" Step 2:", model.get_instance.__doc__)
    
    print(" Step 3:", model.predict.__doc__)
    prediction = model.predict(question)

    # 🔥 First, print the predicted topic:
    print(f"Predicted Topic: {prediction['predicted_topic']}")
    print()

    # 🔥 Then, loop over the probabilities:
    print("Topic Probabilities:")
    for topic, prob in prediction['probabilities'].items():
        print(f'\t {topic}: {prob:.2%}')
    print()


if __name__ == "__main__":
    print(" Begin:", testScienceModel.__doc__)
    testScienceModel()
