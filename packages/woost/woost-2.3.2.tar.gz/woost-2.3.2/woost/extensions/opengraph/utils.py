#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import re
from woost.models import Configuration, get_current_website

html_expr = re.compile(r"</?[a-z][^>]*>")
li_expr = re.compile(r"<li(\s+[^>]*)?>")
br_expr = re.compile(r"<br\s*/?>")
block_end_expr = re.compile(r"</(p|li)>")
excessive_line_jumps_expr = re.compile(r"\n{2,}")

def export_content(content):
    if content:
        content = content.replace("\r", "\n")
        content = li_expr.sub("* ", content)
        content = br_expr.sub("\n", content)
        content = block_end_expr.sub("\n", content)
        content = html_expr.sub("", content)
        content = excessive_line_jumps_expr.sub("\n", content)
        content = content.strip("\n")
    return content

def get_publishable_website(publishable):
    if publishable.websites:
        if len(publishable.websites) == 1:
            return publishable.websites[0]
        else:
            current_website = get_current_website()
            if current_website in publishable.websites:
                return current_website

    config = Configuration.instance
    if len(config.websites) == 1:
        return config.websites[0]

