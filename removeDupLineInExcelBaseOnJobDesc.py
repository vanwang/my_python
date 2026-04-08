import pandas as pd


def remove_duplicates(excel_file):
    # 读取Excel文件
    df = pd.read_excel(excel_file)

    # 按职位ID分组，并保留职位信息不为空的行
    # 如果同一职位ID的所有行职位信息都为空，则保留最后一条记录
    def select_row(group):
        # 检查是否有职位信息不为空的行
        non_empty = group[group['职业链接'].notna()]
        if len(non_empty) > 0:
            # 如果有不为空的行，返回第一个不为空的行
            return non_empty.iloc[0]
        else:
            # 如果所有行都为空，返回最后一行
            return group.iloc[-1]

    # 应用去重逻辑
    result = df.groupby('职业链接', as_index=False).apply(select_row)

    # 保存结果到新的Excel文件
    output_file = 'output.xlsx'
    result.to_excel(output_file, index=False)

    # 打印处理结果
    print(f'原始数据行数：{len(df)}')
    print(f'处理后行数：{len(result)}')
    print(f'删除重复行数：{len(df) - len(result)}')
    print(f'结果已保存至：{output_file}')


# 使用示例
excel_file = '/Users/Van/Desktop/抓取/前程无忧/数据处理/all_with_decoded_query.xlsx'  # 替换为你的Excel文件名
remove_duplicates(excel_file)
