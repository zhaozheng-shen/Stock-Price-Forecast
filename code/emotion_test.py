import csv
csv.field_size_limit(500 * 1024 * 1024)
import jieba
import pandas as pd

#读取文件，文件读取函数
def read_file(filename):
    with open(filename, 'r',encoding='gbk')as f:
        text = f.read()
        #返回list类型数据
        text = text.split('\n')
    return text

def reada_file(filename):
    with open(filename, 'r',encoding='utf-8')as f:
        text = f.read()
        #返回list类型数据
        text = text.split('\n')
    return text    

#去停用词函数
def del_stopwords(words):
    # 读取停用词表
    stopwords = reada_file("./词典/stopwords.txt")
    # 去除停用词后的句子
    new_words = []
    for word in words:
        if word not in stopwords:
            new_words.append(word)
    return new_words

# 获取六种权值的词，根据要求返回list，这个函数是为了配合Django的views下的函数使用
def weighted_value(request):
    result_dict = []
    if request == "one":
        result_dict = read_file("./词典/most.txt")
    elif request == "two":
        result_dict = read_file("./词典/very.txt")
    elif request == "three":
        result_dict = read_file("./词典/more.txt")
    elif request == "four":
        result_dict = read_file("./词典/ish.txt")
    elif request == "five":
        result_dict = read_file("./词典/insufficiently.txt")
    elif request == "six":
        result_dict = read_file("./词典/inverse.txt")
    elif request == 'posdict':
        result_dict = read_file("./词典/pos_all_dict.txt")
    elif request == 'negdict':
        result_dict = read_file("./词典/neg_all_dict.txt")
    else:
        pass
    return result_dict

#读取情感词典
posdict = weighted_value('posdict')
negdict = weighted_value('negdict')
# 读取程度副词词典
# 权值为2
mostdict = weighted_value('one')
# 权值为1.75
verydict = weighted_value('two')
# 权值为1.50
moredict = weighted_value('three')
# 权值为1.25
ishdict = weighted_value('four')
# 权值为0.25
insufficientdict = weighted_value('five')
# 权值为-1
inversedict = weighted_value('six')

#程度副词处理，对不同的程度副词给予不同的权重
def match_adverb(word,sentiment_value):
    #最高级权重为
    if word in mostdict:
        print(word)
        sentiment_value *= 8
    #比较级权重
    elif word in verydict:
        print(word)
        sentiment_value *= 6
    #比较级权重
    elif word in moredict:
        print(word)
        sentiment_value *= 4
    #轻微程度词权重
    elif word in ishdict:
        print(word)
        sentiment_value *= 2
    #相对程度词权重
    elif word in insufficientdict:
        print(word)
        sentiment_value *= 0.5
    #否定词权重
    elif word in inversedict:
        print(word)
        sentiment_value *= -1
    else:
        sentiment_value *= 1
    return sentiment_value


stock_name = "复星医药_总"
with open("./data/" + stock_name + ".csv") as f:
    reader = csv.reader(f)
    rows=[row for row in reader]
    news = []
    for new in rows:
        new_row = [i.encode().decode() for i in new]
        news.append(new_row)
    # print(len(news)) #news是按照行存起来的list
    # print(news[0][3]) #每行的第四个元素是新闻标题

    title = []
    read = [] 
    date = []
    author = []
    flag = 0
    for i in range(len(news)):
        if i > 1 and int(news[i][4][:2]) > int(news[i-1][4][:2]):
            flag = 1
            
        if flag == 0:
            date.append('2021-' + news[i][4][:5])
        else:
            date.append('2020-' + news[i][4][:5])
        read.append(news[i][0])
        title.append(news[i][2])
        author.append(news[i][3])

    # for i in range(len(news)): #与该关键词有关的所有新闻构成的list
    #     content.append(news[title.index(news[i])][4])
    #     date.append(news[title.index(news[i])][1][:10])
    text = []
    for i in range(len(news)): #与该关键词有关的所有新闻分词后构成的list
        text.append(jieba.lcut(title[i], cut_all=True))
    print(len(news))
    print('hhhhhh')
    print(date[-30:])
    print(read[-30:])

    new_text = [] # 去除停用词的新闻list
    poscount_list = []
    negcount_list = []
    sentiment_score = []
    for j in range(len(news)): #第j条新闻
        print('\n\n\n\n')
        print(news[j][2])
        new_text.append(del_stopwords(text[j]))
        #i，s 记录情感词和程度词出现的位置
        i = 0   #记录扫描到的词位子
        s = 0   #记录情感词的位置
        poscount = 0 #记录积极情感词数目
        negcount = 0 #记录消极情感词数目
        #逐个查找情感词
        for word in new_text[j]:
            #如果为积极词
            if word in posdict:
                temp_pos_value = 1  #情感词数目加1
                print('\npos:' + word + '+1')
                print(new_text[j][s:i])
            #在情感词前面寻找程度副词
                for w in new_text[j][s:i]: # 看情感词前面三个词以内有没有程度词
                    new_poscount = match_adverb(w,temp_pos_value)
                    if temp_pos_value != new_poscount:
                        print('pos:程度副词' + str(temp_pos_value) + '->' + str(new_poscount))
                    temp_pos_value = new_poscount
                poscount += temp_pos_value
                s = i+1 #记录情感词位置
            # 如果是消极情感词
            elif word in negdict:
                temp_neg_value = 1
                print('\nneg:' + word + '-1')
                print(new_text[j][s:i])
                for w in new_text[j][s:i]:
                    new_negcount = match_adverb(w,temp_neg_value)
                    if temp_neg_value != new_negcount:
                        print('neg:程度副词' + str(temp_neg_value) + '->' + str(new_negcount))
                    temp_neg_value = new_negcount
                negcount += temp_neg_value
                s = i+1
            #如果结尾为感叹号或者问号，表示句子结束，并且倒序查找感叹号前的情感词，权重+4
            elif word =='!' or  word =='！' or word =='?' or word == '？':
                for w2 in new_text[j][::-1]:
                    #如果为积极词，poscount+2
                    if w2 in posdict:
                        poscount += 4
                        print('pos:' + word + '+4')
                        break
                    #如果是消极词，negcount+2
                    elif w2 in negdict:
                        negcount += 4
                        # print('lll')
                        print('neg:' + word + '-4')
                        break
            i += 1 #定位情感词的位置
        #计算情感值
        print('\ntotal pos count: ' + str(poscount))
        print('total neg count: ' + str(negcount))
        poscount_list.append(poscount)
        negcount_list.append(negcount)
        sentiment_score.append(poscount_list[j] - negcount_list[j])

        # if sentiment_score[j] < 0:
        #     print('情感倾向：消极')
        #     s = '消极'
        # elif sentiment_score[j] == 0:
        #     print('情感倾向：中性')
        #     s = '中性'
        # else:
        #     print('情感倾向：积极')
        #     s = '积极'

        # print('新闻时间：{}'.format(date[j])+'\n')
        # print('情感分值：{}'.format(sentiment_score[j])+'\n') #写入情感分值
        # print('新闻内容：{}'.format(content[j])+'\n')
    j += 1    
    # 1. 写入csv文件
    out_file = './output/' + stock_name + '_out.csv'
    ff = open(out_file,'w',encoding='utf-8')

    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(ff)

    # 3. 构建列表头
    csv_writer.writerow(["date","pos","neg","read"])

    # 4. 写入csv文件内容
    for i in range(len(news)):
        csv_writer.writerow([format(date[i]),format(poscount_list[i]),format(negcount_list[i]),format(read[i])])

    # 5. 关闭文件
    ff.close()

df = pd.read_csv(out_file)
df = df.sort_values(by="date",ascending=True)
df.to_csv(out_file,index=0)

with open(out_file) as f:
    reader = csv.reader(f)
    rows=[row for row in reader]
    news = []
    for new in rows:
        new_row = [i.encode().decode() for i in new]
        news.append(new_row)

news_merge = []
news_merge.append(news[0])
news_merge.append(news[1])
news_merge[-1][1] = str(float(news_merge[-1][1]) * float(news[1][3]))
news_merge[-1][2] = str(float(news_merge[-1][2]) * float(news[1][3]))
temp_date = news[1][0]
# print(news_merge)
for i in range(2, len(news) - 1):
    if news[i][0] == temp_date:
        news_merge[-1][1] = str(float(news_merge[-1][1]) + float(news[i][1]) * float(news[i][3]))
        news_merge[-1][2] = str(float(news_merge[-1][2]) + float(news[i][2]) * float(news[i][3]))
        news_merge[-1][-1] = str(float(news_merge[-1][-1]) + float(news[i][3]))
    else:
        temp_date = news[i][0]
        add_part = news[i]
        add_part[1] = str(float(add_part[1]) * float(add_part[3]))
        add_part[2] = str(float(add_part[2]) * float(add_part[3]))
        news_merge.append(add_part)
# print(news_merge)
for i in range(1, len(news_merge)):
    news_merge[i][1] = str(float(news_merge[i][1]) / float(news_merge[i][-1]))
    news_merge[i][2] = str(float(news_merge[i][2]) / float(news_merge[i][-1]))
# print(news_merge)
date, poscount_list, negcount_list = [], [], []
for i in range(1, len(news_merge)):
    date.append(news_merge[i][0])
    poscount_list.append(float(news_merge[i][1]))
    negcount_list.append(float(news_merge[i][2]))

my_out_file = './output/' + stock_name + '_my_out.csv'
ff = open(my_out_file,'w',encoding='utf-8')
# 2. 基于文件对象构建 csv写入对象
csv_writer = csv.writer(ff)
# 3. 构建列表头
csv_writer.writerow(["date","pos","neg"])
for i in range(1, len(news_merge)):
    csv_writer.writerow([format(date[i-1]),format(poscount_list[i-1]),format(negcount_list[i-1])])
ff.close()