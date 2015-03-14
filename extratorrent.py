# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.
import requests

def search(keywords):
    url='http://extratorrent.cc/search/?search=%s' %keywords
    response=requests.get(url)
    print page 
    lines = page.readlines()
    print lines
    page.close()
    results = []
    for linenum, line in enumerate(lines):
        if '<br /><table class="tl">' in line:
            for i in line.split('<td><a href="/torrent_download/')[1:]:
                item = {}
                item['name'] = \
                    i.split('title="Download ')[1] \
                    .split(' torrent">')[0]
                item['url'] = \
                    'http://extratorrent.cc/download/' \
                    + i.split('" title="')[0]
                filesize = \
                    i.split('</span></td><td>')[1] \
                    .split('</td>')[0] \
                    .replace('&nbsp;', ' ')
                if 'GB' in filesize.split():
                    item['size'] = float(filesize.split()[0]) * 1024 * 1024 * 1024
                elif 'MB' in filesize.split():
                    item['size'] = float(filesize.split()[0]) * 1024 * 1024
                elif 'KB' in filesize.split():
                    item['size'] = float(filesize.split()[0]) * 1024
                else:
                    item['size'] = int(filesize.split()[0])
                item['seed'] = \
                    int(i.split('<td class="s')[1][3:] \
                    .split('</td>')[0] \
                    .replace('---', '-1'))
                item['leech'] = \
                    int(i.split('<td class="l')[1][3:] \
                    .split('</td>')[0] \
                    .replace('---', '-1'))
                item['files'] = -1
                results.append(item)
    return results


print search("gladiator")