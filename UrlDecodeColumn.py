import os
import pandas as pd
from urllib.parse import unquote, urlparse


# 定义解码函数
def decode_url_query(url):
    try:
        parsed = urlparse(url)
        query = parsed.query

        if not query:
            return ''

        params = query.split('&')

        # 遍历每个键值对，找到 query 参数并解码
        for param in params:
            if '=' in param:
                key, value = param.split('=', 1)
                if key == 'query':
                    decoded_query = unquote(value)
                    print(f"Query 参数值（URLDecode）：{decoded_query}")
                    return decoded_query
    except Exception as e:
        print(f"解码URL时发生错误：{e}")
        return ''


# 设置Excel文件目录和输出路径
excel_dir = '/Users/Van/Desktop/抓取/BOSS直聘/数据处理/5001-7480/merged_file.xlsx'
output_file = '/Users/Van/Desktop/抓取/BOSS直聘/数据处理/5001-7480/decoded.xlsx'

# 初始化空的DataFrame
merged_df = pd.DataFrame()

# 遍历并读取所有Excel文件
df = pd.read_excel(excel_dir)

# 确保“页面网址”列存在
if '页面网址' not in df.columns:
    df['页面网址'] = ''

merged_df = pd.concat([merged_df, df], ignore_index=True)

# 应用解码函数到“页面网址”列，生成“搜索”列
if '页面网址' in merged_df.columns:
    merged_df['搜索'] = merged_df['页面网址'].apply(decode_url_query)
else:
    print("没有找到‘页面网址’列，无法进行解码。")

# 保存结果到新的Excel文件
merged_df.to_excel(output_file, index=False)

print("数据已成功处理并保存到：", output_file)