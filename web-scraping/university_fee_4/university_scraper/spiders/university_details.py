# university_details/spiders/university_details.py
import scrapy
import csv
from university_scraper.items import UniversityDetailsItem

class UniversityDetailsSpider(scrapy.Spider):
    name = "university_details"
    allowed_domains = ["basarisiralamalari.com"]

    def start_requests(self):
        # Load the URLs from the previously saved CSV file
        with open('university_urls.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            urls = [row['university_url'] for row in reader]  # Assuming the CSV has a column named 'university_url'
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_university)

    def parse_university(self, response):
        # Extract university name
        university_name = response.xpath("//h1/text()").get() or "Unknown University"
        
        # Locate the tuition fees information (e.g., <li> items with department and fee details)
        tuition_data = response.xpath('//ul/li')

        for item in tuition_data:
            # Extract faculty and fee details
            faculty_name = item.xpath('strong/text()').get()
            fee_text = item.xpath('text()').get()

            if faculty_name and fee_text:
                yield {
                    'Üniversite': university_name,
                    'Bölüm/Fakülte': faculty_name.strip(),
                    'Ücret': fee_text.strip(),
                    "Akademik yıl": 2024
                } 