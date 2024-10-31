# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# university_fees/pipelines.py
class UniversityFeesPipeline:
    def process_item(self, item, spider):
        # Ucret alanının doğruluğunu kontrol et
        if isinstance(item['ucret'], int):
            item['ucret'] = "{:,}".format(item['ucret']).replace(',', '.')
        return item
