/**
 * Sample Rust file for testing Interview Code Lens
 * This file demonstrates various Rust features
 */
use std::collections::HashMap;
use serde_json::{json, Value};
use reqwest;

/**
 * Calculate the sum of a vector of numbers
 */
fn calculate_sum(numbers: &[i32]) -> i32 {
    numbers.iter().sum()
}

/**
 * Process HashMap data and return formatted string
 */
fn process_data(data: &HashMap<&str, Value>) -> Result<String, serde_json::Error> {
    serde_json::to_string_pretty(data)
}

/**
 * Fetch content from URL
 */
async fn fetch_url(url: &str) -> Result<String, reqwest::Error> {
    let response = reqwest::get(url).await?;
    response.text().await
}

/**
 * A struct to process various types of data
 */
pub struct DataProcessor {
    config: HashMap<String, String>,
}

impl DataProcessor {
    /**
     * Create a new DataProcessor
     */
    pub fn new(config: HashMap<String, String>) -> Self {
        DataProcessor { config }
    }
    
    /**
     * Process data based on configuration
     */
    pub fn process(&self) -> String {
        self.config.get("output")
                   .cloned()
                   .unwrap_or_else(|| "default".to_string())
    }
    
    /**
     * Get configuration
     */
    pub fn get_config(&self) -> &HashMap<String, String> {
        &self.config
    }
}

/**
 * Main function for testing
 */
fn main() {
    let numbers = vec![1, 2, 3, 4, 5];
    let result = calculate_sum(&numbers);
    println!("Sum: {}", result);
}
