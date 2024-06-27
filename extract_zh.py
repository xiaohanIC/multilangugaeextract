import os
import re
from googletrans import Translator
import random

translator = Translator()
stringEnSet = {""}

def extract_chinese_sentences_from_file(file_path):

    # 正则表达式匹配双引号之间的中文内容
    chinese_sentence_pattern = re.compile(r'\"[^\"]*[\u4e00-\u9fa5][^\"]*\"')
    value_placeHolder = re.compile(r'(\$\{[^}]+})')
    expression_placeholder = re.compile(r'\$[a-zA-Z_][a-zA-Z0-9_]*')

    try:
        with (open(file_path, 'r', encoding='utf-8') as file):
            content = file.read()
            new_content = content
            # 带双引号的中文内容
            chinese_sentences = chinese_sentence_pattern.findall(content)

            # 创建一个string string的dictionary
            zhToEnDict = {}
            for chinese_sentence in chinese_sentences:
                # 得到英文的Key，截取第一段
                # zhNoQuote = chinese_sentence[1:-1].split("，")[0].strip()
                firstZhSentence = re.search(r'^[^，\.\?！：；:$]+', chinese_sentence[1:-1])
                if firstZhSentence:
                    zhNoQuote = firstZhSentence.group(0).strip()
                else:
                    zhNoQuote = chinese_sentence[1:-1]
                translation = translator.translate(zhNoQuote, src='zh-cn', dest='en').text
                translation = translation.lower()
                translationUnderLine = translation.replace(" ", "_")
                # 让key唯一
                if translationUnderLine in stringEnSet:
                    random_number = random.randint(1000, 9999)
                    translationUnderLine = translationUnderLine + str(random_number)
                stringEnSet.add(translationUnderLine)

                print(zhNoQuote)
                print(translationUnderLine)
                # 替换双引号内容
                # 检查是否存在 ${xxx}的内容
                replacedSentence =  f"getString(Res.string.{translationUnderLine}"
                matches = re.compile(r'\$\{(.*?)\}').findall(chinese_sentence)
                if matches:
                    for match in matches:
                        replacedSentence+= ", " + match
                replacedSentence += ")"

                new_content = new_content.replace(chinese_sentence, replacedSentence, 1)

                # 把${} 替换成 %1$s
                placeholderMatches = re.compile(r'\$\{.*?\}').findall(chinese_sentence)
                if placeholderMatches:
                    for index, match in enumerate(placeholderMatches):
                        chinese_sentence = chinese_sentence.replace(match, f"%{index+1}$s")

                # 放到dictionary里
                zhToEnDict[translationUnderLine] = chinese_sentence[1:-1]
            return zhToEnDict, new_content
    except Exception as e:
        print(f"无法读取文件 {file_path}：{e}")
        return []

def extract_chinese_sentences_from_folder(folder_path, output_file_path):
    if not os.path.isdir(folder_path):
        print(f"错误: {folder_path} 不是一个有效的文件夹路径。")
        return

    with open(output_file_path, 'w', encoding='utf-8') as output_file:

        for root, _, files in os.walk(folder_path):
            # 遍历文件夹下的所有文件
            for file_name in files:
                if file_name.endswith('.kt'):
                    file_path = os.path.join(root, file_name)
                    # 提取文件中的中文句子列表
                    zhToEnDict, new_content = extract_chinese_sentences_from_file(file_path)
                    if zhToEnDict:
                        output_file.write("\n")
                        for enValue, zhKey in zhToEnDict.items():
                            aLine = f"<string name=\"{enValue}\">{zhKey}</string>"
                            output_file.write(aLine + '\n')
                        # 如果存在中文字符，替换文件
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.write(new_content)
                        with open(file_path, 'r', encoding='utf-8') as file:
                            lines = file.readlines()
                            lines.insert(1, "import org.jetbrains.compose.resources.getString\nimport ai.caper.hephaestus.desktopapp.generated.resources.*")
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.writelines(lines)



if __name__ == "__main__":
    # import sys
    # if len(sys.argv) != 3:
    #     print("用法: python extract_chinese_sentences.py 文件夹路径 输出文件路径")
    #     sys.exit(1)
    #
    # folder_path = sys.argv[1]
    # output_file_path = sys.argv[2]

    folder_path = "/Users/xiaohanchen/IdeaProjects/caper-repo/caper/iot_platform/hephaestus/desktopApp/src/jvmMain/kotlin/ai/caper/hephaestus/app/viewmodel/item"
    # folder_path = "/Users/xiaohanchen/IdeaProjects/caper-repo/caper/iot_platform/hephaestus/desktopApp/src/jvmMain/kotlin/ai/caper/hephaestus/app/view"
    output_file_path = "/Users/xiaohanchen/Documents/MIS/output4.txt"

    extract_chinese_sentences_from_folder(folder_path, output_file_path)