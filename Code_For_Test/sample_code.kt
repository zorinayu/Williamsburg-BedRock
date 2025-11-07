/**
 * Sample Kotlin file for testing Interview Code Lens
 * This file demonstrates various Kotlin features
 */
package sample

import kotlinx.coroutines.*
import java.net.URL
import com.google.gson.GsonBuilder

/**
 * Calculate the sum of a list of numbers
 */
fun calculateSum(numbers: List<Int>): Int {
    return numbers.sum()
}

/**
 * Process map data and return formatted string
 */
fun processData(data: Map<String, Any>): String {
    val gson = GsonBuilder().setPrettyPrinting().create()
    return gson.toJson(data)
}

/**
 * Fetch content from URL using coroutines
 */
suspend fun fetchUrl(url: String): String {
    return withContext(Dispatchers.IO) {
        URL(url).readText()
    }
}

/**
 * A class to process various types of data
 */
class DataProcessor(private val config: Map<String, Any>) {
    
    /**
     * Process data based on configuration
     */
    fun process(): String {
        return config["output"] as? String ?: "default"
    }
    
    /**
     * Get configuration
     */
    fun getConfig(): Map<String, Any> {
        return config.toMap()
    }
    
    companion object {
        /**
         * Create default instance
         */
        fun createDefault(): DataProcessor {
            return DataProcessor(mapOf("output" to "default"))
        }
    }
}

/**
 * Main function for testing
 */
fun main() {
    val numbers = listOf(1, 2, 3, 4, 5)
    val result = calculateSum(numbers)
    println("Sum: $result")
}
