import scrapy

class UniversityFeesSpider(scrapy.Spider):
    name = "university_fees_2023"
    start_urls = [
        'https://onedio.com/haber/ozel-universite-fiyatlari-2023-2024-hangi-bolum-ne-kadar-1156735'
    ]

    def parse(self, response):
        # Loop through each university section
        for section in response.xpath("//section[@class='entry entry--image image content-visibility-entry']"):
            # Extract the university name
            university_name = section.xpath(".//h2/text()").get().strip()
            
            # Extract each department and fee
            for item in section.xpath(".//figcaption//li"):
                department = item.xpath(".//p//a/text() | .//p/text()").getall()
                department = ' '.join([text.strip() for text in department if text.strip()])
                fee = item.xpath(".//p/text()").re_first(r'\d+\.?\d* TL')
                
                yield {
                    "Üniversite": university_name,
                    "Bölüm/Fakülte": department,
                    "Ücret": fee,
                    "Akademik yıl": 2023
                }

# To save the data as a CSV, run the command:
# scrapy runspider university_fees_2023_2024.py -o university_fees_2023_2024.csv:csv
