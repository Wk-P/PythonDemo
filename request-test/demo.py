import requests, os

if __name__ == "__main__":
    headers = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }
    response = requests.get("https://whvn.cc/x67z2v", headers=headers)
    filename = os.path.dirname(__file__) + '/img/'
    if not os.path.exists(filename):
        os.makedirs(filename)

    with open(filename + 'img1.html', 'w') as f:
        f.write(response.content.decode('utf-8'))