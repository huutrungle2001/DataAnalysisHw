from yonex_footwear.items import YonexFootwearItem
import scrapy


class YonexFootwearSpiderSpider(scrapy.Spider):
    name = "yonex_footwear_spider"
    allowed_domains = ["www.yonex.com"]
    
    def start_requests(self):
        # Generate URLs for pages 1 to 5
        base_url = "https://www.yonex.com/badminton/footwear?p={}"
        for page in range(1, 6):  # Crawling pages 1 to 5
            yield scrapy.Request(url=base_url.format(page), callback=self.parse_list_page)

    def parse_list_page(self, response):
        """Extract product links and send requests to product pages"""
        product_links = response.css(
            "div.product-item-info a.product-item-link::attr(href)").getall()

        for link in product_links:
            yield scrapy.Request(url=link, callback=self.parse_product_page)

    def parse_product_page(self, response):
        """Extract detailed product information"""

        item = YonexFootwearItem()

        # Extract product name
        item["product_name"] = response.css(
            "span.base[data-ui-id='page-title-wrapper']::text").get(default="").strip()

        # Extract product attributes from the table
        attributes = {}
        for row in response.css("table#product-attribute-specs-table tr"):
            key = row.css("th::text").get(default="").strip()
            value = row.css("td::text").get(default="").strip()
            if key and value:
                attributes[key] = value

        item["product_attributes"] = attributes
        item["product_link"] = response.url

        yield item