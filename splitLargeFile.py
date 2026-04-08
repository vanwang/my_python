def split_urls(input_file, output_prefix, max_lines=50000):
    with open(input_file, 'r') as file:
        urls = file.readlines()

    # 每max_lines条URL为一个文件
    total_urls = len(urls)
    num_files = (total_urls // max_lines) + (1 if total_urls % max_lines > 0 else 0)

    for i in range(num_files):
        start_index = i * max_lines
        end_index = min((i + 1) * max_lines, total_urls)

        # 新文件的路径
        output_file = f"{output_prefix}_{i + 1}.txt"

        # 将一部分URL写入新的文件
        with open(output_file, 'w') as out_file:
            out_file.writelines(urls[start_index:end_index])

        print(f"文件 {output_file} 已保存，包含 {end_index - start_index} 条URL.")


# 示例使用
input_file = '/Users/Van/Desktop/抓取/BOSS直聘/数据处理/5001-7480/职位详情页/职位URLs.txt'  # 输入的txt文件路径
output_prefix = '/Users/Van/Desktop/抓取/BOSS直聘/数据处理/5001-7480/职位详情页/职位URLs_split'  # 拆分后文件的前缀
split_urls(input_file, output_prefix)