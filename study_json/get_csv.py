import json
import pandas as pd
from tools.file_utils import GetNum, Param
import pprint

# 定义文件地址, 卡牌描述, 卡牌信息, 返回的错误值
json_filename = 'data/ThMod_Seles_cards-zh.json'
output_csv_filename = 'out/output1.csv'
descriptions = []
cards_info = []
strange_num = -999
cost_str = ''
str1 = ''
str2 = ''

# 读取json文件，添加异常处理
try:
    with open(json_filename, encoding='utf-8') as f:
        all_cards_data = json.load(f)
except FileNotFoundError:
    print(f"Error: File '{json_filename}' not found.")
    exit()


# 创建设置费用变化的字符串
def create_cost_str():
    global cost_str
    if cost2 == 0:
        cost_str = f'{cost1}'
    else:
        if cost2 == -1:
            cost_str = f'{cost1}->{0}'
        else:
            cost_str = f'{cost1}->{cost2}'


# 遍历all_cards_data这个字典对象, 获取每个键和值
# 键: java对象名, 值: 卡牌名称和描述
for java_name, card_data in all_cards_data.items():
    # 获取卡牌名称和描述
    card_id = card_data.get('NAME', None)
    description = card_data.get('DESCRIPTION', None)

    # 判断卡牌是否有升级后描述
    # 如果存在'UPGRADE_DESCRIPTION'且这个键且其值不为空, 就创建新描述
    if 'UPGRADE_DESCRIPTION' in card_data and card_data['UPGRADE_DESCRIPTION']:
        description = card_data['UPGRADE_DESCRIPTION']

    # 依次从{对象名.java}中获取对应的参数值
    magic_num = GetNum.get_param_number(java_name, Param.Magic)
    block_num = GetNum.get_param_number(java_name, Param.Block)
    damage_num = GetNum.get_param_number(java_name, Param.Damage)

    # 依次从{对象名.java}中获取对应的升级参数值
    magic_upgrade = GetNum.get_upgrade_number(java_name, Param.Magic)
    block_upgrade = GetNum.get_upgrade_number(java_name, Param.Block)
    damage_upgrade = GetNum.get_upgrade_number(java_name, Param.Damage)

    # 将描述对象转化为字符串
    desc = str(description)

    # 分别判断参数是否不存在, 然后替换升级前后描述
    if magic_num != strange_num:
        str1 = desc.replace(" !M! ", str(magic_num))
        str2 = desc.replace(" !M! ", str(magic_num + magic_upgrade))
    if block_num != strange_num:
        str1 = desc.replace(" !B! ", str(block_num))
        str2 = desc.replace(" !B! ", str(block_num + block_upgrade))
    if damage_num != strange_num:
        str1 = desc.replace(" !D! ", str(damage_num))
        str2 = desc.replace(" !D! ", str(damage_num + damage_upgrade))

    # 获取卡牌费用及升级后费用
    cost1 = GetNum.get_cost_number(java_name)
    cost2 = GetNum.get_upgrade_number(java_name, Param.BaseCost, True)

    # 调用获取费用描述字符串的函数
    create_cost_str()

    # 创建卡牌信息的字典
    card_info = {"名称": str(card_id), "费用": cost_str, "描述": str1, "升级描述": str2}

    # 将所有卡牌信息的字典添加到字符串
    cards_info.append(card_info)

"这段可以在控制台打印预览卡牌信息"
# pprint.pprint(cards_info)

# 将字符串转化为DataFrame数据对象, 并将其转化为csv文件,这里如果提取的是英文json就将gbk改为utf-8
df1 = pd.DataFrame(cards_info)
df1.to_csv(output_csv_filename, index=False, encoding='gbk')
