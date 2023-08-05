#!/usr/bin/env python

import re
import sys
import os.path

# Initialize
res = {
    'comment': '//',
    'aside'  : '---$',
    'avatar' : '-.*\((.*)\):$',
    'scene'  : '#(\d+) (.*)$',
    'end'    : '\* END(.*)$',
    'choose' : '> (.*)\((\d+)\)$',
    'url'    : '\[(.*)\]:(.*)$',
}
for key in res:
    res[key] = re.compile(res[key])
empty_img = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='

# Analyze drama lines and get an array full of metadata
def analyze(lines):
    chapter, pos, scene, avatar, url, chaps, states = 0, 1, '', '', {}, {}, []
    n = len(lines)
    while (pos < n):
        l = lines[pos]
        end, dialog, choose = '', '', {}
        pos += 1
        if not l or res['comment'].match(l):
            continue
        if res['aside'].match(l):
            avatar = empty_img
        elif res['avatar'].match(l):
            avatar = res['avatar'].match(l).group(1) or empty_img
        elif res['scene'].match(l):
            m = res['scene'].match(l)
            chapter = m.group(1)
            scene = m.group(2) or empty_img
            avatar = empty_img
        elif res['end'].match(l):
            end = res['end'].match(l).group(1) or 'END'
        elif res['choose'].match(l):
            m = res['choose'].match(l)
            choose[m.group(1)] = m.group(2)
            while (pos < n):
                m = res['choose'].match(lines[pos])
                if m:
                    choose[m.group(1)] = m.group(2)
                    pos += 1
                else:
                    break
        elif res['url'].match(l):
            m = res['url'].match(l)
            url[m.group(1)] = m.group(2)
        else:
            dialog = l
        if end or dialog or choose:
            if not chapter in chaps:
                chaps[chapter] = len(states)
            state = {
                'avatar': avatar,
                'scene' : scene,
            }
            if end: state['end'] = end
            if dialog: state['dialog'] = dialog
            if choose: state['choose'] = choose
            states.append(state);
    for s in states:
        if s['scene']  in url: s['scene']  = url[s['scene']]
        if s['avatar'] in url: s['avatar'] = url[s['avatar']]
        if 'choose' in s:
            for key in s['choose']:
                s['choose'][key] = chaps[s['choose'][key]]
    pos = len(states) - 1
    while (pos > 0):
        for key in ('avatar', 'scene'):
            if states[pos][key] == states[pos - 1][key]:
                states[pos].pop(key, None)
        pos -= 1
    return states

def load(f):
    fh = open(f, 'r')
    return map(str.strip, fh.readlines())

def generate(output):
    print 'var strs=' + str(output) + ';'

if (len(sys.argv) < 2):
    print "Please specify a file name."
    exit(1)
elif (not os.path.isfile(sys.argv[1])):
    print sys.argv[1], "is not a file."
    exit(1)
else:
    generate(analyze(load(sys.argv[1])))
