#!/usr/bin/env python3
"""
清理SQL文件中的非ASCII字符，解决编码问题
"""
import re
import sys

def clean_sql_file(input_file, output_file):
    """清理SQL文件中的非ASCII字符"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 方法1：删除所有非ASCII字符（简单但可能破坏数据）
    # cleaned = content.encode('ascii', 'ignore').decode('ascii')

    # 方法2：只清理注释中的中文，保留SQL语句
    lines = content.split('\n')
    cleaned_lines = []

    for line in lines:
        # 如果是注释行（以--开头），删除非ASCII字符
        if line.strip().startswith('--'):
            # 只保留ASCII字符
            cleaned_line = line.encode('ascii', 'ignore').decode('ascii')
            cleaned_lines.append(cleaned_line)
        else:
            # SQL语句，保留原样（假设没有非ASCII字符在关键字或数据中）
            # 但可以检查是否有非ASCII字符在字符串字面量中
            cleaned_lines.append(line)

    cleaned = '\n'.join(cleaned_lines)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    print(f"已清理文件: {input_file} -> {output_file}")

    # 检查还有哪些非ASCII字符
    print("\n检查剩余的非ASCII字符位置:")
    for i, char in enumerate(cleaned):
        if ord(char) > 127:
            line_num = cleaned[:i].count('\n') + 1
            col_num = i - cleaned[:i].rfind('\n') - 1
            print(f"  行 {line_num}, 列 {col_num}: '{char}' (U+{ord(char):04X})")

    return cleaned

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python cleanup_sql.py <输入文件> <输出文件>")
        print("示例: python cleanup_sql.py scripts/init-db.sql scripts/init-db-cleaned.sql")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    clean_sql_file(input_file, output_file)