from pathlib import Path

import scrapy 

class WallpaperSpider(scrapy.Spider):
    name = "wallpaper"

    start_urls = [
        # "https://wallhaven.cc/"
        "https://wallhaven.cc/latest?page=2",
        "https://wallhaven.cc/latest?page=3",
        "https://wallhaven.cc/latest?page=4",
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        print(page)
        filename = f'wallpaper-{page}.html'
        Path(filename).write_bytes(response.body)