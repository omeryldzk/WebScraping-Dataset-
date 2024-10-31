import scrapy
from university_fees.items import UniversityFeesItem

class UniversityFeesSpider(scrapy.Spider):
    name = "university_fees"
    start_urls = ["https://dogrutercihler.com/vakif-universiteleri-2021-2022-ucretleri/"]

    def parse(self, response):
        for row in response.xpath('//tr[td/span[contains(@style, "color: #ffffff;")]]/following-sibling::tr'):
            item = UniversityFeesItem()

            item['universite'] = row.xpath('td[1]//text()').get().strip()
            bolum_fakulte_raw = row.xpath('td[2]//text()').get().strip()
            ucret_raw = row.xpath('td[3]//text()').get().strip()
            item['ucret'] = int(ucret_raw.replace('.', ''))  # Noktayı kaldır ve integer olarak ata
            item['akademik_yil'] = 2021

            # Burs Oranını Ayıkla ve bolum_fakulte'den çıkar
            if 'Ücretli' in bolum_fakulte_raw:
                item['burs_orani'] = 'Ücretli'
                item['bolum_fakulte'] = bolum_fakulte_raw.replace(' (Ücretli)', '')
            elif '%25 İndirimli' in bolum_fakulte_raw:
                item['burs_orani'] = '%25 İndirimli'
                item['bolum_fakulte'] = bolum_fakulte_raw.replace(' (%25 İndirimli)', '')
            elif '%50 İndirimli' in bolum_fakulte_raw:
                item['burs_orani'] = '%50 İndirimli'
                item['bolum_fakulte'] = bolum_fakulte_raw.replace(' (%50 İndirimli)', '')
            else:
                item['burs_orani'] = 'Ücretli'
                item['bolum_fakulte'] = bolum_fakulte_raw

            yield item
