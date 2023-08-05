#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			March 2009
"""
import re
import htmlentitydefs
from difflib import _mdiff
from cocktail.modeling import GenericMethod
from cocktail.html import templates

def html_diff(from_sequence, to_sequence, linejunk = None, charjunk = None):

    diffs = _mdiff(
        from_sequence,
        to_sequence,
        linejunk = linejunk,
        charjunk = charjunk
    )

    from_list = []
    to_list = []

    for from_data, to_data, flag in diffs:
        from_list.append(_markup(_unescape(from_data[1])))
        to_list.append(_markup(_unescape(to_data[1])))

    return from_list, to_list

def _markup(data):
    return data \
        .replace("&", "&amp;") \
        .replace(">", "&gt;") \
        .replace("<", "&lt;") \
        .replace('\t', '&nbsp;' * 4) \
        .replace(' ', '&nbsp;') \
        .replace('\0+', '<span class="diff_add">') \
        .replace('\0-', '<span class="diff_sub">') \
        .replace('\0^', '<span class="diff_changed">') \
        .replace('\1', '</span>')

def _unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

@GenericMethod
def iter_diff_rows(self, language, source, target, source_value, target_value):
    row = templates.new("woost.views.MemberDiffRow")
    row.diff_member = self
    row.diff_language = language
    row.diff_source = source
    row.diff_target = target
    row.diff_source_value = source_value
    row.diff_target_value = target_value
    yield row

if __name__ == "__main__":
    from_seq = ["Hello universe!"]
    to_seq = ["Hello world!"]
    diffs = html_diff(from_seq, to_seq)
    print diffs

