# -*- coding: utf-8 -*-
# tested on Python 3.5.1
import io
import os
import re
import tokenize

class CodeBuilder:
    INDENT_STEP = 4     # 每次缩进的空格数

    def __init__(self, indent=0):
        self.indent = indent    # 当前缩进
        self.lines = []         # 保存一行一行生成的代码

    def forward(self):
        """缩进前进一步"""
        self.indent += self.INDENT_STEP

    def backward(self):
        """缩进后退一步"""
        self.indent -= self.INDENT_STEP

    def add(self, code):
        self.lines.append(code)

    def add_line(self, code):
        self.lines.append(' ' * self.indent + code)

    def __str__(self):
        """拼接所有代码行后的源码"""
        return '\n'.join(map(str, self.lines))

    def __repr__(self):
        """方便调试"""
        return str(self)


class Template:
    def __init__(self, raw_text, indent=0, default_context=None,
                 func_name='__func_name', result_var='__result',
                 template_dir='', encoding='utf-8', auto_escape=True,
                 safe_attribute=True):
        self.raw_text = raw_text
        self.default_context = default_context or {}
        self.func_name = func_name
        self.result_var = result_var
        self.template_dir = template_dir
        self.encoding = encoding
        self.code_builder = code_builder = CodeBuilder(indent=indent)
        self.buffered = []
        self.auto_escape = auto_escape
        self.default_context.setdefault('escape', escape)
        self.default_context.setdefault('noescape', noescape)
        self.safe_attribute = safe_attribute

        # 变量
        self.re_variable = re.compile(r'\{\{ .*? \}\}')
        # 注释
        self.re_comment = re.compile(r'\{# .*? #\}')
        # 标签
        self.re_tag = re.compile(r'\{% .*? %\}')
        # 用于按变量，注释，标签分割模版字符串
        self.re_tokens = re.compile(r'''(
            (?:\{\{ .*? \}\})
            |(?:\{\# .*? \#\})
            |(?:\{% .*? %\})
        )''', re.VERBOSE)
        # extends
        self.re_extends = re.compile(r'\{% extends (?P<name>.*?) %\}')
        # blocks
        self.re_blocks = re.compile(
            r'\{% block (?P<name>\w+) %\}'
            r'(?P<code>.*?)'
            r'\{% endblock \1 %\}', re.DOTALL)
        # block.super
        self.re_block_super = re.compile(r'\{\{ block\.super \}\}')

        # 生成 def __func_name():
        code_builder.add_line('def {}():'.format(self.func_name))
        code_builder.forward()
        # 生成 __result = []
        code_builder.add_line('{} = []'.format(self.result_var))
        # 解析模版
        self._parse_text()

        self.flush_buffer()
        # 生成 return "".join(__result)
        code_builder.add_line('return "".join({})'.format(self.result_var))
        code_builder.backward()

    def _parse_text(self):
        """解析模版"""
        # extends
        self._handle_extends()

        tokens = self.re_tokens.split(self.raw_text)
        handlers = (
            (self.re_variable.match, self._handle_variable),   # {{ variable }}
            (self.re_tag.match, self._handle_tag),             # {% tag %}
            (self.re_comment.match, self._handle_comment),     # {# comment #}
        )
        default_handler = self._handle_string                  # 普通字符串

        for token in tokens:
            for match, handler in handlers:
                if match(token):
                    handler(token)
                    break
            else:
                default_handler(token)

    def _handle_variable(self, token):
        """处理变量"""
        variable = token.strip('{} ')
        if self.auto_escape:
            self.buffered.append('escape({})'.format(variable))
        else:
            self.buffered.append('str({})'.format(variable))

    def _handle_comment(self, token):
        """处理注释"""
        pass

    def _handle_string(self, token):
        """处理字符串"""
        self.buffered.append('{}'.format(repr(token)))

    def _handle_tag(self, token):
        """处理标签"""
        # 将前面解析的字符串，变量写入到 code_builder 中
        # 因为标签生成的代码需要新起一行
        self.flush_buffer()
        tag = token.strip('{%} ')
        tag_name = tag.split()[0]
        if tag_name == 'include':
            self._handle_include(tag)
        else:
            self._handle_statement(tag)

    def _handle_statement(self, tag):
        """处理 if/for"""
        tag_name = tag.split()[0]
        if tag_name in ('if', 'elif', 'else', 'for'):
            # elif 和 else 之前需要向后缩进一步
            if tag_name in ('elif', 'else'):
                self.code_builder.backward()
            # if True:, elif True:, else:, for xx in yy:
            self.code_builder.add_line('{}:'.format(tag))
            # if/for 表达式部分结束，向前缩进一步，为下一行做准备
            self.code_builder.forward()
        elif tag_name in ('break',):
            self.code_builder.add_line(tag)
        elif tag_name in ('endif', 'endfor'):
            # if/for 结束，向后缩进一步
            self.code_builder.backward()

    def _handle_include(self, tag):
        filename = tag.split()[1].strip('"\'')
        included_template = self._parse_another_template_file(filename)
        # 把解析 include 模版后得到的代码加入当前代码中
        # def __func_name():
        #    __result = []
        #    ...
        #    def __func_name_hash():
        #        __result_hash = []
        #        return ''.join(__result_hash)
        self.code_builder.add(included_template.code_builder)
        # 把上面生成的代码中函数的执行结果添加到原有的结果中
        # __result.append(__func_name_hash())
        self.code_builder.add_line(
            '{0}.append({1}())'.format(
                self.result_var, included_template.func_name
            )
        )

    def _parse_another_template_file(self, filename):
        template_path = os.path.realpath(
            os.path.join(self.template_dir, filename)
        )
        name_suffix = str(hash(template_path)).replace('-', '_')
        func_name = '{}_{}'.format(self.func_name, name_suffix)
        result_var = '{}_{}'.format(self.result_var, name_suffix)
        with open(template_path, encoding=self.encoding) as fp:
            template = self.__class__(
                fp.read(), indent=self.code_builder.indent,
                default_context=self.default_context,
                func_name=func_name, result_var=result_var,
                template_dir=self.template_dir,
                auto_escape=self.auto_escape
            )
        return template

    def _handle_extends(self):
        match_extends = self.re_extends.match(self.raw_text)
        if match_extends is None:
            return

        parent_template_name = match_extends.group('name').strip('"\' ')
        parent_template_path = os.path.join(
            self.template_dir, parent_template_name
        )
        # 获取当前模版里的所有 blocks
        child_blocks = self._get_all_blocks(self.raw_text)
        # 用这些 blocks 替换掉父模版里的同名 blocks
        with open(parent_template_path, encoding=self.encoding) as fp:
            parent_text = fp.read()
        new_parent_text = self._replace_parent_blocks(
            parent_text, child_blocks
        )
        # 改为解析替换后的父模版内容
        self.raw_text = new_parent_text

    def _replace_parent_blocks(self, parent_text, child_blocks):
        """用子模版的 blocks 替换掉父模版里的同名 blocks"""
        def replace(match):
            name = match.group('name')
            parent_code = match.group('code')
            child_code = child_blocks.get(name, '')
            child_code = self.re_block_super.sub(parent_code, child_code)
            new_code = child_code or parent_code
            return new_code
        return self.re_blocks.sub(replace, parent_text)

    def _get_all_blocks(self, text):
        """获取模版内定义的 blocks"""
        return {
            name: code
            for name, code in self.re_blocks.findall(text)
        }

    def flush_buffer(self):
        # 生成类似代码: __result.extend(['<h1>', name, '</h1>'])
        line = '{0}.extend([{1}])'.format(
            self.result_var, ','.join(self.buffered)
        )
        self.code_builder.add_line(line)
        self.buffered = []

    def render(self, context=None):
        """渲染模版"""
        namespace = {}
        namespace.update(self.default_context)
        namespace.setdefault('__builtins__', {})
        if context:
            namespace.update(context)
        code = str(self.code_builder)
        if self.safe_attribute:
            check_unsafe_attributes(code)
        exec(code, namespace)
        func = namespace[self.func_name]
        result = func()
        return result


class NoEscape:

    def __init__(self, raw_text):
        self.raw_text = raw_text


html_escape_table = {
    '&': '&amp;',
    '"': '&quot;',
    '\'': '&apos;',
    '>': '&gt;',
    '<': '&lt;',
}


def html_escape(text):
    return ''.join(html_escape_table.get(c, c) for c in text)


def escape(text):
    if isinstance(text, NoEscape):
        return str(text.raw_text)
    else:
        text = str(text)
        return html_escape(text)


def noescape(text):
    return NoEscape(text)


def check_unsafe_attributes(string):
    g = tokenize.tokenize(io.BytesIO(string.encode('utf-8')).readline)
    pre_op = ''
    for toktype, tokval, _, _, _ in g:
        if toktype == tokenize.NAME and pre_op == '.' and \
                tokval.startswith('_'):
            attr = tokval
            msg = "access to attribute '{0}' is unsafe.".format(attr)
            raise AttributeError(msg)
        elif toktype == tokenize.OP:
            pre_op = tokval