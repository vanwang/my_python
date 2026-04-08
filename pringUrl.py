import pandas as pd

# 读取两个Excel文件
df_all = pd.read_excel('/Users/Van/Desktop/抓取/前程无忧/数据处理/all_unique_with_id.xlsx')
df_jobs = pd.read_excel('/Users/Van/Desktop/抓取/前程无忧/数据处理/jobs_unique.xlsx')

# 打印原始数据信息
print(f"原始数据数量:")
print(f"all_unique_with_id.xlsx 中的行数: {len(df_all)}")
print(f"jobs_unique.xlsx 中的行数: {len(df_jobs)}")

# 记录合并前的空值数量
null_before = df_all['职位信息'].isna().sum()

# 基于"职业ID"列合并两个数据框
df_merged = df_all.merge(
    df_jobs[['职位ID', '职位信息']],
    on='职位ID',
    how='left'
)

# 记录合并后的空值数量
null_after = df_merged['职位信息'].isna().sum()

# 计算成功匹配的数量
matched_count = null_before - null_after

# 打印处理结果统计
print("\n处理结果统计:")
print(f"成功匹配并更新的记录数: {matched_count}")
print(f"未能匹配的记录数: {null_after}")
print(f"合并后总记录数: {len(df_merged)}")

# 将合并后的数据保存回原文件
df_merged.to_excel('all_unique_with_id.xlsx', index=False)

print("\n处理完成!")
