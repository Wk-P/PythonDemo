from urllib.parse import urljoin
import scrapy, os

class WallpaperSpider(scrapy.Spider):
    name = 'wallpaperspider'
    allowed_domains = ['wallhaven.cc']
    start_urls = ["https://wallhaven.cc/latest?page=2"]
    page = 3
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 5,
        'LOG_LEVEL' : 'WARNING',
        'RETRY_TIMES': 50,
        'ITEM_PIPELINES': {
            'wallpaper.pipelines.WallpaperPipeline': 300,
        }
    }

    headers = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }

    urls_number = 0         # 获取到一级地址
    download_number = 0     # 已下载的数量
    gotten_number = 0       # 获取到下载地址
    
    max_limit_page = 4

    image_paths = []

    def __init__(self):
        self.image_file_path = './images/'
        if not os.path.exists(self.image_file_path):
            os.makedirs(self.image_file_path)

    def parse(self, response):
        if response.status == 200:
            self.image_paths.append(response.css("div.thumb-info a.jsAnchor.thumb-tags-toggle.tagged::attr('data-href')").getall())
            self.urls_number += len(self.image_paths[-1])
            # print(f"[TEST LINE]:len(self.image_paths[-1]) : {len(self.image_paths[-1])}")
            # print(f"[TEST LINE]:self.image_paths : {self.image_paths}")
            images = []
            print(f"[已获取][共获取 {self.urls_number} 图片链接]")
            for image_path in self.image_paths[-1]:
                # print(f"[获取到的二级链接]:{image_path}")
                images.append({"image_code": image_path.split('/')[-1], "image_path": image_path})

            # 爬取二级界面
            for image in images:
                # print(f"[打开二级界面]:{image['image_path']}")
                yield scrapy.Request(
                    url=image['image_path'], 
                    callback=self.parse_image_details_url,
                    meta={
                        'image_code': image['image_code']
                    },
                    headers=self.headers,
                )

            if self.page <= self.max_limit_page + 1:
                next_url = urljoin(self.start_urls[0], f'latest?page={self.page}')
                # print(f"[TEST LINE]: urljoin === > {next_url}")
                self.page += 1
                print(f"[已获取 {self.page - 2} 页链接]")
                yield scrapy.Request(url=next_url, callback=self.parse, meta={'page': self.page})

    def parse_image_details_url(self, response):
        if response.status == 301 or response.status == 302:
            redirected_url = response.headers['Location'].decode('utf-8')
            yield scrapy.Request(
                url=redirected_url,
                callback=self.parse_image_details_url,
                meta={'image_code': response.meta['image_code']},
                headers=self.headers,
            )
        else:
            # with open('./html/page2.html', mode='w', encoding='utf-8') as f:
                # f.write(response.body.decode('utf-8'))

            if response.status == 200:
                image_src = response.css("main section div.scrollbox img::attr('src')").get()
                self.gotten_number += 1
                print(f"[1/3 已获取 {self.gotten_number}/{self.urls_number}][下载地址]:{image_src}")
                # 开启下载请求
                yield scrapy.Request(
                    url=image_src, 
                    callback=self.parse_download_image, 
                    meta={'image_name':image_src.split('-')[-1]},
                    headers=self.headers,
                )

    def parse_download_image(self, response):
        image_name = response.meta['image_name']
        if response.status == 200:
            with open(file=self.image_file_path + image_name, mode='wb') as img:
                img.write(response.body)
                self.download_number += 1
                try: 
                    print(f"[2/3 已下载 {self.download_number}/{self.urls_number}][图片]:{image_name}")
                except:
                    print(f"[错误:抓取链接失败][已获取链接个数 {self.urls_number}]")
            try:
                print(f"[3/3 已下载 {self.download_number}/{self.urls_number}][下载进度 {round(float(self.download_number/self.urls_number*100), 2)}%]\n")
            except:
                    print(f"[错误:抓取链接失败][已获取链接个数 {self.urls_number}]")
    def closed(self, reason):
        if self.urls_number > 0:
            print(f"[已爬取 {self.page - 2} 页][已下载 {self.download_number}/{self.urls_number}][下载完成度 {round(float(self.download_number/self.urls_number*100), 2)}%]")
        else:
            print(f"[错误:抓取链接失败][已获取链接个数 {self.urls_number}]")