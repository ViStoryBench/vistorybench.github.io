import os
from pathlib import Path

def rename_images_to_png(target_dir):
    """
    递归地查找指定目录中的图片文件，并将它们的后缀名更改为 .png。

    Args:
        target_dir (str): 需要处理的目标目录路径。
    """
    root_path = Path(target_dir)
    # 检查目标路径是否存在且是否为目录
    if not root_path.is_dir():
        print(f"错误：目录 '{target_dir}' 不存在或不是一个有效的目录。")
        return

    # 定义需要识别的常见图片后缀名（统一转换为小写）
    image_extensions = {'.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
    print(f"开始扫描目录: {root_path.resolve()}") # 打印绝对路径更清晰

    renamed_count = 0
    skipped_count = 0

    # 使用 rglob('*') 递归遍历所有文件和子目录
    for item in root_path.rglob('*'):
        # 确保处理的是文件而不是目录
        if item.is_file():
            # 获取文件后缀名并转换为小写，以便不区分大小写地比较
            original_suffix_lower = item.suffix.lower()

            # 检查文件后缀是否在我们定义的图片后缀列表中
            if original_suffix_lower in image_extensions:
                # 构建新的文件路径，只改变后缀名为 .png
                new_path = item.with_suffix('.png')

                # 如果文件名（包括路径）已经是目标 .png 格式，则跳过
                if item == new_path:
                    # print(f"跳过（已经是 .png）: {item}") # 可以取消注释以查看详细跳过信息
                    skipped_count += 1
                    continue

                # 检查具有新 .png 后缀的文件是否已存在
                if new_path.exists():
                    print(f"警告：目标文件 '{new_path}' 已存在。跳过重命名 '{item}'。")
                    skipped_count += 1
                    continue

                # 尝试重命名文件
                try:
                    item.rename(new_path)
                    print(f"重命名: '{item}' -> '{new_path}'")
                    renamed_count += 1
                except OSError as e:
                    # 处理可能发生的错误，例如权限问题
                    print(f"错误：无法重命名文件 '{item}' 到 '{new_path}': {e}")
                    skipped_count += 1
            # else: # 如果需要，可以取消注释以查看非图片文件或已是png的文件
                # print(f"跳过（非图片或已是.png）: {item}")
                # skipped_count += 1

    print(f"\n处理完成。")
    print(f"成功重命名 {renamed_count} 个文件。")
    print(f"跳过 {skipped_count} 个文件。")

if __name__ == "__main__":
    # 指定要处理的目录路径
    # 使用 r"" 原始字符串来处理Windows路径中的反斜杠 '\'
    output_directory = r"data\outputs"
    rename_images_to_png(output_directory)
