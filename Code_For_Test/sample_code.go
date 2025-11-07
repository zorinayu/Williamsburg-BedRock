/**
 * Sample Go file for testing Interview Code Lens
 * This file demonstrates various Go features
 */
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

/**
 * Calculate the sum of a slice of numbers
 */
func calculateSum(numbers []int) int {
	sum := 0
	for _, num := range numbers {
		sum += num
	}
	return sum
}

/**
 * Process map data and return formatted string
 */
func processData(data map[string]interface{}) (string, error) {
	jsonBytes, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		return "", err
	}
	return string(jsonBytes), nil
}

/**
 * Fetch content from URL
 */
func fetchUrl(url string) (string, error) {
	resp, err := http.Get(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	
	return string(body), nil
}

/**
 * A struct to process various types of data
 */
type DataProcessor struct {
	config map[string]interface{}
}

/**
 * Create a new DataProcessor
 */
func NewDataProcessor(config map[string]interface{}) *DataProcessor {
	return &DataProcessor{config: config}
}

/**
 * Process data based on configuration
 */
func (dp *DataProcessor) Process() string {
	if output, ok := dp.config["output"].(string); ok {
		return output
	}
	return "default"
}

/**
 * Get configuration
 */
func (dp *DataProcessor) GetConfig() map[string]interface{} {
	return dp.config
}

/**
 * Main function for testing
 */
func main() {
	numbers := []int{1, 2, 3, 4, 5}
	result := calculateSum(numbers)
	fmt.Printf("Sum: %d\n", result)
}
