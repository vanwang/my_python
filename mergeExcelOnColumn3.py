import pandas as pd


def merge_excel_files(a_file, b_file, output_file):
    # 读取A.xlsx和B.xlsx
    df_a = pd.read_excel(a_file)
    df_b = pd.read_excel(b_file)

    # 依据“页面网址”和“职业链接”匹配数据
    merged_df = df_a.merge(df_b[['页面网址', '职位ID', '职位信息']], left_on='职业链接', right_on='页面网址',
                           how='left')

    # 更新A.xlsx中的“职位ID”和“职位信息”
    merged_df['职位ID_x'] = merged_df['职位ID_y'].combine_first(merged_df['职位ID_x'])
    merged_df['职位信息_x'] = merged_df['职位信息_y'].combine_first(merged_df['职位信息_x'])

    # 删除多余列
    merged_df = merged_df.drop(columns=['职位ID_y', '职位信息_y', '页面网址'])

    # 重命名列名回原始
    merged_df = merged_df.rename(columns={'职位ID_x': '职位ID', '职位信息_x': '职位信息'})

    # 保存合并后的数据
    merged_df.to_excel(output_file, index=False)
    print(f'合并完成，结果已保存至 {output_file}')


# 示例使用
merge_excel_files('/Users/Van/Desktop/抓取/前程无忧/数据处理/1. 前程无忧-all.xlsx', '/Users/Van/Desktop/抓取/前程无忧/数据处理/jobs.xlsx',
                  '前程无忧.xlsx')
