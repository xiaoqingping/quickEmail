# -*- coding:utf-8 -*-
# author: xiaoqingping@qq.com
# 发送纯文本邮件，无配置文件

from quickEmail.quickEmail import quickEmail

# 创建一个qe实例
qe = quickEmail(config_from='nofile',
                protocol_config=
                {
                    "smtp-ssl": {
                        "server": "smtp.qq.com",
                        "port": "465"
                    }
                },
                account_config=
                {
                    "account":"xiaoqingping@qq.com",
                    "password":"nztkkucqwmktbiba"
                })

qe.dump_config()

# 设置邮件接收列表
qe.add_tolist(['xiaoqingping@qq.com'])
# 设置邮件内容，邮件默认是纯文本邮件
qe.set_mail('标题：测试邮件', '这是一个纯文本邮件 sent by quickEmail', mail_type='plain')
# 发送邮件
qe.send_mail(ssl=True)

