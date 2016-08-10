# -*- coding: utf-8 -*-

import MeCab
import json
import requests


TWEET_FILE = requests.get(
    "http://metadata.google.internal/computeMetadata/v1/instance/attributes/tweet-file",
    headers={"Metadata-Flavor": "Google"}
).content
PATH_MECAB_DIC = "/tmp/wikipedia.dic"
mt = MeCab.Tagger("-u {}".format(PATH_MECAB_DIC))
# mt = MeCab.Tagger()


def text_to_morph(text):
    node = mt.parseToNode(text)
    d = {"resource": text, "tokens": []}
    while node:
        feature = node.feature.split(",")
        if len(feature) < 9:
            feature.extend([None, None])
        token = {
            "surface": node.surface,
            "pos": feature[0],
            "pos_detail1": feature[1],
            "pos_detail2": feature[2],
            "pos_detail3": feature[3],
            "base_form": feature[6],
            "reading": feature[7],
            # "pronunciation": feature[8],
        }
        d["tokens"].append(token)
        node = node.next
    return d


output = open("morph_{}".format(TWEET_FILE), "w")
for i, line in enumerate(open("/tmp/{}".format(TWEET_FILE), 'r')):
    res = json.dumps(text_to_morph(json.loads(line)["Text"].encode("utf-8")), ensure_ascii=False)
    output.write("{}\n".format(res))
    if i % 1000 == 0: print i
output.close()
