import os
import tempfile

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

import langid

from ipodshuffle import Shuffle, MASTER, NORMAL, PODCAST, AUDIOBOOK

from ipodshuffle.audio import get_type as get_audio_type

from ipodshuffle.storage.local import LocalVoiceDB, LocalFileLog

import ipodshuffle.utils

from . import str2list

from .tts import ENGINE_MAP

from .tts.error import GetVoiceDataError

from .fix_zh import fix_zh


CACHE_DIR = os.path.join(os.path.expanduser('~'), '.cache/teresa')
os.makedirs(CACHE_DIR, exist_ok=True)


def filename(path):
    return os.path.splitext(os.path.split(path)[1])[0]


def beautify_text(text):
    new_text = None
    if '-' in text:
        new_text = text.replace('-', ',')

    return new_text


def id3_title_artist(path):
    title = None
    artist = None

    try:
        audio = EasyID3(path)
    except ID3NoHeaderError:
        pass
    else:

        for k, v in audio.items():
            if k == 'title':
                title = v[0]
            elif k == 'artist':
                artist = v[0]

    return title, artist


def title_artist_or_filename(path):

    title, artist = id3_title_artist(path)
    title.strip()
    artist.strip()

    if title:
        text = title
        if artist:
            if text[-1] in ('?', ',', '.'):
                pass
            else:
                text += ','

            text += ' ' + artist
    else:
        text = beautify_text(filename(path))

    return text


###########################################################################


def get_all_dires(dire):
    dirs = []
    # os.path.walk(src, visit, dir_files_list)
    for top, sub_dirs, names in os.walk(dire, followlinks=True):
        dirs.append(top)
    return dirs


get_all_files = ipodshuffle.utils.get_all_files


def get_sub_files_dires(dire):
    files = []
    dires = []
    for one in sorted(os.listdir(dire)):
        path = os.path.join(dire, one)

        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            dires.append(path)

    return files, dires


def get_legal_files(files):
    legal_files = []
    for file in files:
        if get_audio_type(file):
            legal_files.append(file)
        else:
            print('Ignore not legal file: ', file)

    return legal_files

###############################################################################


def get_master_normals(dire):
    titles_files = []

    dires = get_all_dires(dire)

    for _dire in dires:
        legal_files = get_legal_files(get_all_files(_dire))
        if legal_files:
            title = os.path.split(_dire)[1]
            titles_files.append((title, sorted(legal_files)))

    return titles_files


def get_podcasts(dire):
    titles_files = []

    dires = get_sub_files_dires(dire)[1]

    for _dire in dires:
        legal_files = get_legal_files(get_sub_files_dires(_dire)[0])
        if legal_files:
            title = os.path.split(_dire)[1]
            titles_files.append((title, legal_files))

    return titles_files


def get_audiobooks(dire):
    titles_files = []
    files, dires = get_sub_files_dires(dire)

    # Do single file audiobooks
    for file in get_legal_files(files):
        title = filename(file)
        titles_files.append((title, (file,)))

    for _dire in dires:
        legal_files = get_legal_files(get_sub_files_dires(_dire)[0])
        if legal_files:
            title = os.path.split(_dire)[1]
            titles_files.append((title, legal_files))

    return titles_files


def voice_things(local_voicedb, args):

    langs = args.langs or []

    tts_func = None
    if args.engine:
        tts_engine = ENGINE_MAP[args.engine]
        tts_func = tts_engine.get_tts_func(args)

        if not langs:
            langs = tts_engine.legal_langs

    lang_map = {}
    for _lang in langs:
        lang_map[_lang[:2]] = _lang

    languages_to_set = [lang_id_code for lang_id_code in lang_map.keys()]

    langid.set_languages(languages_to_set)

    def classify_tts_lang(text):
        langid_code = langid.classify(text)[0]

        if 'zh' in languages_to_set:
            langid_code = fix_zh(langid_code, text)

        tts_lang = lang_map[langid_code]

        return tts_lang

    def local_voice_path(text, lang):
        tts_lang = lang
        print(repr(lang), repr(text))
        voice_path = local_voicedb.get_path(text, tts_lang)
        if not voice_path and callable(tts_func):  # The voice not in local
            print('   not in local. ', end='')

            print('try TTS engine {} ... '.format(args.engine), end='', flush=True)
            voice_data = tts_func(text, tts_lang)
            print('done!')

            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            tmp_file_name = tmp_file.name
            tmp_file.close()

            with open(tmp_file_name, 'wb') as f:
                f.write(voice_data)

            local_voicedb.add_voice(tmp_file_name, text, tts_lang)

            os.remove(tmp_file_name)

            voice_path = local_voicedb.get_path(text, tts_lang)

        return voice_path

    return classify_tts_lang, local_voice_path


def sync(args):

    src = os.path.realpath(args.src)
    base = os.path.realpath(args.base)

    ipod = Shuffle(base)
    if ipod.enable_voiceover:
        local_voicedb = LocalVoiceDB(os.path.join(CACHE_DIR, 'voices_log.json'), os.path.join(CACHE_DIR, 'voices'))
        local_voicedb.clean()
        classify_tts_lang_func, local_voice_path_func = voice_things(local_voicedb, args)

        ipod.voice_path_func = local_voice_path_func

    ipod.audiodb.clean()

    ipod.tracks_voiceoverdb.clean()
    ipod.playlists_voiceoverdb.clean()

    ipod.playlists.clear()

    local_filelog = LocalFileLog(os.path.join(CACHE_DIR, 'local_file_log.json'))

    dire_and_funs = (
        (src + '/' + 'music', get_master_normals),
        (src + '/' + 'podcasts', get_podcasts),
        (src + '/' + 'audiobooks', get_audiobooks),
    )

    def x(y):
        z = []
        for dire, _fun in y:
            a = []
            if os.path.exists(dire) and os.path.isdir(dire):
                a = _fun(dire)
            z.append(a)
        return z

    master_and_normals, podcasts, audiobooks = x(dire_and_funs)

    master = []
    normals = []
    if master_and_normals:
        master = master_and_normals[0]
        normals = master_and_normals[1:]

    def set_voice(obj, text, lang):
        try:
            obj.voice = text, lang
        except GetVoiceDataError as e:
            print(e, ' ignored.')

    def add_files_to_playlist(pl, files, get_track_voice_title=None):
        for file in files:
            checksum = local_filelog.get_checksum(file)
            if not checksum:
                local_filelog.log_it(file)
                checksum = local_filelog.get_checksum(file)

            path_in_ipod = ipod.audiodb.get_filename(checksum)
            if not path_in_ipod:
                ipod.audiodb.add(file)
                path_in_ipod = ipod.audiodb.get_filename(checksum)

            track = ipod.create_track(path_in_ipod)
            pl.tracks.append(track)

            if ipod.enable_voiceover:
                text = get_track_voice_title(file)
                lang = classify_tts_lang_func(text)

                set_voice(track, text, lang)

    def add_playlists(title_and_files, pl_type, text_fun):
        for title, files in title_and_files:

            pl = ipod.create_playlist(pl_type)
            ipod.playlists.append(pl)

            if ipod.enable_voiceover:

                lang = classify_tts_lang_func(title)
                set_voice(pl, title, lang)

            add_files_to_playlist(pl, files, text_fun)

    master_pl = ipod.playlists.append_one(pl_type=MASTER)
    add_files_to_playlist(master_pl, master[1], title_artist_or_filename)

    add_playlists(normals, NORMAL, title_artist_or_filename)
    add_playlists(podcasts, PODCAST, title_artist_or_filename)
    add_playlists(audiobooks, AUDIOBOOK, filename)

    ipod.write_db()


def register(parser):
    import argparse
    parser_sync = parser.add_parser('sync', help='sync to ipod',
                                    formatter_class=argparse.RawTextHelpFormatter,
                                    epilog='Legal lang codes of engines:\n' +
                                           '\n'.join(['  {}: {}'.format(k, ','.join(sorted(v.legal_langs)))
                                                      for k, v in ENGINE_MAP.items()]) + '\n'
                                           '\n'
                                           'Two examples of use:\n'
                                           '  %(prog)s -b /media/ipod_base -s /media/ipod_src -l en-gb '
                                           '-e svox\n'
                                           '  %(prog)s -b /media/ipod_base -s /media/ipod_src -l en-gb,zh-cn,ja-jp '
                                           '-e voicerss -k d279f919f7384d3bafa516caad0eae56'
                                    )

    parser_sync.add_argument('-b', dest='base', help='ipod base path', metavar='<path>', required=True)
    parser_sync.add_argument('-s', dest='src', help='source path', metavar='<path>', required=True)
    parser_sync.add_argument('-l', dest='langs',
                             help='comma-separated set of target language codes (e.g en-gb,zh-cn)',
                             type=str2list, metavar='<lang1>,<lang2>...')
    parser_sync.add_argument('-e', dest='engine', choices=ENGINE_MAP.keys(), metavar='<engine>',
                             help='TTS engine, one of ' + ', '.join(ENGINE_MAP.keys()))

    for module in ENGINE_MAP.values():
        module.add_arg(parser_sync)

    parser_sync.set_defaults(func=sync)
