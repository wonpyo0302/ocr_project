import warnings
warnings.simplefilter("ignore")
import konlpy
from konlpy.corpus import kolaw, kobill
from konlpy.tag import * # 한국어 형태소 분석 모듈
# print(kolaw.fileids())
kobill_list = kobill.fileids()
okt = Okt()

# koTxt2 = kolaw.open('constitution.txt').read()
for i in range(2,len(kobill_list)):
    print(str(i)+"번째 키워드 추출")
    koTxt = kobill.open(kobill_list[i]).read()

    # okt.nouns # 명사 추출
    # okt.morphs # 형태소 추출
    # okt.pos # 품사 부착
    txt = okt.pos(koTxt)

    # 형태소 분석 및 필터링을 통한 자연어 처리
    filter_words = [word[0] for word in txt if word[1] not in ['Josa', 'Foreign', 'Number', 'Punctuation','Verb','Adjective'] and len(word[0]) != 1]

    # 불용어 리스트 불러오기
    stopwords =  open("stopword.txt",'r',encoding='utf8')
    stopword = stopwords.read().split("\n")
    stopwords.close()

    # 필터링된 단어들 중 불용어를 찾아 삭제
    cleaned_words = [word for word in filter_words if word not in stopword]

    # 빈도수 산출
    import collections
    word_count = collections.Counter(cleaned_words)
    # 최고 빈도수 기준 상위 100개 추출
    word_top = word_count.most_common(100)
    print(word_top)
    print(" ")
