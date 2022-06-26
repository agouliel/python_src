#!/usr/bin/env python

# https://gitlab.com/ewtoombs/footube

domain = 'https://www.youtube.com'

from sys import argv, stdout, stderr
import os
stdin_fd = 0
stdout_fd = 1
stderr_fd = 2
import io
from requests import Session
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urlparse, parse_qs

def get_id(arg):
    def cut_prefix(s):
        return arg[len(s):]
    def get_query_v(s):
        return parse_qs(urlparse(arg).query)['v'][0]
    for (s, f) in [
        ('ytdl://', cut_prefix),
        ('https://www.youtube.com/watch', get_query_v),
        ('https://youtu.be/', cut_prefix),
        ('https://yewtu.be/', cut_prefix),
    ]:
        if arg.startswith(s):
            return f(s)
    return arg

def page(f):
    """Send the output of f() to a pager, then exit. Allow python to exit when
    it's done, keeping the pager process running. f is passed a TextIOBase, to
    which f sends its output. Also, if we're not actually attached to a TTY,
    just call f(stdout)."""

    if not stdout.isatty():
        try:
            f(stdout)
        except BrokenPipeError:
            pass
        exit(0)

    pipe_read, pipe_write = os.pipe()

    if os.fork() == 0:
        # child
        # Change sessions and fork again, so that when the program is done, the
        # process can terminate completely without leaving a zombie and the
        # pager can keep running.
        os.setsid()
        if os.fork() != 0:
            # Parent; exit right away.
            exit(0)
        # child
        # Close unused pipe ends. If you don't do this, no SIGPIPE is sent up
        # the pipe when the pager exits, because technically the pipe is still
        # open!
        os.close(pipe_read)
        try:
            f(io.TextIOWrapper(io.BufferedWriter(io.FileIO(pipe_write, mode='w'))))
        except BrokenPipeError:
            pass
        exit(0)

    # parent
    os.wait()  # Kill the zombie.
    os.dup2(pipe_read, stdin_fd)
    # Again, close unused pipe ends. And their duplicates.
    os.close(pipe_read)
    os.close(pipe_write)
    os.execvp('less', ['less'])

def jprint(j):
    print(json.dumps(j, indent=4))
def json_values_with_key(j, k):
    # Given a tree of dicts and lists, which is what json.loads() returns,
    # search the dicts for a (k, v) pair whose key matches k and yield it.
    def visit(ld):
        if type(ld) == dict:
            if k in ld:
                yield ld[k]
            else:
                for i in ld.values():
                    yield from visit(i)
        elif type(ld) == list:
            for i in ld:
                yield from visit(i)
    return visit(j)

g_session = Session()
g_session.headers = {
    # This is just for fun.
    'User-Agent': 'Fuck you, Google, you coven of data succubi!',
}

def get_soup(*a, **k):
    response_str = g_session.get(*a, **k).content.decode()
    return BeautifulSoup(response_str, 'html.parser')

def initial_data(soup):
    # These days, the coven sends the data back in json format, which is great
    # except that json object is the rvalue of a javascript statement in a
    # certain <script> tag. So there is some heuristic munging to isolate this
    # json. The right way to do this would be to apply a real javascript
    # parser. As it is, this method is sensitive to changes in whitespace. So
    # if it breaks too often, I'll do that.
    start = 'var ytInitialData = '
    data = None

    for script_tag in soup.find_all('script'):
        script = script_tag.string
        if script is not None and script.startswith(start):
            data = json.loads(script[len(start):-1])
            break

    assert data is not None
    return data

def initial_player_response(soup):
    start = 'var ytInitialPlayerResponse = '
    data = None

    for script_tag in soup.find_all('script'):
        script = script_tag.string
        if script is not None and script.startswith(start):
            data = json.loads(script[len(start):-1])
            break

    assert data is not None
    return data

def api_key(soup):
    key = None
    for script_tag in soup.find_all('script'):
        script = script_tag.string
        if script is not None:
            match = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', script)
            if match is not None:
                key = match.group(1)
                break
    assert key is not None
    return key

def continuation(endpoint, key, token):
    post_data = {
        'context': {
            'client': {
                'clientName': 'WEB',
                'clientVersion': '2.20210303.01.00',
            },
        },
        'continuation': token,
    }
    return json.loads(g_session.post(
        domain + '/youtubei/v1/' + endpoint,
        params={'key': key},
        data=json.dumps(post_data),
    ).content)

def str_from_json(j):
    if 'simpleText' in j:
        return j['simpleText']
    return ' '.join([run['text'] for run in j['runs']])
def link_from_runs(runs):
    return runs['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']

def vr_print(vr, w):
    length = ''
    try:
        length = str_from_json(vr['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text'])
    except KeyError:
        pass
    date = str_from_json(vr['publishedTimeText']) \
        if 'publishedTimeText' in vr \
        else ''
    views = str_from_json(vr['shortViewCountText']) \
        if 'shortViewCountText' in vr \
        else ''
    user = link_from_runs(vr['ownerText'])[1:] \
        if 'ownerText' in vr \
        else ''

    w.write('{}\n{} {:7} {:15} {:15} {}\n\n'.format(
        str_from_json(vr['title']),
        'https://yewtu.be/' + vr['videoId'],
        length,
        date,
        views,
        user
    ))



if len(argv) == 1:
    stderr.write("""
usage: footube op arg ...
operations:
    s[earch] keyword ...
    Search youtube for the specified keywords

    c[hannel] chan_name
    Display all of the videos posted at chan_name, ordered by date descending.

    v[ideo] VIDEO
    Play the video VIDEO.

    video-meta|vm VIDEO
    Print a JSON object containing all of the metadata associated with the
    video VIDEO.

    video-comments|vc VIDEO
    Print all comments to the video VIDEO.

VIDEO:
    Videos may be specified by ID or by yewtu.be, youtube.com, youtu.be, or
    ytdl:// links.
"""[1:])
    exit(255)

op = argv[1]

if op == 'search' or op == 's':
    # Interpret the args as a search query in a somewhat sane way. If
    # someone runs footube s "foo bar" baz, they probably want those quote
    # marks in the search term as well.
    def quotify(s):
        if ' ' in s:
            return '"'+s+'"'
        else:
            return s
    q = ' '.join(map(quotify, argv[2:]))
    assert len(q) > 0  # You're so silly.

    soup = get_soup(
        domain + '/results',
        params={'search_query': q},
    )
    data = initial_data(soup)
    key = api_key(soup)

    def f(w):
        global data
        while True:
            for vr in json_values_with_key(data, 'videoRenderer'):
                vr_print(vr, w)

            c = list(json_values_with_key(data, 'continuationCommand'))
            if len(c) != 1:
                break

            c = c[0]['token']
            data = continuation('search', key, c)
    page(f)


elif op == 'channel' or op == 'c':
    soup = get_soup(
        domain + '/' + argv[2] + '/videos',
        params={'sort': 'dd'},
    )
    data = initial_data(soup)

    key = api_key(soup)
    def f(w):
        global data
        while True:
            for vr in json_values_with_key(data, 'gridVideoRenderer'):
                vr_print(vr, w)

            c = list(json_values_with_key(data, 'continuationCommand'))
            if len(c) != 1:
                break

            c = c[0]['token']
            data = continuation('browse', key, c)
    page(f)


elif op == 'video-meta' or op == 'vm':
    id = get_id(argv[2])
    soup = get_soup(
        domain + '/watch',
        params={'v': id},
    )
    meta = {
        'ytInitialData': initial_data(soup),
        'ytInitialPlayerResponse': initial_player_response,
    }

    def f(w):
        global meta
        w.write(json.dumps(meta, indent=4) + '\n')
    page(f)


elif op == 'video-comments' or op == 'vc':
    id = get_id(argv[2])
    soup = get_soup(
        domain + '/watch',
        params={'v': id},
    )
    key = api_key(soup)
    data = initial_data(soup)

    c = None
    for isr in json_values_with_key(data, 'itemSectionRenderer'):
        try:
            if isr['targetId'] != 'comments-section':
                continue
        except KeyError:
            continue
        for t in json_values_with_key(isr, 'token'):
            c = t
            break
        if c is not None:
            break
    assert c is not None

    def f(w):
        global key
        global c

        data = continuation('next', key, c)

        comments = []
        for a in data['onResponseReceivedEndpoints']:
            a = a['reloadContinuationItemsCommand']
            if a['slot'] == 'RELOAD_CONTINUATION_SLOT_BODY':
                comments = a['continuationItems']
        if len(comments) == 0:
            # Hm. No comments, I guess... This hasn't actually happened yet.
            return

        while True:
            for comment in json_values_with_key(comments, 'contentText'):
                w.write(str_from_json(comment) + '\n—————\n')

            c = list(json_values_with_key(comments[-1], 'token'))
            if len(c) != 1:
                break

            c = c[0]

            data = continuation('next', key, c)

            comments = json_values_with_key(data, 'continuationItems').__next__()
    page(f)


elif op == 'video' or op == 'v':
    id = get_id(argv[2])

    # We actually only want the API key lol.
    soup = get_soup(
        domain + '/watch',
        params={'v': id},
    )
    key = api_key(soup)

    # OK, now get the actual streaming data. This looks like continuation(),
    # but there are two exceptions in it.
    post_data = {
        'context': {
            'client': {
                # One here. Needed to avoid bandwidth throttling.
                'clientName': 'ANDROID',
                'clientVersion': '16.05',
            },
        },
        # The other here. It's really not a continuation lol
        'videoId': id,
    }
    fs = json.loads(g_session.post(
        domain + '/youtubei/v1/player',
        params={'key': key},
        data=json.dumps(post_data),
    ).content)['streamingData']['adaptiveFormats']

    vurl = None
    highest = 0
    for f in fs:
        if 'height' in f:
            if f['height'] == 720:
                vurl = f['url']
                break
            if f['height'] < 720 and f['height'] > highest:
                vurl = f['url']
    if vurl is None:
        stderr.write('Couldn\'t find an appropriate video URL.\n')

    aurl = None
    for f in fs:
        if f['itag'] == 251:  # high quality opus
            aurl = f['url']
            break
        if 'audioQuality' in f and f['audioQuality'] == 'AUDIO_QUALITY_MEDIUM':
            aurl = f['url']
    if aurl is None:
        stderr.write('Couldn\'t find an appropriate audio URL.\n')
        if vurl is None:
            exit(1)

    os.execvp('mpv', ['mpv', '--no-ytdl', '--fs', '--audio-file='+aurl, vurl])
