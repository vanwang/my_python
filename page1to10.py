import re
import os


def extract_base_link(link: str) -> tuple[str, str]:
    """
    提取链接的基础部分和仓库名称
    :param link: 原始链接（如https://api.github.com/repos/xtekky/gpt4free/commits?repo_id=123&page=1）
    :return: (基础链接部分<不含page参数>, 仓库名称)
    """
    # 匹配仓库名称和链接基础部分
    repo_pattern = r'(https://api\.github\.com/repos/([\w\-]+/[\w\-]+)/commits)\?(.*)'
    # repo_pattern = r'(https://api\.github\.com/users/([\w\-]+)/followers)\?(.*)'
    match = re.match(repo_pattern, link.strip())
    if not match:
        return "", ""

    base_url = match.group(1)  # https://api.github.com/repos/xtekky/gpt4free/commits
    repo_name = match.group(2)  # xtekky/gpt4free
    params = match.group(3)  # repo_id=123&page=1

    # 移除params中的page参数（如果存在）
    clean_params = re.sub(r'(?<=[?&])page=\d+', '', params).strip('&')
    full_base_link = f"{base_url}?{clean_params}" if clean_params else base_url

    return full_base_link, repo_name


def complete_page_params(input_file: str, output_file: str, page_start: int = 1, page_end: int = 10):
    """
    补齐链接中的page参数，生成page从start到end的完整链接并保存到文件
    核心优化：精准解析原始链接、处理各种参数组合、避免重复/遗漏
    """
    # 1. 读取原始文件并提取所有有效链接
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"原始文件 {input_file} 不存在！")

    original_links = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 只处理GitHub commits链接
            #if line.startswith("https://api.github.com/users/") and "/followers?" in line:
            if line.startswith("https://api.github.com/repos/") and "/commits?" in line:
                original_links.append(line)

    if not original_links:
        raise ValueError("未从原始文件中读取到任何GitHub commits链接！")

    # 2. 去重并提取基础链接
    base_links = {}  # key: 仓库名称, value: 基础链接（不含page参数）
    for link in original_links:
        base_link, repo_name = extract_base_link(link)
        if base_link and repo_name:
            base_links[repo_name] = base_link  # 去重：同一仓库只保留一个基础链接

    if not base_links:
        raise ValueError("未解析到有效的仓库链接！请检查原始文件链接格式。")

    # 3. 生成page=1到page=10的完整链接
    completed_links = ["# 补齐page参数（1-10）的GitHub仓库commits链接清单",
                       "# 生成时间：{}".format(os.path.getctime(input_file)), "\n"]

    for idx, (repo_name, base_link) in enumerate(base_links.items(), 1):
        #completed_links.append(f"## {idx}. 仓库：{repo_name}")
        # 拼接不同page的链接
        for page in range(page_start, page_end + 1):
            # 处理基础链接是否已有参数分隔符
            if "?" in base_link:
                full_link = f"{base_link}&page={page}"
            else:
                full_link = f"{base_link}?page={page}"
            completed_links.append(full_link)
        #completed_links.append("")  # 空行分隔不同仓库

    # 4. 保存到输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(completed_links))

    # 输出统计信息
    total_links = len(base_links) * (page_end - page_start + 1)
    print("=" * 50)
    print(f"处理完成！统计信息：")
    print(f"- 原始文件中解析出有效仓库数：{len(base_links)}")
    print(f"- 生成链接总数（page{page_start}-{page_end}）：{total_links}")
    print(f"- 结果文件路径：{os.path.abspath(output_file)}")
    print("=" * 50)


# ------------------- 调用示例 -------------------
if __name__ == "__main__":
    # 【请务必修改为你的实际文件路径】
    INPUT_FILE = "/Users/Van/Desktop/commits.txt"  # 你的原始链接文件
    OUTPUT_FILE = "/Users/Van/Desktop/commits_all.txt"  # 生成的结果文件

    try:
        complete_page_params(
            input_file=INPUT_FILE,
            output_file=OUTPUT_FILE,
            page_start=1,
            page_end=10
        )
    except Exception as e:
        print(f"\n处理出错：{type(e).__name__} - {str(e)}")
        # 可选：打印详细错误栈
        # import traceback
        # traceback.print_exc()