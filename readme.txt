1. 文件夹内容：

code
  - 词典  # 做新闻内容的情感分析的词典，被emotion_test.py调用。
  - 实验结果.xlsx  # 实验结果总表。
  - data  # 所需要的所有数据，涵盖三只股票（复星医药、恒瑞医药、沃森生物）。
          # 每只股票包含“*_热帖资讯”表示热帖新闻，格式为csv及xlsx；
          # “*_资讯”表示资讯新闻，格式为csv及xlsx；
          # “*_总”表示热帖新闻和资讯新闻的整合，格式为csv及xlsx；
          # “*.csv”表示股票数据。
  - emotion_test.py  # 新闻情感分析代码，运行方式：python3 emotion_test.py。
                     # 输入参数：103行stock_name = 所需新闻csv格式。
  - nohup.txt  # emotion_test.py输出结果展示。
  - output  # 代码输出，涵盖三只股票（复星医药、恒瑞医药、沃森生物），涵盖三种新闻类型（热帖、新闻、合并热帖新闻）。
            # 每只股票包含“*_out.csv”表示新闻情感分析输出；
            # “*_my_out.csv”及“*_my_out1.csv”表示“*_out.csv”合并同一天的输出；
  - readme.txt
  - stock_prediction.ipynb  # 通过新闻和股票预测股价的总代码，为.ipynb格式，需在jupyter notebook上运行。
                            # 参数：
                            # stock_name = "复星医药"  # 股票名称（复星医药、恒瑞医药、沃森生物）
                            # news_name = stock_name + "_总"  # 新闻类型（热帖资讯、资讯、总）
                            # news_method = 2  # 是否加入新闻 {0: 加入前一天新闻；1: 加入当天新闻；2: 不加入}
                            # inner_merge = False  # 是否将没有新闻的那天的新闻设置成与前一天新闻一样
                                                   # {True: 否；False: 是}
  - 验证情感分析准确性.ipynb  # 验证每条新闻标题的情感分析值与股市收盘价的趋势是否基本一致，并画出趋势图。


ppt
  - proposal.pptx
  - proposal.pdf
  - midterm.pptx
  - midterm.pdf
  - final.pptx
  - final.pdf
report
  - proposal.docx
  - proposal.pdf
  - midterm.docx
  - midterm.pdf
  - final_report.docx
  - final_report.pdf

2. 代码运行顺序：
首先python3 emotion_test.py进行情感分析
然后在Jupiter上运行stock_prediction.ipynb