import scrapy, os

class WallpaperSpider(scrapy.Spider):
    name = 'wallpaperspider'
    allowed_domains = ['wallhaven.cc']
    start_urls = [
        'https://wallhaven.cc/latest?page=2',
    ]

    custom_settings = {
        'DOWNLOAD_DALEY': 3,
        'CONCURRENT_REQUESTS': 2,
    }

    headers = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }

    urls_number = 0         # 获取到的urls
    download_number = 0     # 已下载的数量

    def __init__(self):
        self.image_file_path = './images/'
        if not os.path.exists(self.image_file_path):
            os.makedirs(self.image_file_path)

    def parse(self, response):
        image_paths = response.css("div.thumb-info a.jsAnchor.thumb-tags-toggle.tagged::attr('data-href')").getall()
        self.urls_number = len(image_paths)
        images = []
        print(f"[已获取][共获取{self.urls_number}图片链接]")
        for image_path in image_paths:
            print(f"[获取到的二级链接]:{image_path}")
            images.append({"image_code": image_path.split('/')[-1], "image_path": image_path})

        # 打开二级界面
        for image in images:
            print(f"[打开二级界面]:{image['image_path']}")
            yield scrapy.Request(
                url=image['image_path'], 
                callback=self.parse_image_details_url,
                meta={'image_code': image['image_code']},
                headers=self.headers,
            )


    def parse_image_details_url(self, response):
        with open('./html/page2.html', mode='w', encoding='utf-8') as f:
            f.write(response.body.decode('utf-8'))

        if response.status == 200:
            image_src = response.css("main section div.scrollbox img::attr('src')").get()
            print(f"[已获取][下载地址]:{image_src}")
            
            # yield scrapy.Request(
            #     url=image_src, 
            #     callback=self.parse_download_image, 
            #     meta={'image_name': response.meta['image_code']},
            #     headers=self.headers,
            # )

    # def parse_download_image(self, response):
    #     image_name = response.meta['image_code'] + '.jpg'
    #     if response.status == 200:
    #         with open(file=self.image_file_path + image_name, mode='wb') as img:
    #             img.write(response.body)
    #             print(f"[已下载][图片]:{image_name}")
    #             self.download_number += 1
    #         print(f"[已下载的数量]:{self.download_number}")