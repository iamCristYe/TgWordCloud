# from https://zhuanlan.zhihu.com/p/138356932

import matplotlib.pyplot as plt  # 数据可视化
import jieba  # 词语切割
import wordcloud  # 分词
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS  # 词云，颜色生成器，停止词
import numpy as np  # 科学计算
from PIL import Image  # 处理图片
import os
import json


def read_stopword(fpath):
    # 读取中文停用词表
    with open(fpath, "r", encoding="utf-8") as file:
        stopword = file.readlines()
    return [word.replace("\n", "") for word in stopword]


def ciyun(index):
    data = json.load(open("result.json"))
    with open(
        f"result_{index}_{data['chats']['list'][index]['name']}.txt", "r"
    ) as f:  # 打开新的文本转码为gbk
        textfile = f.read()  # 读取文本内容
    wordlist = jieba.lcut(textfile)  # 切割词语
    space_list = " ".join(wordlist)  # 空格链接词语
    # print(space_list)
    background = np.array(Image.open("Tg.png"))

    # 加载多个停用词表
    path = os.path.dirname(os.path.realpath(__file__))

    name_list = [
        "stopwords_baidu.txt",
        "stopwords_cn.txt",
        "stopwords_hit.txt",
        "stopwords_scu.txt",
        "stopwords_tg.txt",
    ]

    stop_word = []
    for fname in name_list:
        stop_word += read_stopword(os.path.join(path, fname))

    wc = WordCloud(
        width=2000,
        height=2000,
        background_color="white",
        mode="RGB",
        mask=background,  # 添加蒙版，生成指定形状的词云，并且词云图的颜色可从蒙版里提取
        max_words=500,
        stopwords=stop_word,  # STOPWORDS.add('link text mention 的'),#内置的屏蔽词,并添加自己设置的词语
        font_path="/mnt/c/Windows/Fonts/msyhl.ttc",
        max_font_size=150,
        relative_scaling=0.6,  # 设置字体大小与词频的关联程度为0.4
        random_state=50,
        scale=2,
    ).generate(space_list)

    image_color = ImageColorGenerator(background)  # 设置生成词云的颜色，如去掉这两行则字体为默认颜色
    wc.recolor(color_func=image_color)

    plt.imshow(wc)  # 显示词云
    plt.axis("off")  # 关闭x,y轴
    plt.show()  # 显示
    wc.to_file(f"result_{index}_{data['chats']['list'][index]['name']}.png")  # 保存词云图


def main():
    data = json.load(open("result.json"))
    for index, list_item in enumerate(data["chats"]["list"]):
        if list_item["type"] != "saved_messages":
            print(f"{index} {list_item['name']} {len(list_item['messages'])}")
            out = open(f"result_{index}_{list_item['name']}.txt", "a")
            for message in list_item["messages"]:
                if str(message["text"]) != "":
                    out.write(str(message["text"]) + "\n")
            try:
                ciyun(index)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
