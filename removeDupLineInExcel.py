import pandas as pd

# 读取Excel文件
def remove_duplicates(input_file, output_file):
    # 读取Excel文件
    df = pd.read_excel(input_file)

    # 删除重复行，保留第一次出现的
    df_no_duplicates = df.drop_duplicates(subset='职位网址')

    # 将去重后的数据保存到新文件
    df_no_duplicates.to_excel(output_file, index=False)

# 示例使用
input_file = '/Users/Van/Desktop/抓取/BOSS直聘/数据处理/2501-5000/职位详情页/BOSS直聘-职位详情页-admin005/merge/merged_file.xlsx'  # 输入的Excel文件路径
output_file = 'merged_file_unique.xlsx'  # 输出去重后的Excel文件路径
remove_duplicates(input_file, output_file)