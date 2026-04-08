# 读取txt文件，去除重复的URL并写回新的文件
def remove_duplicate_urls(input_file, output_file):
    with open(input_file, 'r') as f:
        urls = f.readlines()

    # 去除重复的URL，使用set去重
    unique_urls = set(url.strip() for url in urls)

    # 将去重后的URL写入新文件
    with open(output_file, 'w') as f:
        for url in unique_urls:
            f.write(url + '\n')

# 示例使用
input_file = '/Users/Van/Desktop/抓取/BOSS直聘/数据处理/1-2500/职位URLs.txt'  # 输入的txt文件路径
output_file = '/Users/Van/Desktop/抓取/BOSS直聘/数据处理/1-2500/职位URLs-unique.txt'  # 输出去重后的文件路径
remove_duplicate_urls(input_file, output_file)