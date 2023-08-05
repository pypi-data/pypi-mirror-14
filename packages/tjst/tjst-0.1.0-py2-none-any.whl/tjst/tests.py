# coding: utf-8

from __future__ import unicode_literals

from tjst import compile_text2text
import unittest
import execjs


class TestMain(unittest.TestCase):
    def test_1(self):
        text = '''
        <%
            obj['x'] = 123;
            obj['y'] = '456';
        %>
        XXX
        <% for (var key in obj) { %>
            YYY<%=obj[key]%>ZZZ
        <% } %>
        GGG
        '''
        res = 'XXXYYY111ZZZYYY123ZZZYYY456ZZZGGG'
        compiled = compile_text2text(text)
        ctx = execjs.compile('var testfunc = ' + compiled + ';')
        result = ctx.call("testfunc", {'obj': {'z': 111}}).replace('\n', '').replace(' ', '')
        self.assertEqual(result, res)
