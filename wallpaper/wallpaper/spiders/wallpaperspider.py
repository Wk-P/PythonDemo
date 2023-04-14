import scrapy, os

class WallpaperSpider(scrapy.Spider):
    name = 'wallpaperspider'
    allowed_domains = ['wallhaven.cc']
    start_urls = [
        'https://wallhaven.cc/latest?page=2',
    ]

    def __init__(self):
        self.image_file_path = './images/'
        if not os.path.exists(self.image_file_path):
            os.makedirs(self.image_file_path)

    def parse(self, response):
        image_paths = response.css("div.thumb-info a.jsAnchor.thumb-tags-toggle.tagged::attr('data-href')").getall()
        images = []
        for image_path in image_paths:
            images.append({"image_code": image_path.split('/')[-1], "image_path": image_path})

        # 从源地址下载图片
        for image in images:
            yield scrapy.Request(
                url=image['image_path'], 
                callback=self.parse_image_details_url,
                meta={'image_code': image['image_code']},
            )

    def parse_image_details_url(self, response):
        image_src = response.css("div.scrollbox img#wallpaper::attr('src')").get()
        print("image_src:", image_src)
        yield scrapy.Request(url=image_src, callback=self.parse_download_image, meta={'image_code': response.meta['image_code']})

    def parse_download_image(self, response):
        image_name = response.meta['image_code'] + '.jpg'
        with open(file=self.image_file_path + image_name, mode='wb') as img:
            img.write(response.body)
            print(f"下载图片{image_name}成功!")

        