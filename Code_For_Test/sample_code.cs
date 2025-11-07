/**
 * Sample C# file for testing Interview Code Lens
 * This file demonstrates various C# features
 */
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

namespace SampleCode
{
    /**
     * Main class with utility methods
     */
    public class Program
    {
        /**
         * Calculate the sum of a list of numbers
         */
        public static int CalculateSum(List<int> numbers)
        {
            return numbers.Sum();
        }
        
        /**
         * Process dictionary data and return formatted string
         */
        public static string ProcessData(Dictionary<string, object> data)
        {
            var options = new JsonSerializerOptions
            {
                WriteIndented = true
            };
            return JsonSerializer.Serialize(data, options);
        }
        
        /**
         * Fetch content from URL using async/await
         */
        public static async Task<string> FetchUrl(string url)
        {
            using (var client = new HttpClient())
            {
                return await client.GetStringAsync(url);
            }
        }
        
        /**
         * Main method for testing
         */
        public static void Main(string[] args)
        {
            var numbers = new List<int> { 1, 2, 3, 4, 5 };
            var result = CalculateSum(numbers);
            Console.WriteLine($"Sum: {result}");
        }
    }
    
    /**
     * A class to process various types of data
     */
    public class DataProcessor
    {
        private Dictionary<string, object> config;
        
        public DataProcessor(Dictionary<string, object> config)
        {
            this.config = config;
        }
        
        public string Process()
        {
            // Process data based on configuration
            return config.ContainsKey("output") 
                ? config["output"].ToString() 
                : "default";
        }
        
        public Dictionary<string, object> GetConfig()
        {
            return new Dictionary<string, object>(config);
        }
    }
}
