#作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
#觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools


#在oiginck.txt文件中写入stream抓到的headers
#运行后生成resultck.txt,里面是转换后的json格式headers，直接填青龙完事

#为了配合大佬的一些小毛脚本，需要转换格式

with open('oiginck.txt','r') as fp:
    pg = fp.readlines()
temp = []
for i in pg:
    tp = i.split(':')
    temp.append("\""+tp[0]+"\""+": "+"\""+tp[1].replace("\n","\"").replace(" ","")+",\n")
temp[0]="{"+temp[0]
temp[-1]=temp[-1].replace(',\n','\"')+"}"
with open('resultck.txt','w') as fp:
    fp.writelines(temp)
