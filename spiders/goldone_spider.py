import scrapy

class GoldoneSpider(scrapy.Spider):
    name = 'goldone_spider'
    allowed_domains = ['goldonecomputer.com']
    start_urls = ['https://www.goldonecomputer.com/']

    def parse(self, response):
        category_names = response.css('li.top_level.dropdown > a.activSub::text').getall()
        category_links = response.css('li.top_level.dropdown > a.activSub::attr(href)').getall()

        for name, link in zip(category_names, category_links):
            # Follow each category link
            yield response.follow(link, callback=self.parse_category, meta={'category_name': name.strip()})

    def parse_category(self, response):
        category_name = response.meta['category_name']

        products = []
        for product in response.css('div.product-block'):
            product_name = product.css('div.product-details h4 a::text').get()
            if not product_name:
                product_name = product.css('div.caption h4 a::text').get()
            product_name = product_name.strip() if product_name else 'No Product Name'

            rating_count = product.css('div.rating .fa-star-o').getall()
            rating_number = len(rating_count)

            price_old = product.css('div.product-details p.price span.price-old::text').get()
            price_old = price_old.strip() if price_old else 'No Old Price'

            price_new = product.css('div.product-details p.price span.price-new::text').get()
            if not price_new:
                price_new = product.css('div.caption p.price::text').get()
            price_new = price_new.strip() if price_new else 'No Price'

            product_image = product.css('div.image img::attr(src)').get()

            products.append({
                'product_name': product_name,
                'rating_count': rating_number,
                'price_old': price_old,
                'price_new': price_new,
                'product_image': product_image
            })

        # Yield data structured by category
        yield {
            'category_name': category_name,
            'products': products
        }

        #  handle pagination if category pages have multiple pages
        next_page = response.css('ul.pagination li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category, meta={'category_name': category_name})
