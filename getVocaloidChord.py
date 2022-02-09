import requests
from bs4 import BeautifulSoup
import time

#指定されたchordWikiのurlからコードを抽出して半角空白で分割したテキストとして返す関数
def getChordText(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    chords = soup.select("span.chord")
    words = ""
    for t in chords:
        words += t.get_text() + " "
    return words

chordWiki_url = "https://ja.chordwiki.org"
#Chord Wikiの初音ミクタグのurl
load_url = "https://ja.chordwiki.org/tag/%E5%88%9D%E9%9F%B3%E3%83%9F%E3%82%AF"
page = 1


f = open('mikuChord.txt', 'w')

#html = requests.get(load_url)
#soup = BeautifulSoup(html.content, "html.parser")

#songLinks = soup.select(".note li a")
#songLinks = [url.get('href') for url in soup.find_all('a')]
#print(songLinks)

#print([t.get_text(strip = True) for t in songLinks])
#print([t["href"] for t in songLinks])

#初音ミクタグのあるページを参考にする(最終ページが40だったので固定値として41を格納している)
for i in range(1, 41):
    print(load_url + "?p=" + str(i))
    mikuChordHtml = requests.get(load_url + "?p=" + str(i))
    mikuSoup = BeautifulSoup(mikuChordHtml.content, "html.parser")
    songLinks = mikuSoup.select(".note li a")
    #あるページ内で回収した全ての曲のリンクにいて名前とその曲のリンクとコードの書き込みを行っていくループ
    for t in songLinks:
        #f.write(t.get_text(strip = True) + " " + chordWiki_url + t["href"])
        song_url = chordWiki_url + str(t["href"])
        text = song_url.encode("cp932", "ignore")       #ここは多分いらないけど念のためcp932文字コード(shift_Jsiの改良みたいな文字コード)の例外を弾いてる
        encodeText_url = text.decode("cp932")
        name_and_url = (t.get_text(strip = True) + "," + encodeText_url).encode("cp932", "ignore")
        encodeText_name_url = name_and_url.decode("cp932")
        print(encodeText_name_url)
        f.write(encodeText_name_url + ",")
        chordsTexts = getChordText(encodeText_url + "\n")
        text = chordsTexts.encode("cp932", "ignore")
        encodeText_chord = text.decode("cp932")
        print(encodeText_chord)
        f.write(encodeText_chord + "\n")
