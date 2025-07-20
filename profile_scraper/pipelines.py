import json

class ProfileScraperPipeline:
    def process_item(self, item, spider):
        return item

class JsonExportPipeline:
    def __init__(self):
        self.file = open('scraped_data.json', 'w', encoding='utf-8')
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        json.dump(self.items, self.file, ensure_ascii=False, indent=4)
        self.file.close()


        

# import csv

# class ProfileScraperPipeline:
#     def process_item(self, item, spider):
#         return item

# class CsvExportPipeline:
#     def __init__(self):
#         self.file = open('scraped_data.csv', 'w', newline='', encoding='utf-8')
#         self.writer = csv.writer(self.file)
#         self.writer.writerow(['item_url', 'title', 'sku', 'price', 'category', 'image', 'description'])

#     def process_item(self, item, spider):
#         self.writer.writerow([
#             item.get('item_url', ''),
#             item.get('title', ''),
#             item.get('sku', ''),
#             item.get('price', ''),
#             item.get('category', ''),
#             item.get('image', ''),
#             item.get('description', '')
#         ])
#         return item

#     def close_spider(self, spider):
#         self.file.close()
