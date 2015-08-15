#-------------------------------------------------------------------------------
# Name:        nlp3
# Purpose:     言語処理100本ノック 2015
#
# Author:      TPTamada
#
# Created:     14/08/2015
# Copyright:   TPTamada 2015
# Licence:     MIT License
#-------------------------------------------------------------------------------
# Python 3.3
#-------------------------------------------------------------------------------

import re
import pprint
import numpy as np
import matplotlib.pyplot as plt
import pylab
from matplotlib.font_manager import FontProperties

def main():
    pass

#-------------------------------------------------------------------------------
##30. 形態素解析結果の読み込み
##形態素解析結果（neko.txt.mecab）を読み込むプログラムを実装せよ．
##ただし，各形態素は表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）を
##キーとするマッピング型に格納し，1文を形態素（マッピング型）のリストとして表現せよ．
##第4章の残りの問題では，ここで作ったプログラムを活用せよ．

##表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
#-------------------------------------------------------------------------------
def parseMecabFile(path):
    data = []
    sentence = []
    with open(path, "r", encoding="utf-8") as f:
        line = f.readline()
        while line:
            if line.strip() == "EOS":
                data.append(sentence)
                sentence = []
            else:
                m = re.match(u"(.+?)\t(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)", line)
                if (m):
                    sentence.append(dict(zip(("surface","base","pos","pos1"), m.group(1, 8, 2, 3))))
            line = f.readline()
    return data

##    data = parseMecabFile(path)
##    pprint.pprint(data[:5])
##    with open("neko_data.txt", "w", encoding="utf-8") as f:
##        pprint.pprint(data, f)

#-------------------------------------------------------------------------------
##31. 動詞
##動詞の表層形をすべて抽出せよ．
#-------------------------------------------------------------------------------
def verbSurface(data):
    return [word["surface"] for sentence in data for word in sentence if word["pos"] == u'動詞']

##    verb = verbSurface(data)
##    pprint.pprint(verb[:5])
##    with open("neko_verb.txt", "w", encoding="utf-8") as f:
##        pprint.pprint(verb, f)

#-------------------------------------------------------------------------------
##32. 動詞の原形
##動詞の原形をすべて抽出せよ．
#-------------------------------------------------------------------------------
def verbBase(data):
    return [word["base"] for sentence in data for word in sentence if word["pos"] == u'動詞']

##    verb = verbBase(data)
##    pprint.pprint(verb[:5])
##    with open("neko_verb_base.txt", "w", encoding="utf-8") as f:
##        pprint.pprint(verb, f)

#-------------------------------------------------------------------------------
##33. サ変名詞
##サ変接続の名詞をすべて抽出せよ．
#-------------------------------------------------------------------------------
def nounSaHen(data):
    data = [word for sentence in data for word in sentence if word["pos1"] == u'サ変接続']
    return data

#-------------------------------------------------------------------------------
##34. 「AのB」
##2つの名詞が「の」で連結されている名詞句を抽出せよ．
#-------------------------------------------------------------------------------
def aNoB(data):
    data = [word for sentence in data for word in sentence]
    return [data[i]["surface"] + u"の" + data[i+2]["surface"] for i in range(len(data)-2) if data[i]["pos"]==u"名詞" and data[i+1]["base"]==u"の" and data[i+2]["pos"]==u"名詞"]

#-------------------------------------------------------------------------------
##35. 名詞の連接
##名詞の連接（連続して出現する名詞）を最長一致で抽出せよ．
#-------------------------------------------------------------------------------
## 同じ名詞の連続
def nounRepeat(data):
    data = [word for sentence in data for word in sentence]
    res = ""
    buf = []
    for i in data:
        if buf == []:
            if i['pos'] == u'名詞':
                buf.append(i)
        else:
            if i == buf[0]:
                buf.append(i)
            else:
                bufstr = "".join([x['surface'] for x in buf])
                if len(res) < len(bufstr):
                    res = bufstr
                buf = []
    return res

## 名詞（同じとは限らない）の連続
def nounChain(data):
    data = [word for sentence in data for word in sentence]
    res = ""
    buf = []
    for i in data:
        if i['pos'] == u'名詞':
            buf.append(i)
        else:
            bufstr = "".join([x['surface'] for x in buf])
            if len(res) < len(bufstr):
                res = bufstr
            buf = []
    return res

##print(nounRepeat(data))

#-------------------------------------------------------------------------------
##36. 単語の出現頻度
##文章中に出現する単語とその出現頻度を求め，出現頻度の高い順に並べよ．
#-------------------------------------------------------------------------------
def frequency(data):
    data = [word for sentence in data for word in sentence]
    bucket = {}
    for i in data:
        val = (i['base'], i['pos'], i['pos1'])
##        val = (i['surface'], i['base'], i['pos'], i['pos1'])  #if count different surface as different word
        if val in bucket:
            bucket[val] += 1
        else:
            bucket[val] = 1
    for k in bucket.keys():
        bucket[k] /= len(data)
    return list(sorted(bucket.items(), key=lambda x:x[1], reverse=True))


#-------------------------------------------------------------------------------
##37. 頻度上位10語
##出現頻度が高い10語とその出現頻度をグラフ（例えば棒グラフなど）で表示せよ．
#-------------------------------------------------------------------------------
def showTop(freq, n=10):
    data = freq[:n]
    y = np.array([x[1] for x in data])
    x = np.array(list(range(1, n+1)))
    plt.bar(x, y, align = "center")
    fp = FontProperties(fname='..\\Ricty\\RictyDiminished-Regular.ttf')
    plt.xticks(x, [x[0][0] for x in data], fontproperties=fp)
    plt.title(u'出現頻度が高い' + str(n) + u"語" , fontdict={'fontproperties':fp})
    pylab.ylabel(u'頻度', fontdict={'fontproperties':fp})
    plt.show()

##    freq = frequency(data)
##    showTop(freq, n=20)

#-------------------------------------------------------------------------------
##38. ヒストグラム
## 単語の出現頻度のヒストグラム（横軸に出現頻度，縦軸に出現頻度をとる単語の種類数を
## 棒グラフで表したもの）を描け．
#-------------------------------------------------------------------------------
def showHistogram(freq, bins=25):
    data = np.array([x[1] for x in freq])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(data, bins=bins, log=True)
    ax.set_xlim(0, np.max(data))
    fp = FontProperties(fname='..\\Ricty\\RictyDiminished-Regular.ttf')
    ax.set_title(u'出現頻度の分布', size=16, fontdict={'fontproperties':fp})
    ax.set_xlabel(u'出現頻度', size=14, fontdict={'fontproperties':fp})
    ax.set_ylabel(u'データ個数', size=14, fontdict={'fontproperties':fp})
    plt.show()

##    freq = frequency(data)
##    showHistogram(freq)

#-------------------------------------------------------------------------------
##39. Zipfの法則
##単語の出現頻度順位を横軸，その出現頻度を縦軸として，両対数グラフをプロットせよ．
#-------------------------------------------------------------------------------
def zipf(freq):
    x = np.array(range(1, len(freq)+1))
    y = np.array([x[1] for x in freq])
    plt.scatter(x, y)
    plt.xscale('log', basex=10)
    plt.yscale('log', basey=10)
    fp = FontProperties(fname='..\\Ricty\\RictyDiminished-Regular.ttf')
    plt.title(u'Zipfの法則' , fontdict={'fontproperties':fp})
    plt.xlabel(u'出現頻度順位(log10)', fontdict={'fontproperties':fp})
    plt.ylabel(u'出現頻度(log10)', fontdict={'fontproperties':fp})
    plt.grid(which="both")
    plt.show()

##    freq = frequency(data)
##    zipf(freq)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    path = u"kusa_meikyu.txt.mecab"
    data = parseMecabFile(path)
