#-------------------------------------------------------------------------------
# Name:        nlp4
# Purpose:     言語処理100本ノック 2015
#
# Author:      TPTamada
#
# Created:     14/08/2015
# Copyright:   TPTamada 2015
# Licence:     MIT License
#-------------------------------------------------------------------------------
import re
import pprint

def main():
    pass
#-------------------------------------------------------------------------------
##40. 係り受け解析結果の読み込み（形態素）
##形態素を表すクラスMorphを実装せよ．
##このクラスは表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）を
##メンバ変数に持つこととする．
##さらに，CaboChaの解析結果（neko.txt.cabocha）を読み込み，
##各文をMorphオブジェクトのリストとして表現し，3文目の形態素列を表示せよ．
#-------------------------------------------------------------------------------
class Morph:
    """Morpheme data"""
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1
    def __str__(self):
##        return u"%s (%s) [%s-%s]" % (self.surface, self.base, self.pos, self.pos1)
        return u"%s, %s, %s, %s" % (self.surface, self.base, self.pos, self.pos1)

def getMorphData(path):
##    表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
    data = []
    sentence = []
    with open(path, "r") as f:
        line = f.readline().decode("utf-8")
        while(line):
            if line.strip() == u"EOS":
                data.append(sentence)
                sentence = []
            else:
                m = re.match("(.+)\t(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)", line)
                if m:
                    sentence.append(Morph(*m.group(1,8,2,3)))
            line = f.readline().decode("utf-8")
    return data

#-------------------------------------------------------------------------------
##41. 係り受け解析結果の読み込み（文節・係り受け）
##40に加えて，文節を表すクラスChunkを実装せよ．
##このクラスは形態素（Morphオブジェクト）のリスト（morphs），係り先文節インデックス番号（dst），
##係り元文節インデックス番号のリスト（srcs）をメンバ変数に持つこととする．
##さらに，入力テキストのCaboChaの解析結果を読み込み，１文をChunkオブジェクトのリストとして表現し，
##8文目の文節の文字列と係り先を表示せよ．第5章の残りの問題では，ここで作ったプログラムを活用せよ．
#-------------------------------------------------------------------------------
class Chunk:
    def __init__(self, morphs=None, dst=-1, srcs=None):
        self.morphs = morphs if morphs else []
        self.dst = int(dst)
        self.srcs = srcs if srcs else []
    def __str__(self):
        return u"".join([x.surface for x in self.morphs]) + u" -> " + self.dst
    def chunkStr(self):
        return u"".join([x.surface for x in self.morphs])
    def addMorph(self, morph):
        self.morphs.append(morph)
    def setSrcs(self, sentence):
        if not self in sentence:
            return
        else:
            num = sentence.index(self)
            self.srcs = [sentence.index(x) for x in sentence if x.dst == num]

def getChunkData(path):
##    * 1 2D 0/1 -0.764522
##    表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
    data = []
    sentence = []
    chunk = None
    with open(path, "r") as f:
        line = f.readline().decode("utf-8")
        while(line):
            if line.strip() == u"EOS":
##                chunk-end
                if chunk:
                    sentence.append(chunk)
##                sentence-end
                for c in sentence:
                    c.setSrcs(sentence)
                data.append(sentence)


##                empty variables for next sentence
                sentence = []
                chunk = None
            else:
                m = re.match("\* \d+ (-?\d+)D", line)
                if m:
                    if chunk:
                        sentence.append(chunk)
                    chunk = Chunk(dst = m.group(1))
                else:
                    m = re.match("(.+)\t(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)", line)
                    if m:
                        chunk.addMorph(Morph(*m.group(1,8,2,3)))
            line = f.readline().decode("utf-8")


    return data

##    s = data[7]
##    for i in range(len(s)):
##        print(str(i) + ": " + s[i].__str__())
##    print "-------"

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


if __name__ == '__main__':
    path = "neko.txt.cabocha"
    data = getChunkData(path)
    s = data[7]
    for i in range(len(s)):
        print (str(i) + ": " + s[i].chunkStr()),
        print s[i].srcs,
        print s[i].dst
    print "-------"
