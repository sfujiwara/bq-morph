# -*- coding: utf-8 -*-

import re
import subprocess
import pandas as pd
import numpy as np


"""
Wikipedia のページタイトルから MeCab 用の辞書を生成する.
[表層形, 左文脈ID, 右文脈ID, コスト,品詞, 品詞細分類1, 品詞細分類2, 品詞細分類3, 活用形, 活用型, 原形, 読み, 発音]
"""

print("Download wikipedia title...")

subprocess.call(
    "wget http://dumps.wikimedia.org/jawiki/latest/jawiki-latest-all-titles-in-ns0.gz -P /tmp/",
    shell=True
)
subprocess.call(
    "gunzip /tmp/jawiki-latest-all-titles-in-ns0.gz",
    shell=True
)


print("Create csv file...")

titles = np.loadtxt('/tmp/jawiki-latest-all-titles-in-ns0', dtype=str, skiprows=1)
# 数字のみを表す正規表現
patteran_num = re.compile('^[0123456789]*$')

res = []
for title in titles:
    word = title.decode('utf-8')
    # 1 文字のタイトルは除く
    if len(word) < 2:
        continue
    # 数字だけのページは除く (42 だけは救済する)
    if re.match(patteran_num, word) and word != str(42):
        continue
    # 曖昧さ回避のページは除く
    if u'曖昧さ回避' in word:
        continue
    # 作品の登場人物紹介ページは除く
    if u'登場人物' in word:
        continue
    # 何らかの一覧ページは除く
    if u'一覧' in word:
        continue
    score = int(max(-36000., -400 * len(word)**1.5))
    res.append([title, 0, 0, score, "名詞", 'wikipedia', '*', '*', '*', '*', title, '*', '*'])

df = pd.DataFrame(res)
df.to_csv("/tmp/dic-wikipedia.csv", index=False, header=False)


print("Compile dictionary...")

# sh_compile_dic_mac = """
# /usr/local/Cellar/mecab/0.996/libexec/mecab/mecab-dict-index \
#   -d /usr/local/lib/mecab/dic/ipadic \
#   -u /tmp/dic-wikipedia.dic \
#   -f utf8 \
#   -t utf8 /tmp/dic-wikipedia.csv
# """
# subprocess.call(sh_compile_dic_mac, shell=True)

sh_compile_dic_ubuntu = """
/usr/lib/mecab/mecab-dict-index \
  -d /var/lib/mecab/dic/ipadic-utf8/ \
  -u wikipedia.dic \
  -f utf8 \
  -t utf8 dic-wikipedia.csv
"""
subprocess.call(sh_compile_dic_ubuntu, shell=True)
