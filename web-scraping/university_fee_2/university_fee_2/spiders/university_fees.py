import scrapy

class UniversityFeesSpider(scrapy.Spider):
    name = "university_fees"
    start_urls = [
        'https://onedio.com/haber/2022-2023-ozel-universite-ucretleri-ne-kadar-iste-vakif-universitelerindeki-bolumlerin-ucretleri-1083203'
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
                    "Akademik yıl": 2022
                }

# Save the data as a CSV by running the command:
# scrapy runspider university_fees.py -o university_fees.csv -t csv
