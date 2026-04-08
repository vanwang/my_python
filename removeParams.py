from urllib.parse import urlparse, urlunparse

output_path = "urls_no_params.txt"

def remove_url_params(url):
    # 解析URL
    parsed_url = urlparse(url)
    # 重新构建URL，去掉查询参数和片段
    clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
    return clean_url

# 读取文件内容
with open('职位_链接.txt', 'r', encoding='utf-8') as file:
    urls = file.readlines()

# 去掉参数并输出干净的URL
clean_urls = [remove_url_params(url.strip()) for url in urls]

# 保存到文件
with open(output_path, "w", encoding="utf-8") as output_file:
    output_file.write("\n".join(clean_urls))