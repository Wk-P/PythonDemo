import requests, os, json

def read_cookie_file(filename):
    with open(file=filename, mode='r', encoding='utf-8') as f:
        cookie = json.load(f)['cookie']
        return cookie

def get_to_file(url):
    path = os.path.dirname(__file__) + "/html/"
    if not os.path.exists(path):
        os.mkdir(path)
    


    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'cookie': read_cookie_file('cookie/cookie.json')
    }

    response = requests.request(method="GET", url=url, headers=headers)

    with open(file=path + 'page.html', mode='w', encoding='utf-8') as f:
        f.write(response.content.decode('utf-8'))

    print("写入文件成功!")

if "__main__" == __name__:
    get_to_file(url='https://space.bilibili.com')