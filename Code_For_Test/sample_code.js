/**
 * Sample JavaScript file for testing Interview Code Lens
 * This file demonstrates various JavaScript features
 */

// Calculate the sum of an array of numbers
function calculateSum(numbers) {
    return numbers.reduce((sum, num) => sum + num, 0);
}

// Process object data and return formatted string
function processData(data) {
    return JSON.stringify(data, null, 2);
}

// Fetch content from URL using async/await
async function fetchUrl(url) {
    const response = await fetch(url);
    return await response.text();
}

// Class to process various types of data
class DataProcessor {
    constructor(config) {
        this.config = config;
    }
    
    process() {
        // Process data based on configuration
        return this.config.output || 'default';
    }
    
    // Static method example
    static createDefault() {
        return new DataProcessor({ output: 'default' });
    }
}

// Arrow function example
const multiply = (a, b) => a * b;

// Module export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        calculateSum,
        processData,
        fetchUrl,
        DataProcessor,
        multiply
    };
}

// Example usage
if (require.main === module) {
    const numbers = [1, 2, 3, 4, 5];
    const result = calculateSum(numbers);
    console.log(`Sum: ${result}`);
}
