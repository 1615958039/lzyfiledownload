import re
import requests
import json
import os
print("\n\n\n----开始----\n\n\n")
url = input("请输入蓝奏云盘分享链接：")
while "https://www.lanzous.com/" not in url:
    url = input("请输入蓝奏云盘分享链接：")

session = requests.session()
headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "cache-control":"max-age=0",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3672.400 QQBrowser/10.4.3448.400"
}
res = session.get(url,headers=headers)
html = res.text
info = re.findall('<td width="330" valign="top">(.*?)</td>',html,re.S)
info = info[0].replace("\n","")
info = info.replace("\t","")
info = info.split("<br>")
文件名 = re.findall('<div class="b">(.*?)</div>',html,re.S)[0]
文件大小 = re.findall('</span>(.*?)$',info[0],re.S)[0]
上传时间 = re.findall('</span>(.*?)$',info[1],re.S)[0]
分享用户 = re.findall('<font>(.*?)</font>',info[2],re.S)[0]
文件描述 = info[5]
iframe = re.findall('<iframe(.*?)src="(.*?)"(.*?)></iframe>',html,re.S)
url = "https://www.lanzous.com"+iframe[0][1]
head2 = {
    "x-requested-with": "XMLHttpRequest",
    "origin": "https://www.lanzous.com",
    "referer": url,
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "cache-control":"max-age=0",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3672.400 QQBrowser/10.4.3448.400"
}
file = session.get(url,headers=headers)
file = file.text

zz = re.findall("'(.*?)';",file,re.S)
f_a = zz[0]
f_id = zz[1]
f_ih = zz[2]
f_in = zz[3]

downurl = session.post("https://www.lanzous.com/ajaxm.php",headers=head2,data={"action":f_a,"file_id":f_id,"t":f_ih,"k":f_in,"c":""})
urldata = json.loads(downurl.text)
url = urldata['dom']+"/file/"+urldata['url']+"="
h5 = session.get(url,headers=headers,allow_redirects=False)
直链 = h5.headers['Location']

print("\n\n请确认您要下载的文件:\n文件名:"+文件名+"\n文件大小:"+文件大小+"\n上传时间:"+上传时间+"\n分享用户:"+分享用户+"\n文件描述:"+文件描述+"\n\n下载直链: "+直链+"\n\n(按回车键即可下载)")
inpu = input("是否下载(Y/N 默认Y):")
if inpu!="n" and inpu!="N":
    # filename = re.findall('&q=(.*?)[$|&]',直链,re.S)[0]
    src=session.get(直链,headers=head2)
    url = '''C://py_download/'''+文件名
    if not os.path.exists('''C://py_download/'''):
        os.makedirs('''C://py_download/''')
    with open(url,'wb') as f:
        f.write(src.content)
    print("\n\n下载结束！\n\n\n")
else:
    print("已取消下载！")
