# -*- utf-8 -*-
# author: xiaoqingping@qq.com
# 封装一个邮箱类
import json
import configparser
import smtplib
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from collections import OrderedDict

class quickEmail:
    # 邮件信息从配置文件中读取还是使用内置的邮件配置
    # 默认使用文件配置
    _build_in_config = False
    # 协议配置文件，默认为default.ini
    _protocol_file = 'default.ini'
    # 账号配置文件，默认为account.ini
    _account_file = 'account.ini'
    # 配置文件句柄
    _config_handler = None
    # SMTP配置
    _smtp = OrderedDict({})
    _smtp_ssl = OrderedDict({})
    # POP3配置
    _pop3 = OrderedDict({})
    _pop3_ssl = OrderedDict({})
    # IMAP配置
    _imap = OrderedDict({})
    _imap_ssl = OrderedDict({})
    # 账号
    _from = OrderedDict({})
    # 发送账号集合
    _tolist = []

    # 初始化
    def __init__(self, protocol_file=None, account_file=None):
        # 设置协议配置文件
        if protocol_file is not None:
            self._protocol_file = protocol_file

        # 设置账号配置文件
        if account_file is not None:
            self._account_file = account_file

        # 初始化配置解析器
        self._config_handler = configparser.ConfigParser()
        # 读取协议配置
        self._load_config()
        # 读取账号配置
        self._read_account()

    # 获取字符型的配置
    def _get_ini_str(self, section_name, key_name):
        if self._config_handler.has_section(section_name) and self._config_handler.has_option(section_name, key_name):
            return self._config_handler.get(section_name, key_name)
        else:
            return None

    # 获取整数型的配置
    def _get_ini_int(self, section_name, key_name):
        if self._config_handler.has_section(section_name) and self._config_handler.has_option(section_name, key_name):
            return self._config_handler.getint(section_name, key_name)
        else:
            return None

    # 填充协议字段
    def _set_protocol(self, config_item, section, default_port):
        if self._get_ini_str(section, 'server'):
            config_item['server'] = self._get_ini_str(section, 'server')
            if self._get_ini_int(section, 'port'):
                config_item['port'] = self._get_ini_int(section, 'port')
            else:
                config_item['port'] = default_port

    # 读取配置
    def _load_config(self):
        if self._protocol_file is None:
            raise '协议配置文件未设置'

        # 读取配置文件
        self._config_handler.read(self._protocol_file)

        # 读取smtp配置
        self._set_protocol(self._smtp, 'smtp', 25)
        # 读取smtp-ssl配置
        self._set_protocol(self._smtp_ssl, 'smtp-ssl', 465)
        # 读取pop3配置
        self._set_protocol(self._pop3, 'pop3', 110)
        # 读取pop3-ssl配置
        self._set_protocol(self._pop3_ssl, 'pop3-ssl', 995)
        # 读取imap配置
        self._set_protocol(self._imap, 'imap', 143)
        # 读取imap-ssl配置
        self._set_protocol(self._imap_ssl, 'imap-ssl', 993)

    # 读取邮箱账号
    def _read_account(self):
        if self._account_file is None:
            raise '账号配置文件未设置'

        self._config_handler.read(self._account_file)

        self._from['account'] = self._get_ini_str('setting', 'account')
        self._from['password'] = self._get_ini_str('setting', 'password')

    # 设置接收邮件账户列表
    def add_tolist(self, addr):
        if isinstance(addr, str):
            self._tolist.append(addr)
        elif isinstance(addr, list) or isinstance(addr, tuple) or isinstance(addr, set):
            for x in addr:
                self._tolist.append(x)
        elif isinstance(addr, dict):
            for key, value in addr:
                self._tolist.append(value)

    # 从文件中增加to list列表
    def add_tolist_from_file(self, file):
        pass

    #设置邮件格式
    def set_mail(self, title, body, mail_type='plain'):
        if mail_type == 'plain':
            msg = MIMEText(body, 'plain', 'utf-8')
        else:
            msg = MIMEMultipart()
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

        msg['From'] = self._from['account']
        msg['To'] = ', '. join(self._tolist)
        msg['Subject'] = Header(title, 'utf-8')

        return msg

    # 发送邮件
    # message: 消息体
    # ssl: 是否使用ssl发送
    def send_mail(self, message, ssl=False):
        if ssl is False:
            smtpObj = smtplib.SMTP(self._smtp['server'], self._smtp['port'])
        else:
            smtpObj = smtplib.SMTP_SSL(self._smtp_ssl['server'], self._smtp_ssl['port'])

        # 登陆邮件服务器
        smtpObj.login(self._from['account'], self._from['password'])
        # 发送邮件
        smtpObj.sendmail(self._from['account'], self._tolist, message.as_string())
        # 退出
        smtpObj.quit()

    # 接收邮件
    def recv_mail(self, protocol='pop3', ssl=False):
        pass

    # 测试打印
    def dump_config(self):
        print('smtp     setting: ', self._smtp)
        print('smtp-ssl setting: ', self._smtp_ssl)
        print('pop3     setting: ', self._pop3)
        print('pop3-ssl setting: ', self._pop3_ssl)
        print('imap     setting: ', self._imap)
        print('imap-ssl setting: ', self._imap_ssl)
        print('==================================')
        print('account:', self._from)

    def dump_tolist(self):
        print('tolist: ', self._tolist)


