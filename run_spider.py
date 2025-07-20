import subprocess
import time
from error_logger import error_logger

def run_spider():
    while True:
        try:
            # Run the Scrapy spider
            subprocess.run(['scrapy', 'crawl', 'profileeducation'], check=True)
        except subprocess.CalledProcessError as e:
            error_logger.error(f"Spider encountered an error: {e}")
        # Wait for a specified interval before restarting the spider
        time.sleep(60)  # Wait for 60 seconds before restarting

if __name__ == "__main__":
    run_spider()