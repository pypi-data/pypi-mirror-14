#-*- encoding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

class MailSender():
    def __init__(self,host,from_account,password,encoding=None,debuglevel=None):
        self.host=host
        self.from_account=from_account
        self.password=password
        self.encoding=encoding or "utf-8"
        self.debuglevel=debuglevel or 0

    # def ma
    def send(self,to,subject,content,attach_filepath,attach_filename):
        smtp = SMTP_SSL(self.host)
        smtp.set_debuglevel(self.debuglevel)
        smtp.ehlo(self.host)
        smtp.login(self.from_account,self.password)
        msg=MIMEMultipart()
        msg["Subject"] = Header(subject,self.encoding)
        msg["from"] = self.from_account
        msg["to"] = to
        #正文
        body =  MIMEText(content,"plain",self.encoding)
        msg.attach(body)
        #附件

        att1 = MIMEText(open(attach_filepath, 'rb').read())
        att1["Content-Type"] = 'application/octet-stream'
        #att1["charset"] = 'gbk'
        att1["Content-Disposition"] = 'attachment; filename="%s"' % attach_filename#这里的filename可以任意写，写什么名字，邮件中显示什么名字
        msg.attach(att1)

        smtp.sendmail(self.from_account, to, msg.as_string())

        smtp.quit()
if __name__ == '__main__':
    sender=MailSender('smtp.189.cn','12345678900@189.cn','111111')
    sender.send("1726950105@qq.com","标题","内容","out.wav","文件.wav")