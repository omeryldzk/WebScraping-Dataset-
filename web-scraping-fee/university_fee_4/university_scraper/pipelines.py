# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import re

class UniversityScraperPipeline:
    def process_item(self, item, spider):
        # Convert fields to strings if they are not already to avoid errors
        universite = str(item.get('Üniversite', ''))
        ucret = str(item.get('Ücret', ''))
        
        # Extract and clean the university name
        item['universite'] = re.sub(r' Eğitim Ücretleri.*', '', universite).strip()
        
        # Extract scholarship rate (burs_orani) from 'Ücret' field
        burs_orani_match = re.search(r'%\d+ indirimli', ucret)
        item['burs_orani'] = burs_orani_match.group(0) if burs_orani_match else "None"
        
        # Extract tuition fee (ucret) from 'Ücret' field
        ucret_match = re.search(r'(\d+[\.,]?\d*) TL', ucret)
        item['ucret'] = ucret_match.group(0) if ucret_match else "None"
        
        # Keep the akademik_yil and bolum_fakulte fields as they are
        item['akademik_yil'] = item.get('Akademik yıl', 'Unknown')
        item['bolum_fakulte'] = item.get('Bölüm/Fakülte', 'Unknown')
        
        # Remove original keys if not needed for saving to the output
        item.pop('Üniversite', None)
        item.pop('Ücret', None)
        item.pop('Akademik yıl', None)
        item.pop('Bölüm/Fakülte', None)
        
        return item
