# university_fees/items.py
import scrapy

class UniversityFeesItem(scrapy.Item):
    universite = scrapy.Field()
    bolum_fakulte = scrapy.Field()
    ucret = scrapy.Field()
    akademik_yil = scrapy.Field()
    burs_orani = scrapy.Field()  # Yeni alan
