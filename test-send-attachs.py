# -*- coding:utf-8 -*-
# author: xiaoqingping@qq.com
# 发送多个附件

from quickEmail import quickEmail

# 创建一个qe实例
qe = quickEmail()
# 设置邮件接收列表
qe.add_tolist(['xiaoqingping@qq.com'])
# 添加附件列表
qe.add_attach_list(['1.jpeg', 'test.tpl', 'default.ini'])
# 设置邮件内容，邮件默认是纯文本邮件
qe.set_mail('标题：测试邮件',
            '''
            <font style="color:red;">这是一个带多个附件的邮件</font> sent by <b>quickEmail</b>
            ''',
            mail_type='attach')
# 发送邮件
qe.send_mail(ssl=True)