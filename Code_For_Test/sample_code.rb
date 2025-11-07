# Sample Ruby file for testing Interview Code Lens
# This file demonstrates various Ruby features

require 'json'
require 'net/http'
require 'uri'

# Calculate the sum of an array of numbers
def calculate_sum(numbers)
  numbers.sum
end

# Process hash data and return formatted string
def process_data(data)
  JSON.pretty_generate(data)
end

# Fetch content from URL
def fetch_url(url)
  uri = URI(url)
  response = Net::HTTP.get_response(uri)
  response.body
end

# A class to process various types of data
class DataProcessor
  attr_reader :config
  
  def initialize(config)
    @config = config
  end
  
  def process
    # Process data based on configuration
    @config[:output] || @config['output'] || 'default'
  end
  
  def get_config
    @config.dup
  end
  
  # Class method example
  def self.create_default
    new({ output: 'default' })
  end
end

# Example usage
if __FILE__ == $0
  numbers = [1, 2, 3, 4, 5]
  result = calculate_sum(numbers)
  puts "Sum: #{result}"
end
