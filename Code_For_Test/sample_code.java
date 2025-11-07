/**
 * Sample Java file for testing Interview Code Lens
 * This file demonstrates various Java features
 */
import java.util.*;
import java.util.stream.Collectors;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import com.fasterxml.jackson.databind.ObjectMapper;

public class SampleCode {
    
    /**
     * Calculate the sum of a list of numbers
     */
    public static int calculateSum(List<Integer> numbers) {
        return numbers.stream()
                     .mapToInt(Integer::intValue)
                     .sum();
    }
    
    /**
     * Process map data and return formatted string
     */
    public static String processData(Map<String, Object> data) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            return mapper.writerWithDefaultPrettyPrinter()
                        .writeValueAsString(data);
        } catch (Exception e) {
            return "Error processing data: " + e.getMessage();
        }
    }
    
    /**
     * Fetch content from URL
     */
    public static String fetchUrl(String url) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                                        .uri(URI.create(url))
                                        .build();
        HttpResponse<String> response = client.send(request, 
                                                   HttpResponse.BodyHandlers.ofString());
        return response.body();
    }
    
    /**
     * A class to process various types of data
     */
    public static class DataProcessor {
        private Map<String, Object> config;
        
        public DataProcessor(Map<String, Object> config) {
            this.config = config;
        }
        
        public String process() {
            // Process data based on configuration
            return config.getOrDefault("output", "default").toString();
        }
        
        public Map<String, Object> getConfig() {
            return new HashMap<>(config);
        }
    }
    
    /**
     * Main method for testing
     */
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        int result = calculateSum(numbers);
        System.out.println("Sum: " + result);
    }
}
