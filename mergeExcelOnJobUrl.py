import pandas as pd

# 读取A.xlsx和B.xlsx文件
a_df = pd.read_excel('/Users/Van/Desktop/抓取/前程无忧/人工智能/前程无忧-人工智能_merged_file.xlsx')
b_df = pd.read_excel('/Users/Van/Desktop/抓取/前程无忧/人工智能/前程无忧-职位详情_人工智能_1.xlsx')

print("文件读取完成!")

# 创建一个空列表来存储需要添加的职位信息
new_positions = []

# 遍历A.xlsx中的"职业链接"
print("开始遍历A.xlsx中的'职业链接'...")
for link in a_df['职业链接']:
    print(f"正在检查链接: {link}")
    # 检查B.xlsx中是否有相同的"页面网址"
    matching_row = b_df[b_df['页面网址'] == link]
    if not matching_row.empty:
        # 如果找到匹配的行,就将"职位信息"添加到新列表中
        print(f"找到匹配的行,添加职位信息: {matching_row['职位信息'].values[0]}")
        new_positions.append(matching_row['职位信息'].values[0])
    else:
        # 如果没有找到匹配的行,就添加一个空值
        print(f"未找到匹配的行,添加空值")
        new_positions.append('')
print("A.xlsx中的'职业链接'遍历完成!")

# 将新的"职位信息"添加到A.xlsx中
print("正在将新的'职位信息'添加到A.xlsx中...")
a_df['职位信息'] = new_positions
print("添加完成!")

# 保存更新后的A.xlsx文件
print("正在保存更新后的A.xlsx文件...")
a_df.to_excel('A.xlsx', index=False)
print("保存完成!")
