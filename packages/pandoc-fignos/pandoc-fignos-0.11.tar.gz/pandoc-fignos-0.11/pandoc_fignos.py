#! /usr/bin/env python

"""pandoc-fignos: a pandoc filter that inserts figure nos. and refs."""

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
# The basic idea is to scan the AST two times in order to:
#
#   1. Insert text for the figure number in each figure caption.
#      For LaTeX, insert \label{...} instead.  The figure ids
#      and associated figure numbers are stored in the global
#      references tracker.
#
#   2. Replace each reference with a figure number.  For LaTeX,
#      replace with \ref{...} instead.
#
# There is also an initial scan to do some preprocessing.

# pylint: disable=invalid-name

import re
import functools
import itertools
import io
import sys
import os, os.path
import subprocess
import psutil
import argparse

# pylint: disable=import-error
import pandocfilters
from pandocfilters import stringify, walk
from pandocfilters import RawBlock, RawInline
from pandocfilters import Str, Space, Para, Plain, Cite, elt
from pandocattributes import PandocAttributes

# Read the command-line arguments
parser = argparse.ArgumentParser(description='Pandoc figure numbers filter.')
parser.add_argument('fmt')
parser.add_argument('--pandocversion', help='The pandoc version.')
args = parser.parse_args()

# Get the pandoc version.  Check the command-line args first, then inspect the
# parent process.  As a last resort, make a bare call to pandoc.
PANDOCVERSION = None
if args.pandocversion:
    PANDOCVERSION = args.pandocversion
else:
    try:  # Get the information from the parent process, if we can
        if os.name == 'nt':
            # psutil appears to work differently for windows.  Two parent calls?
            # Weird.
            command = psutil.Process(os.getpid()).parent().parent().exe()
        else:
            command = psutil.Process(os.getpid()).parent().exe()
    except:  # pylint: disable=bare-except
        # Call whatever pandoc is available and hope for the best
        command = 'pandoc'
    if 'fignos' in command:  # Infinite process creation!
        command = 'pandoc'  # Hope for the best here too
    if os.path.basename(command).startswith('pandoc'):
        output = subprocess.check_output([command, '-v'])
        line = output.decode('utf-8').split('\n')[0]
        PANDOCVERSION = line.split(' ')[-1]
if PANDOCVERSION is None:
    raise RuntimeError('Cannot determine pandoc version.  '\
                       'Please file an issue at '\
                       'https://github.com/tomduck/pandoc-fignos/issues')

# Create our own pandoc image primitives
Image = elt('Image', 2)      # Pandoc < 1.16
AttrImage = elt('Image', 3)  # Pandoc >= 1.16

# Detect python 3
PY3 = sys.version_info > (3,)

# Pandoc uses UTF-8 for both input and output; so must we
if PY3:  # Force utf-8 decoding (decoding of input streams is automatic in py3)
    STDIN = io.TextIOWrapper(sys.stdin.buffer, 'utf-8', 'strict')
    STDOUT = io.TextIOWrapper(sys.stdout.buffer, 'utf-8', 'strict')
else:    # No decoding; utf-8-encoded strings in means the same out
    STDIN = sys.stdin
    STDOUT = sys.stdout

# Patterns for matching labels and references
LABEL_PATTERN = re.compile(r'(fig:[\w/-]*)')
REF_PATTERN = re.compile(r'@(fig:[\w/-]+)')

references = {}  # Global references tracker

# Meta variables
figurename = 'Figure'  # May be reset by main()

def is_attrimage(key, value):
    """True if this is an attributed image; False otherwise."""
    return key == 'Image' and len(value) == 3

def parse_attrimage(value):
    """Parses an attributed image."""
    o, caption, target = value
    attrs = PandocAttributes(o, 'pandoc')
    if attrs.id == 'fig:': # Make up a unique description
        attrs.id = 'fig:' + '__'+str(hash(target[0]))+'__'
    return attrs, caption, target

def is_figure(key, value):
    """True if this is a figure; False otherwise."""
    if key == 'Para' and len(value) == 1:
        return is_figure(value[0]['t'], value[0]['c'])
    elif key == 'Image' and is_attrimage(key, value):
        # pylint: disable=unused-variable
        attrs, caption, target = parse_attrimage(value)
        return target[1] == 'fig:'  # Pandoc uses this as a figure marker
    else:
        return False

def is_figref(key, value):
    """True if this is a figure reference; False otherwise."""
    return key == 'Cite' and REF_PATTERN.match(value[1][0]['c']) and \
      parse_figref(value)[1] in references

def parse_figref(value):
    """Parses a figure reference."""
    prefix = value[0][0]['citationPrefix']
    label = REF_PATTERN.match(value[1][0]['c']).group(1)
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
    if PANDOCVERSION < '1.16':
        return key1 == 'Link' and value1[0][0]['t'] == 'Str' and \
          value1[0][0]['c'].endswith('{@fig') \
            and key2 == 'Str' and '}' in value2
    else:
        return key1 == 'Link' and value1[1][0]['t'] == 'Str' and \
          value1[1][0]['c'].endswith('{@fig') \
          and key2 == 'Str' and '}' in value2

def repair_broken_refs(value):
    """Repairs references broken by pandoc's --autolink_bare_uris."""

    # autolink_bare_uris splits {@fig:id} at the ':' and treats
    # the first half as if it is a mailto url and the second half as a string.
    # Let's replace this mess with Cite and Str elements that we normally get.
    flag = False
    for i in range(len(value)-1):
        if value[i] == None:
            continue
        if is_broken_ref(value[i]['t'], value[i]['c'],
                         value[i+1]['t'], value[i+1]['c']):
            flag = True  # Found broken reference
            if PANDOCVERSION < '1.16':
                s1 = value[i]['c'][0][0]['c']  # Get the first half of the ref
            else:
                s1 = value[i]['c'][1][0]['c']  # Get the first half of the ref
            s2 = value[i+1]['c']           # Get the second half of the ref
            ref = '@fig' + s2[:s2.index('}')]  # Form the reference
            prefix = s1[:s1.index('{@fig')]    # Get the prefix
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
        return [v for v in value if not v is None]

def is_braced_figref(i, value):
    """Returns true if a reference is braced; otherwise False.
    i is the index in the value list.
    """
    # The braces will be found in the surrounding values
    return is_figref(value[i]['t'], value[i]['c']) \
      and value[i-1]['t'] == 'Str' and value[i+1]['t'] == 'Str' \
      and value[i-1]['c'].endswith('{') and value[i+1]['c'].startswith('}')

def remove_braces_from_figrefs(value):
    """Search for figure references and remove curly braces around them."""
    flag = False
    for i in range(len(value)-1)[1:]:
        if is_braced_figref(i, value):
            flag = True  # Found reference
            value[i-1]['c'] = value[i-1]['c'][:-1]  # Remove the braces
            value[i+1]['c'] = value[i+1]['c'][1:]
    return flag

# pylint: disable=unused-argument
def preprocess(key, value, fmt, meta):
    """Preprocesses to correct for problems."""
    if key in ('Para', 'Plain'):
        while True:  # Repeat processing until it succeeds
            newvalue = repair_broken_refs(value)
            if newvalue:
                value = newvalue
            else:
                break
        if key == 'Para':
            return Para(value)
        else:
            return Plain(value)

def deQuoted(value):
    """Replaces Quoted elements that stringify() can't handle."""
    # pandocfilters.stringify() needs to be updated...

    # The weird thing about this is that chained filters do not see this
    # element.  Pandoc gives different json depending on whether or it is
    # calling the filter directly.  This should not be happening.
    newvalue = []
    for v in value:
        if v['t'] != 'Quoted':
            newvalue.append(v)
        else:
            quote = '"' if v['c'][0]['t'] == 'DoubleQuote' else "'"
            newvalue.append(Str(quote))
            newvalue += v['c'][1]
            newvalue.append(Str(quote))
    return newvalue

def get_attrs(value, n):
    """Extracts attributes from a list of values.
    Extracted elements are set to None in the list.
    n is the index of the image.
    """
    # Note: Pandoc does not allow for there to be a space between the image
    # and its attributes.

    # Fix me: This currently does not allow curly braces inside quoted
    # attributes.  The close bracket is interpreted as the end of the attrs.
    assert value[n]['t'] == 'Image'
    n += 1  # n is now the index where attributes should start
    if value[n:] and value[n]['t'] == 'Str' and value[n]['c'].startswith('{'):
        for i, v in enumerate(value[n:]):
            if v['t'] == 'Str' and v['c'].strip().endswith('}'):
                s = stringify(deQuoted(value[n:n+i+1]))  # Extract the attrs
                value[n:n+i] = [None]*i          # Remove extracted elements
                endspaces = s[len(s.rstrip()):]  # Check for spaces after attrs
                value[n+i] = Str(endspaces) if len(endspaces) else None
                return PandocAttributes(s.strip(), 'markdown')

# pylint: disable=unused-argument, too-many-branches
def replace_attrimages(key, value, fmt, meta):
    """Replaces attributed images while storing reference labels."""

    if key == 'Para':

        flag = False  # Flag that the value is modified

        # Internally use AttrImage for all attributed images, regardless of
        # the pandoc version.  Unattributed images will be left as such.
        if PANDOCVERSION < '1.16':  # Attributed images were introduced in 1.16
            for i, v in enumerate(value):
                if v and v['t'] == 'Image':
                    attrs = get_attrs(value, i)
                    if attrs:
                        value[i] = AttrImage(attrs.to_pandoc(), *v['c'])
                        flag = True

            # If the only element of this paragraph is an image, then mark the
            # image as a figure.
            value = [v for v in value if not v is  None]
            if flag and len(value) == 1:
                attrs, caption, target = parse_attrimage(value[0]['c'])
                target[1] = 'fig:'  # Pandoc uses this as a figure marker

        # Return the content.  Add html anchors for figures.
        if fmt in ('html', 'html5') and is_figure(key, value):
            attrs, caption, target = parse_attrimage(value[0]['c'])
            anchor = RawInline('html', '<a name="%s"></a>'%attrs.id)
            return [Plain([anchor]), Para(value)]
        elif flag:
            return Para(value)

    elif is_attrimage(key, value):

        # Parse the image
        attrs, caption, target = parse_attrimage(value)

        # Bail out if the label does not conform
        if not attrs.id or not LABEL_PATTERN.match(attrs.id):
            if PANDOCVERSION < '1.16':
                return Image(caption, target)
            else:
                return None

        # Save the reference
        references[attrs.id] = len(references) + 1

        # Adjust caption depending on the output format
        if fmt == 'latex':
            caption = list(caption) + [RawInline('tex', r'\label{%s}'%attrs.id)]
        else:
            caption = ast('%s %d. '%(figurename, references[attrs.id])) + \
              list(caption)

        # Return the replacement
        if PANDOCVERSION < '1.16':
            return Image(caption, target)
        else:
            if PANDOCVERSION >= '1.17' and fmt == 'latex':
                # Remove id from the image attributes.  It is incorrectly
                # handled by pandoc's TeX writer for these versions
                if attrs.id.startswith('fig:'):
                    attrs.id = ''
            return AttrImage(attrs.to_pandoc(), caption, target)

# pylint: disable=unused-argument
def replace_refs(key, value, fmt, meta):
    """Replaces references to labelled images."""

    # Remove braces around references
    if key in ('Para', 'Plain'):
        if remove_braces_from_figrefs(value):
            if key == 'Para':
                return Para(value)
            else:
                return Plain(value)

    # Replace references
    if is_figref(key, value):
        prefix, label, suffix = parse_figref(value)
        # The replacement depends on the output format
        if fmt == 'latex':
            return prefix + [RawInline('tex', r'\ref{%s}'%label)] + suffix
        elif fmt in ('html', 'html5'):
            link = '<a href="#%s">%s</a>' % (label, references[label])
            return prefix + [RawInline('html', link)] + suffix
        else:
            return prefix + [Str('%d'%references[label])] + suffix

def main():
    """Filters the document AST."""

    global figurename  # pylint: disable=global-statement

    # Get the output format, document and metadata
    fmt = args.fmt
    doc = pandocfilters.json.loads(STDIN.read())
    meta = doc[0]['unMeta']

    # Extract meta variables
    if 'figure-name' in meta:
        figurename = meta['figure-name']['c']  # Works for cmdline vars
        if type(figurename) is list:  # For YAML vars
            # Note: At this point I am expecting a single-word replacement.
            # This will need to be revisited if multiple words are needed.
            figurename = figurename[0]['c']

    # For latex/pdf, inject command to change figurename
    if fmt == 'latex' and figurename != 'Figure':
        tex = r'\renewcommand{\figurename}{%s}'%figurename
        doc[1] = [RawBlock('tex', tex)] + doc[1]

    # Replace attributed images and references in the AST
    altered = functools.reduce(lambda x, action: walk(x, action, fmt, meta),
                               [preprocess, replace_attrimages, replace_refs],
                               doc)

    # Dump the results
    pandocfilters.json.dump(altered, STDOUT)

    # Flush stdout
    STDOUT.flush()

if __name__ == '__main__':
    main()
