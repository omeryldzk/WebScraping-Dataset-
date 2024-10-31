import scrapy

class UniversityLinksSpider(scrapy.Spider):
    name = "university_links"
    allowed_domains = ["basarisiralamalari.com"]
    start_urls = ["https://www.basarisiralamalari.com/ozel-universite-ogrenim-egitim-ucretleri/"]  # Replace with the actual main page URL listing universities

    def parse(self, response):
        # Extract all university URLs from the listing page
        university_links = response.xpath('//a[contains(@href, "egitim-ucretleri")]/@href').getall()
        
        for link in university_links:
            # Store each university link for later processing
            yield {'university_url': response.urljoin(link)}
