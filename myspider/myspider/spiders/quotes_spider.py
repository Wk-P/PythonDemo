import scrapy 

class QuotesSpider(scrapy.Spider):
    # 用于控制台crawl [name] 启动爬虫
    name = "quotes"

    # 要爬取的页面列表
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
        'https://quotes.toscrape.com/page/2/',
    ]

    # def start_requests(self):
        # 使用start_urls替代函数执行
        # for url in urls:
        #     # yield: 一有结果就返回，之后再运行剩下的代码，直到函数结束
        #     # 发出一个请求(Request，并启动一个回调函数parse用于解析返回的response)
        #     yield scrapy.Request(url=url, callback=self.parse)

    # 自定义回调函数parse，用于解析response
    # parse是默认的解析函数，我们在这里重写这个函数以便spider自动为call_back调用
    def parse(self, response):

        # 解析并直接从迭代器传出数据
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css("div.tags a.tag::text").getall(),
            }
        
        next_page = response.css("li.next a::attr('href')").get()
        if next_page is not None:
            # next_page = response.urljoin(next_page)               # 下一页的page界面添加到url
            yield response.follow(next_page, callback=self.parse)   # 快捷方式完成
        # page = response.url.split('/')[-2]
        # filename = f'quotes-{page}.html'
        # Path(filename).write_bytes(response.body)   # 构建文件写入response解析后的html代码
        # self.log(f'Saved file {filename}')          # 向控制台输出Log语句