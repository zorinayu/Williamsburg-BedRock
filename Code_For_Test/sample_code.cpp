/**
 * Sample C++ file for testing Interview Code Lens
 * This file demonstrates various C++ features
 */
#include <iostream>
#include <vector>
#include <numeric>
#include <map>
#include <string>
#include <curl/curl.h>
#include <json/json.h>

using namespace std;

/**
 * Calculate the sum of a vector of numbers
 */
int calculateSum(const vector<int>& numbers) {
    return accumulate(numbers.begin(), numbers.end(), 0);
}

/**
 * Process map data and return formatted string
 */
string processData(const map<string, string>& data) {
    Json::Value root;
    for (const auto& pair : data) {
        root[pair.first] = pair.second;
    }
    
    Json::StreamWriterBuilder builder;
    builder["indentation"] = "  ";
    return Json::writeString(builder, root);
}

/**
 * Fetch content from URL using libcurl
 */
string fetchUrl(const string& url) {
    CURL* curl = curl_easy_init();
    string response;
    
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, 
                        [](void* contents, size_t size, size_t nmemb, string* data) {
                            data->append((char*)contents, size * nmemb);
                            return size * nmemb;
                        });
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
    
    return response;
}

/**
 * A class to process various types of data
 */
class DataProcessor {
private:
    map<string, string> config;
    
public:
    DataProcessor(const map<string, string>& config) : config(config) {}
    
    string process() {
        // Process data based on configuration
        auto it = config.find("output");
        return (it != config.end()) ? it->second : "default";
    }
    
    map<string, string> getConfig() const {
        return config;
    }
};

/**
 * Main function for testing
 */
int main() {
    vector<int> numbers = {1, 2, 3, 4, 5};
    int result = calculateSum(numbers);
    cout << "Sum: " << result << endl;
    
    return 0;
}
