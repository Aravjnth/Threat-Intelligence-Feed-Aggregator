import requests
import json
import pandas as pd
from datetime import datetime
import re

class ThreatIntelligenceFeedAggregator:
    def __init__(self):
        self.feeds = {
            "OpenPhish": "https://openphish.com/feed.txt",
            "PhishTank": "https://www.phishtank.com/phish_search.php?active=y&valid=y&Search=Search",
            "URLhaus": "https://urlhaus.abuse.ch/downloads/urlhaus",
            "MalwareDomainList": "https://www.malwaredomainlist.com/hostslist/hosts.txt"
        }
        self.data = []

    def fetch_feeds(self):
        for feed, url in self.feeds.items():
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for bad status codes
                self.parse_feed(feed, response.text)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {feed} feed: {e}")

    def parse_feed(self, feed, data):
        try:
            if feed == "OpenPhish":
                for line in data.splitlines():
                    url, _, _ = line.split(",")
                    self.data.append({"feed": feed, "url": url, "timestamp": datetime.now()})
            elif feed == "PhishTank":
                pattern = r'<td>(https?://[^\s]+)</td>'
                urls = re.findall(pattern, data)
                for url in urls:
                    self.data.append({"feed": feed, "url": url, "timestamp": datetime.now()})
            elif feed == "URLhaus":
                for line in data.splitlines():
                    url, _, _ = line.split(",")
                    self.data.append({"feed": feed, "url": url, "timestamp": datetime.now()})
            elif feed == "MalwareDomainList":
                for line in data.splitlines():
                    url = line.strip()
                    self.data.append({"feed": feed, "url": url, "timestamp": datetime.now()})
        except Exception as e:
            print(f"Error parsing {feed} feed: {e}")

    def aggregate_data(self):
        try:
            df = pd.DataFrame(self.data)
            df.to_csv("threat_intelligence_feed_aggregator.csv", index=False)
        except Exception as e:
            print(f"Error aggregating data: {e}")

if __name__ == "__main__":
    aggregator = ThreatIntelligenceFeedAggregator()
    aggregator.fetch_feeds()
    aggregator.aggregate_data()