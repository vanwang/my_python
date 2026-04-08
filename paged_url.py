import pandas as pd
import re
import numpy as np
import os
from typing import List


def load_and_clean_data(excel_path: str) -> pd.DataFrame:
    """读取Excel文件并清洗数据（修复strip错误，保留count=0记录）"""
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Excel文件不存在：{excel_path}")

    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        raise ValueError(f"读取Excel失败：{str(e)}")

    print(f"✅ 成功读取Excel文件，共 {len(df)} 条原始记录")

    # 校验必要列
    required_cols = ['url', 'count']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Excel缺少必要列：{missing_cols}（需包含url、count列）")

    # 数据预处理：修复核心错误 + 严谨过滤
    df_clean = df.copy()

    # 1. 处理count列：空值转0，统一为整数
    df_clean['count_int'] = pd.to_numeric(df_clean['count'], errors='coerce').fillna(0).astype(int)

    # 2. 处理url列：修复strip错误（用.str.strip()批量处理）
    # 先转为字符串，再去除首尾空格，空值填充为空字符串
    df_clean['url'] = df_clean['url'].astype(str).str.strip().fillna('')

    # 3. 过滤url为空的记录（仅保留url非空的）
    df_clean = df_clean[df_clean['url'] != ''].copy()
    df_valid = df_clean.reset_index(drop=True)

    # 统计信息
    invalid_count = len(df) - len(df_valid)
    count_zero = len(df_valid[df_valid['count_int'] == 0])
    count_gt_zero = len(df_valid[df_valid['count_int'] > 0])

    print(f"📊 数据筛选结果：")
    print(f"   - 有效记录数（url有效）：{len(df_valid)} 条")
    print(f"     ├─ count>0 记录数：{count_gt_zero} 条（动态分页）")
    print(f"     └─ count=0/空值 记录数：{count_zero} 条（强制page=1）")
    print(f"   - 无效记录数：{invalid_count} 条（url为空）")

    return df_valid


def calculate_pages(df: pd.DataFrame, per_page: int = 100) -> pd.DataFrame:
    """计算总页数（count=0时强制1页）"""
    df['total_pages'] = np.where(
        df['count_int'] > 0,
        np.ceil(df['count_int'] / per_page).astype(int),
        1
    )
    df['total_pages'] = df['total_pages'].apply(lambda x: max(x, 1))

    total_url_count = df['total_pages'].sum()
    print(f"🔢 分页计算结果：")
    print(f"   - 每页数据量：{per_page} 条")
    print(f"   - 预计生成URL总数：{total_url_count} 条")
    print(f"     ├─ count>0 生成：{df[df['count_int'] > 0]['total_pages'].sum()} 条")
    print(f"     └─ count=0 生成：{len(df[df['count_int'] == 0])} 条（各1页）")

    return df


def complete_url_params(original_url: str, page_num: int, per_page_val: int = 100) -> str:
    """精准匹配per_page和page参数（避免互相干扰）"""
    # 确保url是字符串且去除首尾空格（兜底处理）
    url = str(original_url).strip()

    # 分离URL的锚点（#后面的内容）
    anchor = ''
    if '#' in url:
        url, anchor = url.split('#', 1)

    # --------------------------
    # 1. 精准处理per_page参数
    per_page_pattern = r'(?<=[?&])per_page=\d+(?=&|$)'
    if re.search(per_page_pattern, url):
        url = re.sub(per_page_pattern, f'per_page={per_page_val}', url)
    else:
        url += '&per_page=' + str(per_page_val) if '?' in url else '?per_page=' + str(per_page_val)

    # --------------------------
    # 2. 精准处理page参数
    page_pattern = r'(?<=[?&])page=\d+(?=&|$)'
    if re.search(page_pattern, url):
        url = re.sub(page_pattern, f'page={page_num}', url)
    else:
        url += '&page=' + str(page_num)

    # 恢复锚点
    if anchor:
        url += '#' + anchor

    # 清理多余的分隔符
    url = re.sub(r'&$', '', url)
    return url


def generate_all_urls(df: pd.DataFrame, per_page: int = 100) -> List[str]:
    """批量生成所有分页URL"""
    all_complete_urls = []
    for _, row in df.iterrows():
        original_url = row['url']
        total_pages = row['total_pages']
        for page in range(1, total_pages + 1):
            complete_url = complete_url_params(original_url, page, per_page)
            all_complete_urls.append(complete_url)

    print(f"✅ 实际生成URL总数：{len(all_complete_urls)} 条")
    return all_complete_urls


def save_urls_to_txt(url_list: List[str], txt_path: str, df_valid: pd.DataFrame, per_page: int = 100):
    """保存URL到TXT文件"""
    output_dir = os.path.dirname(txt_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    count_zero_num = len(df_valid[df_valid['count_int'] == 0])

    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("# 分页URL自动生成清单\n")
        f.write(f"# 生成时间：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# 每页数据量：{per_page} 条\n")
        f.write(f"# 生成规则：\n")
        f.write(f"  - count>0：根据count动态计算页数（向上取整）\n")
        f.write(f"  - count=0/空值：强制生成page=1的URL\n")
        f.write(f"# 参数处理规则：精准匹配per_page/page参数，避免互相干扰\n")
        f.write(f"# 有效原始记录数：{len(df_valid)} 条\n")
        f.write(f"  ├─ count>0 记录数：{len(df_valid[df_valid['count_int'] > 0])} 条\n")
        f.write(f"  └─ count=0/空值 记录数：{count_zero_num} 条\n")
        f.write(f"# 生成URL总数：{len(url_list)} 条\n")
        f.write(f"# 格式：每条URL独立一行，可直接复制使用\n\n")
        for url in url_list:
            f.write(url + '\n')

    print(f"\n📁 TXT文件生成完成！")
    print(f"   - 文件路径：{os.path.abspath(txt_path)}")
    print(f"   - 文件编码：UTF-8")
    print(f"   - 内容：{len(url_list)} 条URL + 详细说明")


# ------------------- 主执行逻辑 -------------------
if __name__ == "__main__":
    # 配置参数（修改为你的实际路径）
    EXCEL_PATH = '/Users/Van/Desktop/url.xlsx'
    TXT_SAVE_PATH = '/Users/Van/Desktop/complete_paginated_urls.txt'
    PER_PAGE = 100

    try:
        df_valid = load_and_clean_data(EXCEL_PATH)

        if len(df_valid) == 0:
            print("⚠️ 无有效记录，终止生成！")
        else:
            df_valid = calculate_pages(df_valid, PER_PAGE)
            all_urls = generate_all_urls(df_valid, PER_PAGE)

            # 验证前3条URL
            if all_urls:
                print(f"\n🔍 前3条URL示例（验证参数完整性）：")
                for i, url in enumerate(all_urls[:3]):
                    has_per_page = 'per_page=100' in url
                    has_correct_page = f'page={i + 1}' in url
                    print(f"{i + 1}. {url}")
                    print(
                        f"   - 参数验证：per_page=100 {'✅' if has_per_page else '❌'} | page={i + 1} {'✅' if has_correct_page else '❌'}")

            save_urls_to_txt(all_urls, TXT_SAVE_PATH, df_valid, PER_PAGE)

    except Exception as e:
        print(f"\n❌ 执行失败：{type(e).__name__} - {str(e)}")
        # 可选：打印详细错误栈，方便定位问题
        # import traceback
        # traceback.print_exc()