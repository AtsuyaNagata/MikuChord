import re

#https://sakkyoku.info/beginner/determine-the-key/ を参考
chordPattern_key = [
    ["C", "Dm", "Em", "F", "G", "Am", "Bm-5"],       #キー：C or Am
    ["G", "Am", "Bm", "C", "D", "Em", "F#m-5"],      #キー：G or Em
    ["D", "Em", "F#m", "G", "A", "Bm", "C#m-5"],     #キー：D or Bm
    ["A", "Bm", "C#m", "D", "E", "F#m", "G#m-5"],    #キー：A or F#m
    ["E", "F#m", "G#m", "A", "B", "C#m", "D#m-5"],   #キー：E or C#m
    ["B", "C#m", "D#m", "E", "F#", "G#m", "A#m-5"],  #キー：B or G#m
    ["F#", "G#m", "A#m", "B", "C#", "D#m", "Fm-5"],  #キー：F# or D#m
    ["F", "Gm", "Am", "Bb", "C", "Dm", "Em-5"],      #キー：F or Dm
    ["Bb", "Cm", "Dm", "Eb", "F", "Gm", "Am-5"],     #キー：Bb or Gm
    ["Eb", "Fm", "Gm", "Ab", "Bb", "Cm", "Dm-5"],    #キー：Eb or Cm
    ["Ab", "Bbm", "Cm", "Db", "Eb", "Fm", "Gm-5"],   #キー：Ab or Fm
    ["Db", "Ebm", "Fm", "Gb", "Ab", "Bbm", "Cm-5"]   #キー：Db or A#m
]

def analysisKey(chordsText):
    chords = chordsText.split(" ")
    key_probability = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   #インデックスに対応するキーである確率が格納される
    key_probability_ans = [.0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0]
    isMajor = [False, False, False, False, False, False, False, False, False, False, False, False]
    MajorPoints = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    prevChordNums = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    #コードごとにキーに対応するコードと一致するかを確かめる
    for chord in chords:
        mChord = re.sub("M|7|/[a-zA-Z#]+|sus[0-9]|add[0-9]|\(.+?\)|9", "", chord)
        
        for i in range(12):
            for j in range(7):
                if chordPattern_key[i][j] == mChord:       #あるキーのコードと一致したら
                    key_probability[i] += 1                #そのキーに対応するインデックス値の場所の値をインクリメント
                    #メジャーコード的な進行を検知
                    if prevChordNums[i] == 0 and j == 3:
                        MajorPoints[i] += 1
                    if prevChordNums[i] == 3 and j == 4:
                        MajorPoints[i] += 1
                    if prevChordNums[i] == 4 and j == 0:
                        MajorPoints[i] += 1
                    #マイナーコード的な進行を検知
                    if prevChordNums[i] == 5 and j == 1:
                        MajorPoints[i] -= 1
                    if prevChordNums[i] == 1 and j == 2:
                        MajorPoints[i] -= 1
                    if prevChordNums[i] == 2 and j == 5:
                        MajorPoints[i] -= 1
                    prevChordNums[i] = j
                    break
                #最後の要素だったら合致するコードが見つからなかったってことになる
                if j == 6:
                    prevChordNums[i] = -1   #不正な値をいれておく

    #正規化と解析率を求めるためのカウンター
    sum = 0
    for i in key_probability:
        sum += i

    if sum < (len(chords) * 0.7):            #もし7割以下が不明なコードなら空の解答を返す
        return (key_probability_ans, isMajor)

    for i in range(12):
        if sum == 0:
            print("error : divide 0")
        key_probability_ans[i] = key_probability[i] / sum       #正規化を行う
    
    isMajor = [MajorPoint >= 0 for MajorPoint in MajorPoints]
    
    return (key_probability_ans, isMajor)
        
def writeChordMarkDown(songName, songUrl, chordsText, key_probability):
    with open("mikuChord.md", mode="a") as markdownFile:
        markdownFile.write("# **[" + songName + "](" + songUrl + ")**\n\n")
        markdownFile.write("## KeyPercentage\n")
        
        #受け取ったkeyの可能性を表示する処理
        text = ""
        if key_probability[1][0] == True:
            text += "Cメジャー："
        else :
            text += "Aマイナー："
        text += str(round(key_probability[0][0] * 100, 2)) + "％  "

        if key_probability[1][1] == True:
            text += "Gメジャー："
        else :
            text += "Eマイナー："
        text += str(round(key_probability[0][1] * 100, 2)) + "％  "

        if key_probability[1][2] == True:
            text += "Dメジャー："
        else :
            text += "Bマイナー："
        text += str(round(key_probability[0][2] * 100, 2)) + "％  "

        if key_probability[1][3] == True:
            text += "Aメジャー："
        else :
            text += "F#マイナー："
        text += str(round(key_probability[0][3] * 100, 2)) + "％  "

        if key_probability[1][4] == True:
            text += "Eメジャー："
        else :
            text += "C#マイナー："
        text += str(round(key_probability[0][4] * 100, 2)) + "％  "

        if key_probability[1][5] == True:
            text += "Bメジャー："
        else :
            text += "G#マイナー："
        text += str(round(key_probability[0][5] * 100, 2)) + "％  "

        if key_probability[1][6] == True:
            text += "F#メジャー："
        else :
            text += "D#マイナー："
        text += str(round(key_probability[0][6] * 100, 2)) + "％  "

        if key_probability[1][7] == True:
            text += "Fメジャー："
        else :
            text += "Dマイナー："
        text += str(round(key_probability[0][7] * 100, 2)) + "％  "

        if key_probability[1][8] == True:
            text += "Bbメジャー："
        else :
            text += "Gマイナー："
        text += str(round(key_probability[0][8] * 100, 2)) + "％  "

        if key_probability[1][9] == True:
            text += "Ebメジャー："
        else :
            text += "Cマイナー："
        text += str(round(key_probability[0][9] * 100, 2)) + "％  "

        if key_probability[1][10] == True:
            text += "Abメジャー："
        else :
            text += "Fマイナー："
        text += str(round(key_probability[0][10] * 100, 2)) + "％  "

        if key_probability[1][11] == True:
            text += "Dbメジャー："
        else :
            text += "A#マイナー："
        text += str(round(key_probability[0][11] * 100, 2)) + "％  "

        markdownFile.write(text + "\n\n")
        
        #一番可能性が高いキーを特別に表示
        maxNum = max(key_probability[0])
        maxIndex = key_probability[0].index(maxNum)
        text = "## **"
        #表示するインデックスが指定されてること以外は上の処理と同様
        if maxIndex == 0:
            if key_probability[1][0] == True:
                text += "Cメジャー："
            else :
                text += "Aマイナー："
            text += str(round(key_probability[0][0] * 100, 2)) + "％"
        
        if maxIndex == 1:
            if key_probability[1][1] == True:
                text += "Gメジャー："
            else :
                text += "Eマイナー："
            text += str(round(key_probability[0][1] * 100, 2)) + "％"

        if maxIndex == 2:
            if key_probability[1][2] == True:
                text += "Dメジャー："
            else :
                text += "Bマイナー："
            text += str(round(key_probability[0][2] * 100, 2)) + "％"

        if maxIndex == 3:
            if key_probability[1][3] == True:
                text += "Aメジャー："
            else :
                text += "F#マイナー："
            text += str(round(key_probability[0][3] * 100, 2)) + "％"
        
        if maxIndex == 4:
            if key_probability[1][4] == True:
                text += "Eメジャー："
            else :
                text += "C#マイナー："
            text += str(round(key_probability[0][4] * 100, 2)) + "％"

        if maxIndex == 5:
            if key_probability[1][5] == True:
                text += "Bメジャー："
            else :
                text += "G#マイナー："
            text += str(round(key_probability[0][5] * 100, 2)) + "％"

        if maxIndex == 6:
            if key_probability[1][6] == True:
                text += "F#メジャー："
            else :
                text += "D#マイナー："
            text += str(round(key_probability[0][6] * 100, 2)) + "％"

        if maxIndex == 7:
            if key_probability[1][7] == True:
                text += "Fメジャー："
            else :
                text += "Dマイナー："
            text += str(round(key_probability[0][7] * 100, 2)) + "％"

        if maxIndex == 8:
            if key_probability[1][8] == True:
                text += "Bbメジャー："
            else :
                text += "Gマイナー："
            text += str(round(key_probability[0][8] * 100, 2)) + "％"

        if maxIndex == 9:
            if key_probability[1][9] == True:
                text += "Ebメジャー："
            else :
                text += "Cマイナー："
            text += str(round(key_probability[0][9] * 100, 2)) + "％"
        
        if maxIndex == 10:
            if key_probability[1][10] == True:
                text += "Abメジャー："
            else :
                text += "Fマイナー："
            text += str(round(key_probability[0][10] * 100, 2)) + "％"
        
        if maxIndex == 11:
            if key_probability[1][11] == True:
                text += "Dbメジャー："
            else :
                text += "A#マイナー："
            text += str(round(key_probability[0][11] * 100, 2)) + "％"
        text += "**"
        markdownFile.write(text + "\n\n")

        chords = chordsText.split(" ")
        markdownFile.write("### **")
        for i, chord in enumerate(chords):
            if i == len(chords) - 1:
                markdownFile.write(chord)
            else:
                markdownFile.write(chord + " | ")

        markdownFile.write("**\n<br>\n\n")

        #予測したキーに応じてローマ数字表記に書き換える
        singles = ['Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ']
        minorSingles = ['Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅰ', 'Ⅱ']
        markdownFile.write("## 予測結果\n\n**")
        for i, chord in enumerate(chords):
            isKeyChord = False              #キーに含まれないコードは赤で表示する
            isOne = False                   #コードがⅠだったときにTrueになる
            isFour = False                  #コードがⅣだったとき
            isFive = False                  #コードがⅤだったとき
            isDominant = False              #前回のコードから5度下(4度上)のコードに進行するのを検知したらTrueにする
            numberChordName = chord         #もし書き換え不可だった時、元のコードを出力する
            mChord = re.sub("M|7|/[a-zA-Z#]+|sus[0-9]|add[0-9]|\(.+?\)|9", "", chord)
            for j in range(7):
                if chordPattern_key[maxIndex][j] == mChord:       #あるキーのコードと一致したら
                    isKeyChord = True                             #キーに属するコードだと分かったのでTrueにする
                    #次のコードが強進行的なニュアンスを含んでいたら
                    if i < len(chords) - 1:
                        if re.sub("M|7|/[a-zA-Z#]+|sus[0-9]|add[0-9]|\(.+?\)|9", "", chords[i + 1]) == chordPattern_key[maxIndex][(j + 3) % 7]:
                            isDominant = True
                    if key_probability[1][maxIndex] == True:       #メジャーコードだったら
                        if j == 0:
                            isOne = True                              #Ⅰだと分かったのでTrue
                        if j == 3:
                            isFour = True
                        if j == 4:
                            isFive = True
                        numberChordName = chord.replace(mChord ,singles[j])
                    else :
                        if j == 5:
                            isOne = True                              #Ⅰだと分かったのでTrue
                        if j == 1:
                            isFour = True
                        if j == 2:
                            isFive = True
                        numberChordName = chord.replace(mChord ,minorSingles[j])
            
            #コードの情報を書く前に、特定のコードを着色する処理を入れる
            if isKeyChord == False:
                    markdownFile.write("<font color=\"Red\">")
            elif isOne == True:
                    markdownFile.write("<font color=\"Lime\">")
            elif isFour == True:
                    markdownFile.write("<font color=\"Aqua\">")
            elif isFive == True:
                    markdownFile.write("<font color=\"Coral\">")

            #コードを書く処理
            if i == len(chords) - 1:
                markdownFile.write(numberChordName)
                #着色する処理の後処理(最後の出力以外の「|」を記述する処理のために後処理は2重化を許容してる)
                if isKeyChord == False or isOne == True or isFour == True or isFive == True:
                    markdownFile.write("</font>")
            else:
                markdownFile.write(numberChordName)
                #着色する処理の後処理
                if isKeyChord == False or isOne == True or isFour == True or isFive == True:
                    markdownFile.write("</font>")
                if isDominant == True:
                    markdownFile.write("<font color=\"DeepPink\">")
                    markdownFile.write(" -> ")
                    markdownFile.write("</font>")
                else :
                    markdownFile.write(" | ")

        markdownFile.write("**\n<br>\n\n")
    
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def chordTransitionStatistics(chordsText, key_probability, chordTransisionPercentage):
    maxNum = max(key_probability[0])
    maxIndex = key_probability[0].index(maxNum)
    chords = chordsText.split(" ")
    for i, chord in enumerate(chords):
        for j in range(7):
            mChord = re.sub("M|7|/[a-zA-Z#]+|sus[0-9]|add[0-9]|\(.+?\)|9", "", chord)
            if chordPattern_key[maxIndex][j] == mChord:
                #次のコードを調べる
                if i < len(chords) - 1:
                    for k in range(7):
                        if re.sub("M|7|/[a-zA-Z#]+|sus[0-9]|add[0-9]|\(.+?\)|9", "", chords[i + 1]) == chordPattern_key[maxIndex][k]:
                            chordTransisionPercentage[j][k] += 1
    return chordTransisionPercentage

def retFirstChord(chordsText, key_probability):
    singles = ['Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ']
    minorSingles = ['Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅰ', 'Ⅱ']
    #一番可能性が高いキーを取得
    maxNum = max(key_probability[0])
    maxIndex = key_probability[0].index(maxNum)
    mChord = re.sub("M|7|/[a-zA-Z#]+|sus[0-9]|add[0-9]|\(.+?\)|9", "", chordsText.split(" ")[0])
    for j in range(7):
        if chordPattern_key[maxIndex][j] == mChord:       #あるキーのコードと一致したら
            if key_probability[1][maxIndex] == True:       #メジャーコードだったら
                numberChordName = singles[j]
            else :                                         #マイナーコードだったら
                numberChordName = minorSingles[j]
            return numberChordName
    
    return ""

def min_max(x, axis=None):
    min = x.min(axis=axis, keepdims=True)
    max = x.max(axis=axis, keepdims=True)
    result = (x-min)/(max-min)
    return result

def writeChordStatistics(chordTransisionPercentage, firstChordNums):
    chordTransitionPercentage_normal = min_max(chordTransisionPercentage)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("chord number before transition")
    ax.set_ylabel("chord number after transition")
    ax.set_zlabel("Normalized probability")
    X1, X2 = np.mgrid[0:7, 0:7]
    """before = [3,0,4,1,5,2,6]
    after = [2,5,1,4,0,3,6]
    chord_sp = np.zeros((7, 7), dtype=float)
    for i in range(7):
        for j in range(7):
            chord_sp[i][j] = chordTransitionPercentage_normal[before[i]][after[j]]
    print(chord_sp)
    print()
    print(chordTransitionPercentage_normal)"""
    surf = ax.plot_surface(X1, X2, chordTransitionPercentage_normal, cmap="plasma", facecolor="w")
    plt.xticks([0,1,2,3,4,5,6], ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ"])
    plt.yticks([0,1,2,3,4,5,6], ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ"])
    #plt.xticks([0,1,2,3,4,5,6], ["Ⅳ", "Ⅰ", "Ⅴ", "Ⅱ", "Ⅵ", "Ⅲ", "Ⅶ"])
    #plt.yticks([0,1,2,3,4,5,6], ["Ⅲ", "Ⅵ", "Ⅱ", "Ⅴ", "Ⅰ", "Ⅳ", "Ⅶ"])
    fig.colorbar(surf)
    ax.set_title("chord transition statistics plot")
    plt.show()
    fig.savefig("chordTransitionImage.png")
    
    with open("mikuChordStatistics.md", mode="w") as sFile:
        singles = ['Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ']
        chordTransitionPercentage_line = np.zeros((7, 7), dtype=float)
        sFile.write("# **初音ミク関係の曲のコード遷移確率**\n")
        sFile.write("## コード遷移の比重を表した画像\n")
        sFile.write("![コード遷移の統計画像](chordTransitionImage.png)\n")
        sFile.write("\n<br>\n\n")
        for i in range(7):
            sum = 0.0
            for j in range(7):
                sum += chordTransitionPercentage_normal[i][j]
            for j in range(7):
                chordTransitionPercentage_line[i][j] = chordTransitionPercentage_normal[i][j] / sum
        for i in range(7):
            sFile.write("## **" + singles[i] + "からの遷移確率**\n")
            for j in range(7):
                sFile.write("### **" + singles[j] + " : " + str(chordTransitionPercentage_line[i][j]*100) + "％**\n")
            sFile.write("\n<br>\n\n")

        sFile.write("## **開始のコード確率**\n")
        sum = 0
        for key in firstChordNums:
            if key != "":
                sum += firstChordNums[key]
        for key in firstChordNums:
            if key != "":
                sFile.write("### **" + key + " : " + str(float(firstChordNums[key]) / sum * 100) + "％**\n")
            else:
                sFile.write("### 有効なコード数 : " +  str(sum) + "\n")
                sFile.write("### 無効なコード数 : " +  str(firstChordNums[key]))
        sFile.write("\n<br>\n\n")

#メインの処理
with open("mikuChord.txt") as f:
    lines = [s.strip() for s in f.readlines()]
    with open("mikuChord.md", mode="w") as markdownFile:
        markdownFile.write("")
        print("マークダウンファイルをクリアしました")
    chordTransisionPercentage = np.zeros((7, 7), dtype=int)
    firstChordNums = {'Ⅰ':0, 'Ⅱ':0, 'Ⅲ':0, 'Ⅳ':0, 'Ⅴ':0, 'Ⅵ':0, 'Ⅶ':0, '':0}
    for oneLineText in lines:
        lineTexts = oneLineText.split(",", 2)       #区切るのは名前とURLとコード列の三つだけ、後の要素はコード進行なので分割しないでおく
        songName = lineTexts[0]
        songUrl = lineTexts[1]
        chordsText = lineTexts[2]
        key_probability = analysisKey(chordsText)
        writeChordMarkDown(songName, songUrl, chordsText, key_probability)
        firstChordNums[retFirstChord(chordsText, key_probability)] += 1
        #統計を出すための処理
        chordTransisionPercentage = chordTransitionStatistics(chordsText, key_probability, chordTransisionPercentage)
    
    writeChordStatistics(chordTransisionPercentage, firstChordNums)
    