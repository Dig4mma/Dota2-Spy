# scrapers/base_scraper.py

from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def get_data(self, data_type):
        pass

    @abstractmethod
    def parse_data(self, html_content, data_type):
        pass