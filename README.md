# quickEmail
封装python的Email库，使其更容易使用

## 支持功能
1、发送纯文本邮件\<br>
2、发送HTML文本邮件\<br>
3、发送单附件邮件\<br>
4、发送多附件邮件\<br>
5、发送邮件模板

## 上手使用
quickEmail快速入门实例
```python
from quickEmail import quickEmail
qe = quickEmail()
# 添加发送邮件列表
qe.add_tolist('youremail@qq.com')
# 构造邮件
qe.set_mail('title', 'email content')
# 发送邮件
qe.send_mail(ssl=True)
```

## 配置文件
quickEmail默认有两个配置文件：
`default.ini` : 配置邮件服务器参数，包含SMTP、POP3和IMAP协议参数
`account.ini` : 配置邮件账号
这两个文件都可以修改：
```python
qe = quickEmail(protocol_file='server.ini', account_file='youraccount.ini')
```
在quickEmail中，我们内置了常用的邮件服务器参数，可以在built-in目录下查看到。

## 群发邮件
`qe.add_tolist()`不仅支持单个邮件的添加，还支持使用list、set、tuple和dict添加
其中dict使用的是其每个项的value
```python
qe.add_tolist(['abc@example.com', 'def@example.com'])
```

## 使用SSL
在邮件服务器中配置smtp-ssl、pop3-ssl等参数
在发送邮件时，send_mail增加一个ssl=True的参数即可
```python
qe.send_mail(qe.set_mail('title', 'email body'), ssl=True)
```

## 使用模板
导入`from template import Template`, 例子：
```python
from quickEmail import quickEmail
from template import Template

# 创建一个qe实例
qe = quickEmail()
# 设置邮件接收列表
qe.add_tolist(['youremail@qq.com'])
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
```

## 发送附件
quickEmail支持发送附件。无论是单个附件、多个附件或者是某个路径下的所有文件（不支持多层嵌套）
发送单个附件：`qe.add_attach(filename)`\<br>
多个附件：`qe.add_attach_list([file list])`\<br>
某个路径下的所有文件：`qe.add_attach_path(pathname)`

## 待更新
### tolist配置文件化


