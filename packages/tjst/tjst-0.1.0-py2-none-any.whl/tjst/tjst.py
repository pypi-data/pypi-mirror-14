# coding: utf-8

from __future__ import with_statement
from __future__ import unicode_literals

import os
import sys
import traceback
import execjs

__all__ = ['compile_text2text', 'compile_file2file']

ROOT = os.path.dirname(os.path.abspath(__file__))


def iter_files(src, exts):
    if os.path.isfile(src):
        yield src, os.path.basename(src)
    elif os.path.isdir(src):
        prefix_len = None
        for root, dirs, files in os.walk(src):
            if prefix_len is None:
                prefix_len = len(root) + 1
            prefix = root[prefix_len:]
            for tpl in files:
                if ('*' in exts) or ('.' in tpl and tpl.rsplit('.', 1)[-1] in exts):
                    yield os.path.join(root, tpl), os.path.join(prefix, tpl)


def error2str():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    info = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    return info


def compile_text2text(text):
    with open(os.path.join(ROOT, 'tjst.js')) as f:
        compiler = f.read()
        ctx = execjs.compile(compiler)
        return ctx.call("tpl2code", text)


def compile_file2file(src, dst, exts):
    with open(os.path.join(ROOT, 'tjst.js')) as f:
        parts = [f.read()]
    parts.append('var templates = {};')
    for tpl_path, tpl_name in iter_files(src, exts):
        with open(tpl_path) as tpl:
            tpl_text = tpl.read().decode('utf-8')
        try:
            prefix = 'templates["%s"] = ' % tpl_name
            parts.append(prefix + compile_text2text(tpl_text) + ';')
        except:
            print >> sys.stderr, 'There is error in %s template' % tpl_path
            print >> sys.stderr, error2str()
            raise
    with open(dst, 'w') as of:
        of.write('\n'.join(parts).encode('utf-8'))
