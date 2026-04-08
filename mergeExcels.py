import pandas as pd
import os

# 设置目标目录和输出文件路径
target_dir = '/Users/Van/Desktop/github_search/GPT/list_repo_forks'  # 替换为你的Excel文件所在目录
output_file = target_dir + '/merged_file.xlsx'

# 初始化合并后的DataFrame和计数器
merged_df = pd.DataFrame()
total_rows = 0

# 遍历目标目录下的所有文件
for filename in os.listdir(target_dir):
    if filename.endswith('.xlsx') or filename.endswith('.xls'):
        file_path = os.path.join(target_dir, filename)

        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)

            # 追加到合并的DataFrame中
            merged_df = pd.concat([merged_df, df], axis=0)

            # 累计行数
            total_rows += len(df)

            print(f"成功读取并处理了文件：{filename}")

        except Exception as e:
            print(f"错误：文件 {filename} 处理失败，原因：{str(e)}")

# 写入到新的Excel文件中
merged_df.to_excel(output_file, index=False)
# merged_df.to_csv(output_file, index=False)
print(f"\n合并后的文件已保存为：{output_file}")
print(f"总共处理了 {total_rows} 条数据。")