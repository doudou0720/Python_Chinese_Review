import stardict as sd

#cl = r'D:\Downloads\ECDICT-master\dict_'+ input("input:l(large)(Have problems) m(middle) or s(small)(unrecommend)") +'.db'
cl = r'D:\doudou\dic_en\dict_l.db'
ru = sd.StarDict(cl,True).match(input())
if ru != []:
    print("查询成功!")
    for i in range(len(ru)):
        print(i," : ",ru[i][1]," NO.",ru[i][0])
print(sd.StarDict(cl,True).query(input("Input the word you want to know")))