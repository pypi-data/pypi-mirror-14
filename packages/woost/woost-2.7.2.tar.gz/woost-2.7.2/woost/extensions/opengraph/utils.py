#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import re
from woost import app
from woost.models import Configuration

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

    acceptable_websites = publishable.websites

    current_website = app.website
    if current_website is not None:
        if not acceptable_websites or current_website in acceptable_websites:
            return current_website

    for website in Configuration.instance.websites:
        if not acceptable_websites or website in acceptable_websites:
            return website

