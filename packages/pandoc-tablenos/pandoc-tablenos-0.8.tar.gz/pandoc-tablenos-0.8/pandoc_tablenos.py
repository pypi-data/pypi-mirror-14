#! /usr/bin/env python

"""pandoc-tablenos: a pandoc filter that inserts table nos. and refs."""

# Copyright 2015, 2016 Thomas J. Duck.
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# OVERVIEW
#
# The basic idea is to scan the AST twice in order to:
#
#   1. Insert text for the table number in each table caption.
#      For LaTeX, insert \label{...} instead.  The table labels
#      and associated table numbers are stored in the global
#      references tracker.
#
#   2. Replace each reference with a table number.  For LaTeX,
#      replace with \ref{...} instead.
#
# There is also an initial scan to do some preprocessing.

import re
import functools
import itertools
import io
import sys

# pylint: disable=import-error
import pandocfilters
from pandocfilters import stringify, walk
from pandocfilters import RawInline, Str, Space, Para, Table, Plain, Cite
from pandocattributes import PandocAttributes

# Patterns for matching attributes, labels and references
ATTR_PATTERN = re.compile(r'(.*)\{(.*)\}')
LABEL_PATTERN = re.compile(r'(tbl:[\w/-]*)(.*)')
REF_PATTERN = re.compile(r'@(tbl:[\w/-]+)')

# Detect python 3
PY3 = sys.version_info > (3,)

# Pandoc uses UTF-8 for both input and output; so must we
if PY3:  # Force utf-8 decoding (decoding of input streams is automatic in py3)
    STDIN = io.TextIOWrapper(sys.stdin.buffer, 'utf-8', 'strict')
    STDOUT = io.TextIOWrapper(sys.stdout.buffer, 'utf-8', 'strict')
else:    # No decoding; utf-8-encoded strings in means the same out
    STDIN = sys.stdin
    STDOUT = sys.stdout

# pylint: disable=invalid-name
references = {}  # Global references tracker

def is_attrtable(key, value):
    """True if this is an attributed table; False otherwise."""
    try:
        s = stringify(value[0]).strip()
        return key == 'Table' and ATTR_PATTERN.match(s)
    # pylint: disable=bare-except
    except:
        return False

def parse_attrtable(value):
    """Parses an attributed table."""
    # Extract the attribute string.  There may be text immediately in front
    # of the attribute string that we will need to retain.

    caption, content = value[0], value[1:]
    c, s = ATTR_PATTERN.match(caption[-1]['c']).groups()
    if not c:
        caption = caption[:-1]
        if caption and caption[-1]['t'] == 'Space':
            caption = caption[:-1]
    else:
        caption[-1]['c'] = c
    # Extract label from the attributes (label, classes, kvs)
    label = PandocAttributes(s, 'markdown').to_pandoc()[0]
    if label == 'tbl:': # Make up a unique description
        label = label + '__'+str(hash(str(content)))+'__'
    return content, caption, label

def is_ref(key, value):
    """True if this is a table reference; False otherwise."""
    return key == 'Cite' and REF_PATTERN.match(value[1][0]['c']) and \
            parse_ref(value)[1] in references

def parse_ref(value):
    """Parses a table reference."""
    prefix = value[0][0]['citationPrefix']
    label = REF_PATTERN.match(value[1][0]['c']).groups()[0]
    suffix = value[0][0]['citationSuffix']
    return prefix, label, suffix

def ast(string):
    """Returns an AST representation of the string."""
    toks = [Str(tok) for tok in string.split()]
    spaces = [Space()]*len(toks)
    ret = list(itertools.chain(*zip(toks, spaces)))
    if string[0] == ' ':
        ret = [Space()] + ret
    return ret if string[-1] == ' ' else ret[:-1]

def is_broken_ref(key1, value1, key2, value2):
    """True if this is a broken link; False otherwise."""
    try:     # Pandoc >= 1.16
        return key1 == 'Link' and value1[1][0]['t'] == 'Str' \
          and value1[1][0]['c'].endswith('{@tbl') \
            and key2 == 'Str' and '}' in value2
    except TypeError:  # Pandoc < 1.16
        return key1 == 'Link' and value1[0][0]['t'] == 'Str' \
           and value1[0][0]['c'].endswith('{@tbl') \
            and key2 == 'Str' and '}' in value2

def repair_broken_refs(value):
    """Repairs references broken by pandoc's --autolink_bare_uris."""

    # autolink_bare_uris splits {@tbl:label} at the ':' and treats
    # the first half as if it is a mailto url and the second half as a string.
    # Let's replace this mess with Cite and Str elements that we normally
    # get.
    flag = False
    for i in range(len(value)-1):
        if value[i] == None:
            continue
        if is_broken_ref(value[i]['t'], value[i]['c'],
                         value[i+1]['t'], value[i+1]['c']):
            flag = True  # Found broken reference
            try:  # Pandoc >= 1.16
                s1 = value[i]['c'][1][0]['c']  # Get the first half of the ref
            except TypeError:  # Pandoc < 1.16
                s1 = value[i]['c'][0][0]['c']  # Get the first half of the ref
            s2 = value[i+1]['c']           # Get the second half of the ref
            ref = '@tbl' + s2[:s2.index('}')]  # Form the reference
            prefix = s1[:s1.index('{@tbl')]    # Get the prefix
            suffix = s2[s2.index('}')+1:]      # Get the suffix
            # We need to be careful with the prefix string because it might be
            # part of another broken reference.  Simply put it back into the
            # stream and repeat the preprocess() call.
            if i > 0 and value[i-1]['t'] == 'Str':
                value[i-1]['c'] = value[i-1]['c'] + prefix
                value[i] = None
            else:
                value[i] = Str(prefix)
            # Put fixed reference in as a citation that can be processed
            value[i+1] = Cite(
                [{"citationId":ref[1:],
                  "citationPrefix":[],
                  "citationSuffix":[Str(suffix)],
                  "citationNoteNum":0,
                  "citationMode":{"t":"AuthorInText", "c":[]},
                  "citationHash":0}],
                [Str(ref)])
    if flag:
        return [v for v in value if v is not None]

def is_braced_ref(i, value):
    """Returns true if a reference is braced; otherwise False."""
    return is_ref(value[i]['t'], value[i]['c']) \
      and value[i-1]['t'] == 'Str' and value[i+1]['t'] == 'Str' \
      and value[i-1]['c'].endswith('{') and value[i+1]['c'].startswith('}')

def remove_braces(value):
    """Search for references and remove curly braces around them."""
    flag = False
    for i in range(len(value)-1)[1:]:
        if is_braced_ref(i, value):
            flag = True  # Found reference
            # Remove the braces
            value[i-1]['c'] = value[i-1]['c'][:-1]
            value[i+1]['c'] = value[i+1]['c'][1:]
    return flag

# pylint: disable=unused-argument
def preprocess(key, value, fmt, meta):
    """Preprocesses to correct for problems."""
    if key in ('Para', 'Plain'):
        while True:
            newvalue = repair_broken_refs(value)
            if newvalue:
                value = newvalue
            else:
                break
        if key == 'Para':
            return Para(value)
        else:
            return Plain(value)

# pylint: disable=unused-argument
def replace_attrtables(key, value, fmt, meta):
    """Replaces attributed tables while storing reference labels."""

    if is_attrtable(key, value):

        # Parse the table
        content, caption, label = parse_attrtable(value)

        # Bail out if the label does not conform
        if not label or not LABEL_PATTERN.match(label):
            return None

        # Save the reference
        references[label] = len(references) + 1

        # Adjust caption depending on the output format
        if fmt == 'latex':
            caption = list(caption) + [RawInline('tex', r'\label{%s}'%label)]
        else:
            caption = ast('Table %d. '%references[label]) + list(caption)

        # Return the replacement
        # pylint: disable=star-args
        args = [caption,]+content
        if fmt in ('html', 'html5'):
            anchor = RawInline('html', '<a name="%s"></a>'%label)
            return [Plain([anchor]), Table(*args)]
        else:
            return Table(*args)

# pylint: disable=unused-argument
def replace_refs(key, value, fmt, meta):
    """Replaces references to labelled tables."""

    # Remove braces around references
    if key in ('Para', 'Plain'):
        if remove_braces(value):
            if key == 'Para':
                return Para(value)
            else:
                return Plain(value)

    # Replace references
    if is_ref(key, value):
        prefix, label, suffix = parse_ref(value)
        # The replacement depends on the output format
        if fmt == 'latex':
            return prefix + [RawInline('tex', r'\ref{%s}'%label)] + suffix
        elif fmt in ('html', 'html5'):
            link = '<a href="#%s">%s</a>' % (label, references[label])
            return prefix + [RawInline('html', link)] + suffix
        else:
            return prefix + [Str('%d'%references[label])]+suffix

def main():
    """Filters the document AST."""

    # Get the output format, document and metadata
    fmt = sys.argv[1] if len(sys.argv) > 1 else ''
    doc = pandocfilters.json.loads(STDIN.read())
    meta = doc[0]['unMeta']

    # Replace attributed tables and references in the AST
    altered = functools.reduce(lambda x, action: walk(x, action, fmt, meta),
                               [preprocess, replace_attrtables, replace_refs],
                               doc)

    # Dump the results
    pandocfilters.json.dump(altered, STDOUT)

    # Flush stdout
    STDOUT.flush()

if __name__ == '__main__':
    main()
