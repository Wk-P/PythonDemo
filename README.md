# 使用Scrapy 下载 wallhaven.cc 高清壁纸

## 功能
### - 下载 latest 壁纸 
### - 下载 任意关键字 壁纸 ###
---
# 运行教程
+ ## 直接下载仓库代码到本地
+ ## 安装 python3 以及 scrapy 第三方库
    - ### python3 安装（略）
    - ### scrapy 安装 
        python3 安装完成后打开任意 cmd 窗口

        输入以下指令

            > pip3 install scrapy

        安装完成后, 在 cmd 命令行中转调至 /path/ScrapySpider/wallpaper文件夹下，自行选择运行以下两种代码
        
        1. 下载 latest 图集
            
                > scrapy crawl wallpaperspider

        2. 下载 keyword 图集
        
                > scrapy crawl searchpaperspider

            默认关键词为 "sakura" 可在程序内自行更换