import pandas as pd
import numpy as np


def fill_job_info(file_a, file_b):
    # 读取两个Excel文件
    df_a = pd.read_excel(file_a)
    df_b = pd.read_excel(file_b)

    # 创建一个DataFrame副本，避免修改原始数据
    df_result = df_a.copy()

    # 使用页面网址作为键，将B文件中的职位信息合并到A文件中
    url_to_job_info = dict(zip(df_b['页面网址'], df_b['职位信息']))

    # 记录更新信息
    update_count = 0
    empty_to_filled = 0
    value_changed = 0

    print("\n更新详情：")
    print("-" * 100)
    print(f"{'页面网址':<50} | {'更新前':<20} | {'更新后':<20}")
    print("-" * 100)

    # 遍历A文件的每一行
    for index, row in df_result.iterrows():
        url = row['页面网址']
        # 如果该网址在B文件中存在
        if url in url_to_job_info:
            old_value = row['职位信息']
            new_value = url_to_job_info[url]

            # 判断原值是否为空（考虑多种空值情况）
            is_old_empty = pd.isna(old_value) or str(old_value).strip() == ''

            # 只有当新值不为空时才更新
            if not (pd.isna(new_value) or str(new_value).strip() == ''):
                # 更新职位信息
                df_result.at[index, '职位信息'] = new_value
                update_count += 1

                # 打印更新信息
                old_display = '空' if is_old_empty else str(old_value)
                print(f"{url[:50]:<50} | {old_display[:20]:<20} | {str(new_value)[:20]:<20}")

                # 统计更新类型
                if is_old_empty:
                    empty_to_filled += 1
                else:
                    value_changed += 1

    # 保存结果到新的Excel文件
    output_file = 'output.xlsx'
    df_result.to_excel(output_file, index=False)

    # 打印处理结果统计
    print("\n处理结果统计：")
    print("-" * 50)
    print(f"总记录数：{len(df_result)}")
    print(f"匹配到的记录数：{sum(df_result['页面网址'].isin(df_b['页面网址']))}")
    print(f"实际更新记录数：{update_count}")
    print(f"  - 从空值更新：{empty_to_filled}")
    print(f"  - 值被覆盖：{value_changed}")
    print(f"\n结果已保存至：{output_file}")


# 使用示例
file_a = '/Users/Van/Desktop/抓取/前程无忧/数据处理/jobs_unique.xlsx'  # 替换为你的A文件名
file_b = '/Users/Van/Desktop/抓取/前程无忧/数据处理/merged_file.xlsx'  # 替换为你的B文件名
fill_job_info(file_a, file_b)
