<?php
/**
 * Sample PHP file for testing Interview Code Lens
 * This file demonstrates various PHP features
 */

/**
 * Calculate the sum of an array of numbers
 */
function calculateSum(array $numbers): int {
    return array_sum($numbers);
}

/**
 * Process array data and return formatted string
 */
function processData(array $data): string {
    return json_encode($data, JSON_PRETTY_PRINT);
}

/**
 * Fetch content from URL
 */
function fetchUrl(string $url): string {
    return file_get_contents($url);
}

/**
 * A class to process various types of data
 */
class DataProcessor {
    private $config;
    
    /**
     * Constructor
     */
    public function __construct(array $config) {
        $this->config = $config;
    }
    
    /**
     * Process data based on configuration
     */
    public function process(): string {
        return $this->config['output'] ?? 'default';
    }
    
    /**
     * Get configuration
     */
    public function getConfig(): array {
        return $this->config;
    }
    
    /**
     * Static method to create default instance
     */
    public static function createDefault(): DataProcessor {
        return new self(['output' => 'default']);
    }
}

// Example usage
if (php_sapi_name() === 'cli') {
    $numbers = [1, 2, 3, 4, 5];
    $result = calculateSum($numbers);
    echo "Sum: $result\n";
}
?>
