import pandas as pd
from urllib.parse import unquote

# 读取Excel文件
df = pd.read_excel('/Users/Van/Desktop/抓取/BOSS直聘/数据处理/公司详情页/blank_companys_url.xlsx')

# 处理职位网址列
def process_url(url):
    # prefix = "https://www.zhipin.com/web/user/safe/verify-slider?callbackUrl="
    # if isinstance(url, str) and url.startswith(prefix):
    #     # 移除前缀并进行URL解码
    #     return unquote(url[len(prefix):])
    # return url
    return unquote(url)

# 应用处理函数
df['职位网址'] = df['职位网址'].apply(process_url)

# 保存处理后的文件
df.to_excel('A_processed.xlsx', index=False)