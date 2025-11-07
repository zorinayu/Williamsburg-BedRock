/**
 * Sample C file for testing Interview Code Lens
 * This file demonstrates various C features
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

/**
 * Structure to hold response data
 */
struct MemoryStruct {
    char *memory;
    size_t size;
};

/**
 * Calculate the sum of an array of numbers
 */
int calculate_sum(int numbers[], int length) {
    int sum = 0;
    for (int i = 0; i < length; i++) {
        sum += numbers[i];
    }
    return sum;
}

/**
 * Process data structure and return formatted string
 */
char* process_data(const char* key, const char* value) {
    int len = strlen(key) + strlen(value) + 20;
    char* result = (char*)malloc(len * sizeof(char));
    snprintf(result, len, "{\"%s\": \"%s\"}", key, value);
    return result;
}

/**
 * Callback function for curl write
 */
static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *)userp;
    
    char *ptr = realloc(mem->memory, mem->size + realsize + 1);
    if (!ptr) {
        return 0;
    }
    
    mem->memory = ptr;
    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;
    
    return realsize;
}

/**
 * Fetch content from URL
 */
char* fetch_url(const char* url) {
    CURL *curl;
    CURLcode res;
    struct MemoryStruct chunk;
    
    chunk.memory = malloc(1);
    chunk.size = 0;
    
    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
    
    return chunk.memory;
}

/**
 * A structure to process various types of data
 */
typedef struct {
    char* output;
} DataProcessor;

/**
 * Create a new DataProcessor
 */
DataProcessor* create_data_processor(const char* output) {
    DataProcessor* dp = (DataProcessor*)malloc(sizeof(DataProcessor));
    dp->output = strdup(output);
    return dp;
}

/**
 * Process data based on configuration
 */
const char* process(DataProcessor* dp) {
    return dp->output ? dp->output : "default";
}

/**
 * Free DataProcessor memory
 */
void free_data_processor(DataProcessor* dp) {
    if (dp) {
        free(dp->output);
        free(dp);
    }
}

/**
 * Main function for testing
 */
int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int length = sizeof(numbers) / sizeof(numbers[0]);
    int result = calculate_sum(numbers, length);
    printf("Sum: %d\n", result);
    
    return 0;
}

