# -*- coding: utf-8 -*-
'''
Created on 2013-3-10
@author: Administrator
'''

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class EmailUtil(object):
    
    def __init__(self, smtpserver, smtpuser, smtppass, smtpport, debuglevel=1):
        smtp = smtplib.SMTP()
#        设定调试级别，依情况而定  
        smtp.set_debuglevel(0)
        smtp.connect(smtpserver)
        smtp.login(smtpuser, smtppass)
        self.smtp = smtp
        self.smtpuser = smtpuser
        self.smtppass = smtppass

    def sendmessage(self, to, subj, content):
 
        strTo = ' ,'.join(to)  
        
        # 设定root信息  
        msgRoot = MIMEMultipart('related')  
        msgRoot['Subject'] = subj  
        msgRoot['From'] = self.smtpuser  
        msgRoot['To'] = strTo  
        msgRoot.preamble = 'This is a multi-part message in MIME format.'  
        
        # Encapsulate the plain and HTML versions of the message body in an  
        # 'alternative' part, so message agents can decide which they want to display.  
        msgAlternative = MIMEMultipart('alternative')  
        msgRoot.attach(msgAlternative)  
        
        #设定纯文本信息  
        #        msgText = MIMEText(plainText, 'plain', 'utf-8')  
        #        msgAlternative.attach(msgText)  
        
        #设定HTML信息  
        msgText = MIMEText(content, 'html', 'utf-8')  
        msgAlternative.attach(msgText)  
        
        self.smtp.login(self.smtpuser, self.smtppass)  
        self.smtp.sendmail(self.smtpuser, to, msgRoot.as_string())  
        self.smtp.quit() 
        
    @staticmethod
    def sendmsg(to, subj, content, smtpserver='smtp.139.com'
                , smtppass=None, smtpport='25'
                , smtpuser='13764256496@139.com'):
        
        eu = EmailUtil(smtpserver, smtpuser, smtppass, smtpport)
        eu.sendmessage(to, subj, content)
        
EmailUtil.sendmsg(['13764256496@139.com'
#                   , '535521469@qq.com'
                   ], u'love', 'beibei , corleone love you forever .',
                  smtppass='8kingZW')


