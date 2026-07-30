"""Tests for the trained NIDS models."""

import os
import joblib
import numpy as np
import pytest

MODEL_PATH = os.path.join("models", "lightgbm_model.pkl")


@pytest.fixture(scope="module")
def model():
    assert os.path.exists(MODEL_PATH), f"Model not found at {MODEL_PATH}"
    return joblib.load(MODEL_PATH)


def test_model_loads(model):
    """The saved model file loads without errors."""
    assert model is not None


def test_model_has_expected_feature_count(model):
    """The model knows how many features it was trained on."""
    assert getattr(model, "n_features_in_", 0) > 0


def test_model_predicts_on_valid_input(model):
    """The model returns one prediction for one input row."""
    sample = np.zeros((1, model.n_features_in_))
    prediction = model.predict(sample)
    assert prediction.shape == (1,)


def test_scaler_loads_and_transforms(model):
    """The saved scaler loads and outputs the right shape."""
    scaler = joblib.load(os.path.join("models", "scaler.pkl"))
    sample = np.zeros((1, model.n_features_in_))
    scaled = scaler.transform(sample)
    assert scaled.shape == sample.shape
