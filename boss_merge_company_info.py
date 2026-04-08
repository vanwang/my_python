import pandas as pd


def merge_excel_files():
    try:
        # 读取两个Excel文件
        df_a = pd.read_excel('/Users/Van/Desktop/抓取/BOSS直聘/数据处理/merge3/decoded-5001-7480_company_merged.xlsx')
        df_b = pd.read_excel('/Users/Van/Desktop/抓取/BOSS直聘/数据处理/merge3/jobs_merged_file_not_blank.xlsx')

        # 创建一个新的数据框来存储结果，初始时复制A文件的所有内容
        result_df = df_a.copy()

        # 遍历A文件中的每一行
        for index_a, row_a in df_a.iterrows():
            # 在B文件中查找匹配的行
            matching_rows = df_b[df_b['职位网址'] == row_a['职业链接']]

            # 如果找到匹配的行
            if not matching_rows.empty:
                # 获取B文件中匹配的第一行
                match_row = matching_rows.iloc[0]

                # 将B文件中的所有列添加到结果中
                for col in df_b.columns:
                    # 跳过用于匹配的列，避免重复
                    if col != '职位网址':
                        result_df.at[index_a, col] = match_row[col]

        # 保存结果到新的Excel文件
        result_df.to_excel('合并结果.xlsx', index=False)
        print("文件合并成功！结果已保存到'合并结果.xlsx'")

        # 打印处理统计信息
        total_matches = len(df_a[df_a['职业链接'].isin(df_b['职位网址'])])
        print(f"\n处理统计信息：")
        print(f"A文件总记录数：{len(df_a)}")
        print(f"B文件总记录数：{len(df_b)}")
        print(f"成功匹配的记录数：{total_matches}")

    except FileNotFoundError:
        print("错误：找不到输入的Excel文件，请确保A.xlsx和B.xlsx在正确的目录下")
    except Exception as e:
        print(f"发生错误：{str(e)}")


if __name__ == "__main__":
    merge_excel_files()
