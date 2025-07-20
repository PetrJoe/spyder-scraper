# -*- coding: utf-8 -*-
import scrapy
import re
from profile_scraper.items import ProfileEducationItem

class ProfileEducationSpider(scrapy.Spider):
    name = 'profileeducation'
    allowed_domains = ['profile-education.co.uk']
    start_urls = ['https://www.profile-education.co.uk']

    custom_settings = {
        'USER_AGENT': 'my-app/0.0.1',
        'HTTPERROR_ALLOWED_CODES': [404]
    }

    def start_requests(self):
        """Initiates requests to various category pages."""
        headers = {
            "origin": "https://www.profile-education.co.uk",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }

        category_urls = [
            "https://www.profile-education.co.uk/clearance-view-all/page/1/",
            "https://www.profile-education.co.uk/early-years-view-all/page/1/",
            "https://www.profile-education.co.uk/furniture-view-all/page/1/",
            "https://www.profile-education.co.uk/outdoor-view-all/page/1/",
            "https://www.profile-education.co.uk/winther-view-all/page/1/",
            "https://www.profile-education.co.uk/gonge-view-all/page/1/",
            "https://www.profile-education.co.uk/stationery-view-all/page/1/",
            "https://www.profile-education.co.uk/sen-trade-view-all/page/1/",
        ]

        for url in category_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        """Parse the first page and determine total pages for pagination."""
        try:
            total_items = int(re.search(r'(\d+)\s+Items', response.text).group(1))
            total_pages = round(total_items / 16)
        except Exception as e:
            self.logger.warning(f"Failed to parse total items on {response.url}: {e}")
            return

        base_url = response.url.replace("/1/", "").strip()
        for page in range(1, total_pages + 1):
            paginated_url = f"{base_url}/{page}/"
            yield scrapy.Request(url=paginated_url, callback=self.parse_listing, dont_filter=True)

    def parse_listing(self, response):
        """Parse individual product URLs from a listing page."""
        product_urls = response.xpath('//*[@class="prd-list-cell"]//span//a/@href').extract()
        for relative_url in product_urls:
            full_url = response.urljoin(relative_url)
            yield scrapy.Request(url=full_url, callback=self.parse_product)

    def parse_product(self, response):
        """Extract product details from product page."""
        item = ProfileEducationItem()

        item['item_url'] = response.url
        item['title'] = response.xpath('//*[@id="product_details"]//h1//text()').get(default='').strip()
        item['sku'] = response.xpath("//*[contains(text(),'Product Code')]/../span/text()").get(default='').strip()
        item['price'] = response.xpath('//*[@id="price_selling"]//text()').get(default='').strip()

        category = response.xpath('//*[@itemprop="name"]//text()').extract()
        item['category'] = category[1].strip() if len(category) > 1 else ''

        image_url = response.xpath('//*[@id="image"]//img/@src').get(default='').strip()
        image_url = re.sub(r'\?as=0(&h=100&w=100)?', '', image_url)
        item['image'] = response.urljoin(image_url) if image_url else ''

        description = response.xpath('//*[@id="product_tabs-0"]//text()').extract()
        item['description'] = '\n\n'.join([d.strip() for d in description if d.strip()])

        yield item

    def close(self, spider, reason):
        """Run export and notify logic when crawl ends."""
        self.logger.info("Spider closed: running export and email...")
        # Implement Export_CSV and sendEmail functions or import them
        # Export_CSV(_name=self.name)
        # sendEmail(_name=self.name)