# university_fees/spiders/university_fees.py
import scrapy

class UniversityFeesSpider(scrapy.Spider):
    name = "university_fees"
    start_urls = ["https://dogrutercihler.com/vakif-universiteleri-2021-2022-ucretleri/"]

    def parse(self, response):
        for row in response.xpath('//tr[td/span[contains(@style, "color: #ffffff;")]]/following-sibling::tr'):
            university = row.xpath('td[1]//text()').get().strip()
            department = row.xpath('td[2]//text()').get().strip()
            fee = row.xpath('td[3]//text()').get().strip()

            yield {
                "Üniversite": university,
                "Bölüm/Fakülte": department,
                "Ücret": fee,
                "Akademik yıl": 2021
            }
