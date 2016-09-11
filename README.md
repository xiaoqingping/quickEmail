# quickEmail
封装python的Email库，使其更容易使用

## 上手使用
quickEmail快速入门实例
```python
from quickEmail import quickEmail
qe = quickEmail()
# 添加发送邮件列表
qe.add_tolist('youremail@qq.com')
# 发送邮件
qe.send_mail(qe.set_mail('title', 'email body'))
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

## 待更新
### tolist配置文件化
### 支持发送附件


