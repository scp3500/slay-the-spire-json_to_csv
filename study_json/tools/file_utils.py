import re
from enum import Enum


class GetNum:

    @staticmethod
    def get_param_number(name, param):
        java_code = GetNum.load_json(name)

        # 使用正则表达式匹配第一次出现的 this.baseMagicNumber 的赋值语句
        match = re.search(fr'this\.base{param.value}\s*=\s*(\d+)', java_code)

        if match:
            num = int(match.group(1))
        else:
            num = -999
        return num

    @staticmethod
    def get_upgrade_number(name, param, is_cost=False):
        java_code = GetNum.load_json(name)

        # 使用正则表达式匹配第一次出现的 this.baseMagicNumber 的赋值语句
        match = re.search(fr'upgrade{param.value}\((-?\d+)', java_code)

        if match:
            num = int(match.group(1))
            if is_cost and num == 0:
                num = -1
        else:
            num = 0
        return num

    @staticmethod
    def load_json(name):
        # Java 文件路径
        java_file_path = f'data/cards/{name}.java'
        # 读取 Java 文件内容
        with open(java_file_path, 'r', encoding='utf-8') as java_file:
            java_code = java_file.read()
        return java_code

    @staticmethod
    def get_cost_number(name):
        file_path = f'data/cards/{name}.java'  # 替换为实际的文件路径

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 使用正则表达式匹配 super 行中的数字
        match1 = re.search(fr'{name}\.png", (\d+),', content)
        match2 = re.search(fr'IMG_PATH, (\d+),', content)
        if match1:
            num= match1.group(1)
        elif match2:
            num = match2.group(1)
        else:
            num = 'X'
        return num


class Param(Enum):
    Magic = "MagicNumber"
    Damage = "Damage"
    Block = "Block"
    BaseCost = "BaseCost"
