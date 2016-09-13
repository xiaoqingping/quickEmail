from quickEmail.quickEmail import quickEmail

try:
    qe = quickEmail()
except Exception as error:
    print(error)

qe.add_tolist('xiaoqingping@qq.com')
qe.add_tolist('xiaoqingping2001@163.com')
qe.dump_tolist()

qe.send_mail(qe.set_mail('This is a email send by Python', 'This is content'), ssl=True)