import scrapy

class UniversityDetailsItem(scrapy.Item):
    akademik_yil = scrapy.Field()
    bolum_fakulte = scrapy.Field()
    ucret = scrapy.Field()
    universite = scrapy.Field()  # Add this line if `universite` is missing
