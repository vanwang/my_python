import os
import re


def remove_comments(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 删除单行注释（//）
    content = re.sub(r'//.*', '', content)
    # 删除多行注释和文档注释（/* ... */ 和 /** ... */）
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


# 使用示例：处理指定路径下的所有 .java 文件
def main():
    directory = '/Users/Van/Desktop/'

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('APP.txt'):
            print(f"处理文件: {filename}")
            remove_comments(file_path)


if __name__ == "__main__":
    main()