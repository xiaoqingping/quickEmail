你好 {{ name }},
    这是一封发自<a href='https://github.com/xiaoqingping/quickEmail'>quickEmail</a>的邮件
    {% for number in numbers %}
        这里使用了循环，改行是第{{ number + 1 }}次循环<br />
    {% endfor %}
    欢迎你使用quickEmail，如果有疑问，请与我沟通：<a href='mailto:xiaoqingping@qq.com'>点击此处给我发送邮件</a>

