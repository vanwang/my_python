import pandas as pd
from urllib.parse import urlparse, parse_qs, unquote

# 读取上传的Excel文件
file_path = '/Users/Van/Desktop/抓取/前程无忧/四川-重庆/final/merged.xlsx'
df = pd.read_excel(file_path)

# 创建一个新列，存储URL解码后的查询参数
def decode_url_query(url):
    # 解析URL并获取查询部分
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # 解码查询参数
    decoded_params = {key: [unquote(value[0])] for key, value in query_params.items()}
    return decoded_params

# 假设"页面网址"列包含了我们需要处理的URL
df['解码后的查询参数'] = df['页面网址'].apply(decode_url_query)

# 保存新的Excel文件，包含解码后的查询参数
output_file = '/mnt/data/BOSS_merged_with_decoded_query.xlsx'
df.to_excel(output_file, index=False)

output_file
