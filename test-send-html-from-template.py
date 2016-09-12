# -*- coding:utf-8 -*-
# author: xiaoqingping@qq.com
# 使用模板

from quickEmail import quickEmail
from template import Template

# 创建一个qe实例
qe = quickEmail()
# 设置邮件接收列表
qe.add_tolist(['xiaoqingping@qq.com'])
# 打开模板文件，读取模板内容
tpl_text = open('default.tpl', encoding='utf-8').read()
# 解析模板
tpl = Template(tpl_text)
# 渲染数据，生成最终结果
text = tpl.render({'name': '陈先生', 'numbers': range(5)})

# 设置邮件内容，邮件默认是纯文本邮件
qe.set_mail('标题：这是一个模板文件', text, mail_type='plain')
# 发送邮件
qe.send_mail(ssl=True)
