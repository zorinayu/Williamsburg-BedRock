/**
 * Sample TypeScript file for testing Interview Code Lens
 * This file demonstrates various TypeScript features
 */

// Type definitions
interface Config {
    output?: string;
    [key: string]: any;
}

type NumberArray = number[];

/**
 * Calculate the sum of an array of numbers
 */
function calculateSum(numbers: NumberArray): number {
    return numbers.reduce((sum, num) => sum + num, 0);
}

/**
 * Process object data and return formatted string
 */
function processData<T extends Record<string, any>>(data: T): string {
    return JSON.stringify(data, null, 2);
}

/**
 * Fetch content from URL using async/await
 */
async function fetchUrl(url: string): Promise<string> {
    const response = await fetch(url);
    return await response.text();
}

/**
 * Class to process various types of data
 */
class DataProcessor {
    private config: Config;
    
    constructor(config: Config) {
        this.config = config;
    }
    
    process(): string {
        // Process data based on configuration
        return this.config.output || 'default';
    }
    
    getConfig(): Config {
        return { ...this.config };
    }
    
    // Static method example
    static createDefault(): DataProcessor {
        return new DataProcessor({ output: 'default' });
    }
}

// Generic function example
function multiply<T extends number>(a: T, b: T): T {
    return (a * b) as T;
}

// Example usage
if (require.main === module) {
    const numbers: NumberArray = [1, 2, 3, 4, 5];
    const result = calculateSum(numbers);
    console.log(`Sum: ${result}`);
}

export {
    calculateSum,
    processData,
    fetchUrl,
    DataProcessor,
    multiply,
    Config,
    NumberArray
};
