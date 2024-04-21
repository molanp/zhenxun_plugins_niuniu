import random
import ujson
import os
import base64
import asyncio
import time
from PIL import Image
from io import BytesIO
from pathlib import Path
from decimal import Decimal as de
from .image_utils import BuildMat
from typing import List, Union

IMAGE_PATH = Path(__file__).resolve().parent / "image"


def pic2b64(pic: Image) -> str:
    """
    说明:
        PIL图片转base64
    参数:
        :param pic: 通过PIL打开的图片文件
    """
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return "base64://" + base64_str


def random_long():
    """
    注册随机牛牛长度
    """
    return de(str(f"{random.randint(1,9)}.{random.randint(00,99)}"))

def hit_glue(l): 
  l -= de(1)
  return de(abs(de(random.random())*l/de(2))).quantize(de("0.00"))

def fence(rd):
    """

    根据比例减少/增加牛牛长度
    Args:
        rd (decimal): 精确计算decimal类型或float,int
    """
    rd -= de(time.localtime().tm_sec % 10)
    if rd > 1000000:
      return de(rd - de(random.randint(0.13, 0.34))*rd)
    return de(abs(rd*de(random.random()))).quantize(de("0.00"))


def round_numbers(data, num_digits=2):
    """
    递归地四舍五入所有数字

    Args:
        data (any): 要处理的数据
        num_digits (int, optional): 四舍五入的小数位数. Defaults to 2.

    Returns:
        any: 处理后的数据
    """
    if isinstance(data, dict):
        return {k: round_numbers(v, num_digits) for k, v in data.items()}
    elif isinstance(data, list):
        return [round_numbers(item, num_digits) for item in data]
    elif isinstance(data, (int, float)):
        return round(data, num_digits)
    else:
        return data


def ReadOrWrite(file, w=None):
    """
    读取或写入文件

    Args:
        file (string): 文件路径，相对于脚本
        w (any, optional): 写入内容，不传入则读. Defaults to None.

    Returns:
        any: 文件内容(仅读取)
    """
    file_path = Path(__file__).resolve().parent / file
    if w is not None:
        # 对要写入的内容进行四舍五入处理
        w_rounded = round_numbers(w)
        with file_path.open("w", encoding="utf-8") as f:
            f.write(ujson.dumps(w_rounded, indent=4, ensure_ascii=False))
        return True
    else:
        with file_path.open("r", encoding="utf-8") as f:
            return ujson.loads(f.read().strip())


def get_all_users(group):
    """
    获取全部用户及长度
    """
    return ReadOrWrite("data/long.json")[group]


def fencing(my, oppo, at, qq, group, content={}):
    """
    击剑判断

    Args:
        my (decimal): 精确计算decimal类型或float,int
        oppo (decimal): 精确计算decimal类型或float,int
        at (str): 被at的人qq号
        qq (str): 自己的qq号
        group (str): 当前群号
        content (dic): 数据
    """
    # 损失比例
    RdLimit = de(0.25)
    # 吞噬比例
    GtLimit = de(0.27)
    probability = random.randint(1, 100)
    if oppo <= -100 and my > 0 and 10 < probability <= 20:
        oppo = de(0.85)*oppo
        my -= abs(RdLimit*my)
        result = f"对方身为魅魔诱惑了你，你同化成魅魔！当前长度{my}cm!"
    elif oppo >= 100 and my > 0 and 10 < probability <= 20:
        oppo = de(0.85)*oppo
        my -= abs(GtLimit*my)
        result = f"对方以牛头人的荣誉摧毁了你的牛牛！当前长度{my}cm!"
    elif my <= -100 and oppo > 0 and 10 < probability <= 20:
        my = de(0.85)*my
        oppo -= abs(RdLimit*oppo)
        result = f"你身为魅魔诱惑了对方，吞噬了对方部分长度！当前长度{my}cm!"
    elif my >= 100 and oppo > 0 and 10 < probability <= 20:
        my = de(0.85)*my
        oppo -= abs(GtLimit*oppo)
        result = f"你以牛头人的荣誉摧毁了对方的牛牛！当前长度{my}cm!"
    else:
        if oppo > my:
            probability = random.randint(1, 100)
            if 0 < probability <= 60:
                reduce = fence(my)
                my -= reduce
                oppo += reduce*de(0.8)
                if my < 0:
                    result = random.choice([
                        f"哦吼！？看来你的牛牛因为击剑而凹进去了呢！凹进去了{reduce}cm！",
                        f"由于对方击剑技术过于高超，造成你的牛牛凹了进去呢！凹进去了深{reduce}cm哦！",
                        f"好惨啊，本来就不长的牛牛现在凹进去了呢！凹进去了{reduce}cm呢！"
                    ])
                else:
                    result = f"对方以绝对的长度让你屈服了呢！你的长度减少{reduce}cm，当前长度{my}cm！"

            else:
                reduce = fence(oppo)
                oppo -= reduce
                my += reduce*de(0.8)
                if my < 0:
                    result = random.choice([
                        f"哦吼！？你的牛牛在长大欸！长大了{reduce}cm！",
                        f"牛牛凹进去的深度变浅了欸！变浅了{reduce}cm！"
                    ])
                else:
                    result = f"虽然你不够长，但是你逆袭了呢！你的长度增加{reduce}cm，当前长度{my}cm！"
        elif my > oppo:
            probability = random.randint(1, 100)
            if 0 < probability <= 73:
                reduce = fence(oppo)
                oppo -= reduce
                reduce = reduce*de(0.8)
                my += reduce
                if my < 0:
                    result = random.choice([
                        f"哦吼！？你的牛牛在长大欸！长大了{reduce}cm！",
                        f"牛牛凹进去的深度变浅了欸！变浅了{reduce}cm！"
                    ])
                else:
                    result = f"你以绝对的长度让对方屈服了呢！你的长度增加{reduce}cm，当前长度{my}cm！"
            else:
                reduce = fence(my)
                oppo += reduce*de(0.8)
                my -= reduce
                if my < 0:
                    result = random.choice([
                        f"哦吼！？看来你的牛牛因为击剑而凹进去了呢！目前深度{reduce}cm！",
                        f"由于对方击剑技术过于高超，造成你的牛牛凹了进去呢！当前深度{reduce}cm！",
                        f"好惨啊，本来就不长的牛牛现在凹进去了呢！凹进去了{reduce}cm！"
                    ])
                else:
                    result = f"虽然你比较长，但是对方逆袭了呢！你的长度减少{reduce}cm，当前长度{my}cm！"
        else:
            probability = random.randint(1, 100)
            reduce = fence(oppo)
            if 0 < probability <= 50:
                oppo -= reduce
                reduce = reduce*de(0.8)
                my += reduce
                if my < 0:
                    result = random.choice([
                        f"哦吼！？你的牛牛在长大欸！长大了{reduce}cm！",
                        f"牛牛凹进去的深度变浅了欸！变浅了{reduce}cm！"
                    ])
                else:
                    result = f"你以技艺的高超让对方屈服啦🎉！你的长度增加{reduce}cm，当前长度{my}cm！"
            else:
                oppo += reduce*de(0.8)
                my -= reduce
                if my < 0:
                    result = random.choice([
                        f"哦吼！？看来你的牛牛因为击剑而凹进去了呢🤣🤣🤣！目前深度{reduce}cm！",
                        f"由于对方击剑技术过于高超，造成你的牛牛凹了进去呢😰！当前深度{reduce}cm！",
                        f"好惨啊，本来就不长的牛牛现在凹进去了呢😂！凹进去了{reduce}cm！"
                    ])
                else:
                    result = f"由于对方击剑技术过于高超，你的长度减少{reduce}cm，当前长度{my}cm！"
    content[group][qq] = my
    content[group][at] = oppo
    ReadOrWrite("data/long.json", content)
    return result


async def init_rank(
    title: str, all_user_id: List[int], all_user_data: List[float], group_id: int, total_count: int = 10
) -> BuildMat:
    """
    说明:
        初始化通用的数据排行榜
    参数:
        :param title: 排行榜标题
        :param all_user_id: 所有用户的qq号
        :param all_user_data: 所有用户需要排行的对应数据
        :param group_id: 群号，用于从数据库中获取该用户在此群的昵称
        :param total_count: 获取人数总数
    """
    _uname_lst = []
    _num_lst = []
    for i in range(len(all_user_id) if len(all_user_id) < total_count else total_count):
        _max = max(all_user_data)
        max_user_id = all_user_id[all_user_data.index(_max)]
        all_user_id.remove(max_user_id)
        all_user_data.remove(_max)
        try:
          # 暂未找到nonebot方法获取群昵称
            user_name = max_user_id
        except AttributeError:
            user_name = f"{max_user_id}"
        _uname_lst.append(user_name)
        _num_lst.append(_max)
    _uname_lst.reverse()
    _num_lst.reverse()
    return await asyncio.get_event_loop().run_in_executor(
        None, _init_rank_graph, title, _uname_lst, _num_lst
    )


def _init_rank_graph(
    title: str, _uname_lst: List[str], _num_lst: List[Union[int, float]]
) -> BuildMat:
    """
    生成排行榜统计图
    :param title: 排行榜标题
    :param _uname_lst: 用户名列表
    :param _num_lst: 数值列表
    """
    image = BuildMat(
        y=_num_lst,
        y_name="* 可以在命令后添加数字来指定排行人数 至多 50 *",
        mat_type="barh",
        title=title,
        x_index=_uname_lst,
        display_num=True,
        x_rotate=30,
        background=[
            f"{IMAGE_PATH}/{x}"
            for x in os.listdir(f"{IMAGE_PATH}")
        ],
        bar_color=["*"],
    )
    image.gen_graph()
    return image