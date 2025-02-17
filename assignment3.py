import argparse
import csv
import re
import urllib.request
from collections import defaultdict, Counter
from datetime import datetime

# Function to download file from the given URL
def download_file(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8').splitlines()

# Function to process log file and extract relevant data
def process_log_file(lines):
    data = []
    for line in csv.reader(lines):
        data.append({
            'path': line[0],
            'datetime': line[1],
            'browser': line[2],
            'status': line[3],
            'size': line[4]
        })
    return data

# Function to find image hits and calculate percentage
def find_image_hits(data):
    image_pattern = re.compile(r'.*\.(jpg|gif|png)$', re.IGNORECASE)
    image_hits = [entry for entry in data if image_pattern.match(entry['path'])]
    percentage = (len(image_hits) / len(data)) * 100 if data else 0
    print(f"Image requests account for {percentage:.1f}% of all requests")

# Function to find the most popular browser used
def find_most_popular_browser(data):
    browser_pattern = re.compile(r'(Firefox|Chrome|Safari|MSIE)')
    browser_counts = Counter()
    
    for entry in data:
        match = browser_pattern.search(entry['browser'])
        if match:
            browser_counts[match.group(1)] += 1
    
    most_popular = browser_counts.most_common(1)
    if most_popular:
        print(f"Most popular browser: {most_popular[0][0]}")
    else:
        print("No browser data available.")

# Function to count hits per hour and sort them
def count_hits_per_hour(data):
    hour_counts = defaultdict(int)
    for entry in data:
        hour = datetime.strptime(entry['datetime'], "%m/%d/%Y %H:%M:%S").hour
        hour_counts[hour] += 1
    
    for hour, count in sorted(hour_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"Hour {hour:02} has {count} hits")

# Main function to execute the script
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='URL of the log file')
    args = parser.parse_args()
    
    lines = download_file(args.url)  # Download file
    data = process_log_file(lines)  # Process file
    find_image_hits(data)  # Find image hits
    find_most_popular_browser(data)  # Find most popular browser
    count_hits_per_hour(data)  # Count hits per hour

if __name__ == "__main__":
    main()
