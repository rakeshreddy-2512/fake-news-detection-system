from pathlib import Path
from typing import Dict, List

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from app.core.config import settings


class ModelService:
    def __init__(self) -> None:
        self.model_path = Path(settings.model_path)
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        self.pipeline = self._load_or_create_model()

    def _bootstrap_dataset(self) -> pd.DataFrame:
        rows = [
            ("Government confirms alien invasion in Nevada", "FAKE"),
            ("Scientists discover miracle cure hidden in soda", "FAKE"),
            ("Central bank releases official inflation report", "REAL"),
            ("Local elections results certified by commission", "REAL"),
            ("Celebrity says the earth is flat again", "FAKE"),
            ("WHO publishes annual global health statistics", "REAL"),
        ]
        return pd.DataFrame(rows, columns=["text", "label"])

    def _load_or_create_model(self) -> Pipeline:
        if self.model_path.exists():
            return joblib.load(self.model_path)

        data = self._bootstrap_dataset()
        pipeline = Pipeline(
            [
                ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2))),
                ("clf", LogisticRegression(max_iter=400)),
            ]
        )
        pipeline.fit(data["text"], data["label"])
        joblib.dump(pipeline, self.model_path)
        return pipeline

    def predict(self, title: str, content: str) -> Dict[str, float]:
        text = f"{title}. {content}"
        probabilities = self.pipeline.predict_proba([text])[0]
        labels = self.pipeline.classes_
        idx = int(np.argmax(probabilities))
        return {
            "label": str(labels[idx]),
            "confidence": float(probabilities[idx]),
        }

    def train(self, dataset_path: str) -> Dict[str, float]:
        dataset = pd.read_csv(dataset_path)
        if "text" not in dataset.columns or "label" not in dataset.columns:
            raise ValueError("Dataset must include text and label columns")

        x_train, x_test, y_train, y_test = train_test_split(
            dataset["text"], dataset["label"], test_size=0.2, random_state=42
        )

        pipeline = Pipeline(
            [
                ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2))),
                ("clf", LogisticRegression(max_iter=700)),
            ]
        )
        pipeline.fit(x_train, y_train)
        score = pipeline.score(x_test, y_test)

        self.pipeline = pipeline
        joblib.dump(self.pipeline, self.model_path)

        return {
            "samples": int(len(dataset)),
            "test_accuracy": float(score),
        }


model_service = ModelService()
