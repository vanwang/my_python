from ftplib import print_line

import pandas as pd
from urllib.parse import urlparse, parse_qs, unquote

# 读取上传的Excel文件
file_path = '/Users/Van/PycharmProjects/PythonProject/前程无忧-人工智能.xlsx'
df = pd.read_excel(file_path)

# 创建一个新列，存储URL解码后的查询参数
def decode_url_query(url):
    # 解析URL并获取查询部分
    parsed_url = unquote(url)
    print_line(parsed_url)
    return parsed_url

# 假设"页面网址"列包含了我们需要处理的URL
df['解码后的搜索关键词'] = df['搜索关键词'].apply(decode_url_query)

# 保存新的Excel文件，包含解码后的查询参数
output_file = 'B.xlsx'
df.to_excel(output_file, index=False)

output_file
