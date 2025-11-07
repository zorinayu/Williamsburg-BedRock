/**
 * Sample Swift file for testing Interview Code Lens
 * This file demonstrates various Swift features
 */
import Foundation

/**
 * Calculate the sum of an array of numbers
 */
func calculateSum(_ numbers: [Int]) -> Int {
    return numbers.reduce(0, +)
}

/**
 * Process dictionary data and return formatted string
 */
func processData(_ data: [String: Any]) -> String? {
    guard let jsonData = try? JSONSerialization.data(withJSONObject: data, options: .prettyPrinted),
          let jsonString = String(data: jsonData, encoding: .utf8) else {
        return nil
    }
    return jsonString
}

/**
 * Fetch content from URL using async/await
 */
func fetchUrl(_ urlString: String) async throws -> String {
    guard let url = URL(string: urlString) else {
        throw URLError(.badURL)
    }
    
    let (data, _) = try await URLSession.shared.data(from: url)
    guard let string = String(data: data, encoding: .utf8) else {
        throw URLError(.cannotDecodeContentData)
    }
    
    return string
}

/**
 * A class to process various types of data
 */
class DataProcessor {
    private var config: [String: Any]
    
    init(config: [String: Any]) {
        self.config = config
    }
    
    func process() -> String {
        // Process data based on configuration
        return config["output"] as? String ?? "default"
    }
    
    func getConfig() -> [String: Any] {
        return config
    }
    
    // Static method example
    static func createDefault() -> DataProcessor {
        return DataProcessor(config: ["output": "default"])
    }
}

/**
 * Main function for testing
 */
if CommandLine.argc > 0 {
    let numbers = [1, 2, 3, 4, 5]
    let result = calculateSum(numbers)
    print("Sum: \(result)")
}
