#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
class SimpleMailerSender:
    def __init__(self,host,from_account,password,encoding=None):
        self.host=host
        self.from_account=from_account
        self.password=password
        self.encoding=encoding or "utf-8"

    def send(self,to,sub,content):
        to_list=[to,]
        # me="hello1"+"<"+mail_user+"@"+mail_postfix+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
        me=self.from_account
        msg = MIMEText(content,_subtype='html',_charset=self.encoding)    #创建一个实例，这里设置为html格式邮件
        msg['Subject'] = sub    #设置主题
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            s = smtplib.SMTP()
            s.connect(self.host)  #连接smtp服务器
            s.login(self.from_account,self.password)  #登陆服务器
            s.sendmail(me, to_list, msg.as_string())  #发送邮件
            s.close()
            return True
        except Exception, e:
            print str(e)
            return False
if __name__ == '__main__':

    mailer=SimpleMailerSender("smtp.189.cn","13809522353@189.cn","xxxx")
    mailer.send("1726950105@qq.com","test title","test contetn")
