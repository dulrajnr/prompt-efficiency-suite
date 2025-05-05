import os
import pytest
from PIL import Image
import numpy as np

@pytest.fixture(scope="session")
def test_data_dir():
    return os.path.join(os.path.dirname(__file__), "data")

@pytest.fixture(scope="session")
def sample_image(test_data_dir):
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_path = os.path.join(test_data_dir, "sample_image.jpg")
    img.save(img_path)
    return img_path

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_data(test_data_dir):
    yield
    # Clean up test data after all tests
    if os.path.exists(test_data_dir):
        for file in os.listdir(test_data_dir):
            os.remove(os.path.join(test_data_dir, file))
        os.rmdir(test_data_dir) 