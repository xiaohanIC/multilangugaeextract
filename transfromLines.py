import re

def transform_line(line):
    # 使用正则表达式匹配格式并进行替换
    match = re.match(r'(\w+)\("([^"]+)", "([^"]+)"\)', line)
    if match:
        key = match.group(1)
        title = match.group(2)
        desc = match.group(3)
        return f'{key}(MultiLangSupportUtil.lang(MultiLangResourceEnum.{key}_TITLE), MultiLangSupportUtil.lang(MultiLangResourceEnum.{key}_DESC)),'
    return line

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            transformed_line = transform_line(line.strip())
            outfile.write(transformed_line + '\n')


if __name__ == "__main__":
    # 指定输入文件和输出文件的路径
    input_file = 'lines.txt'
    output_file = 'linesOutput.txt'

    # 处理文件
    process_file(input_file, output_file)