"""
Sample Python file for testing Interview Code Lens
This file demonstrates various Python features
"""
import os
import json
from typing import List, Dict
import requests


def calculate_sum(numbers: List[int]) -> int:
    """Calculate the sum of a list of numbers"""
    return sum(numbers)


def process_data(data: Dict) -> str:
    """Process dictionary data and return formatted string"""
    return json.dumps(data, indent=2)


def fetch_url(url: str) -> str:
    # Fetch content from URL
    response = requests.get(url)
    return response.text


class DataProcessor:
    """A class to process various types of data"""
    
    def __init__(self, config: Dict):
        self.config = config
    
    def process(self):
        """Process data based on configuration"""
        return self.config.get('output', 'default')


if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    result = calculate_sum(numbers)
    print(f"Sum: {result}")

