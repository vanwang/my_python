import pandas as pd

# 读取Excel文件
df = pd.read_excel('/Users/Van/Desktop/抓取/前程无忧/数据处理/all_with_decoded_query.xlsx')

# 打印原始数据行数
print(f"去重前数据行数: {len(df)}")

column = '职业链接'

# 打印原始数据行数
print(f"去重前数据行数: {len(df)}")

# 添加原始顺序列
df['原始顺序'] = range(len(df))

# 数据清理
df[column] = df[column].fillna('')  # 将NA/NaN值替换为空字符串
df[column] = df[column].astype(str)  # 转换为字符串
df[column] = df[column].str.strip()  # 去除首尾空白

# 按职位ID去重，保留第一次出现的记录
df_deduped = df.drop_duplicates(subset=[column], keep='first')

# 按原始顺序排序
df_deduped = df_deduped.sort_values('原始顺序')

# 删除原始顺序列
df_deduped = df_deduped.drop('原始顺序', axis=1)

# 打印去重后数据行数
print(f"去重后数据行数: {len(df_deduped)}")
print(f"删除的重复行数: {len(df) - len(df_deduped)}")

# 保存结果到新文件
df_deduped.to_excel('output_deduped.xlsx', index=False)

print("处理完成！")

# 打印详细统计信息
print("\n空值统计:")
print(f"去重前空值数量: {df[column].isna().sum()}")
print(f"去重后空值数量: {df_deduped[column].isna().sum()}")
