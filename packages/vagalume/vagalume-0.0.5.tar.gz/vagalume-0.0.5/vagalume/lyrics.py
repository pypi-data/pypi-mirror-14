# -*- coding: utf-8 -*-

"""
Wrapper for lyrics search
"""
import requests
import re

API_URL = 'https://api.vagalume.com.br'
API_LYRIC_SEARCH_URL = API_URL + '/search.php'

STATUS_ARTIST_NOT_FOUND = 'notfound'
STATUS_SONG_NOT_FOUND = 'song_notfound'

LANGUAGES = {
    'pt-br': 1,
    'en': 2,
    'es': 3,
    'fr': 4,
    'de': 5,
    'it': 6,
    'nl': 7,
    'jp': 8,
    'pt': 9
}

def find(artist_name, song_title):
    params = {
        'art': artist_name,
        'mus': song_title
    }
    response = requests.get(API_LYRIC_SEARCH_URL, params=params)
    response.raise_for_status()
    return SearchResult(response.json())


class Artist(object):
    def __init__(self, artist):
        self.id = artist['id']
        self.name = artist['name']
        self.url = artist['url']


class Song(object):
    def __init__(self, song):
        self.id = song['id']
        self.name = song.get('name', None)
        self.language = song['lang']
        self.url = song['url']
        self.lyric = song['text']
        self.is_translation = False

        if not self.name:
            self.is_translation = True

            # For translations, the song title comes with the lyric body
            # followed by one or more empty lines. Here we get the title
            # and remove the first line and any following empty lines.

            self.name = self.get_title_from_lyric(self.lyric)
            self.lyric = self.remove_title(self.lyric)

    def get_title_from_lyric(self, lyric):
        lines = lyric.splitlines()
        title = re.sub(r'\[|\]|\n', '', lines[0]).strip()
        return title

    def remove_title(self, lyric):
        lines = lyric.splitlines()
        lines.pop(0)
        self.remove_initial_blank_lines(lines)
        return "\n".join(lines)

    def remove_initial_blank_lines(self, lines):
        if lines[0] and lines[0] not in ['\n', '\r\n']:
            return
        lines.pop(0)
        self.remove_initial_blank_lines(lines)


class SearchResult(object):
    def __init__(self, result):
        self.status = result['type']

        if self.is_not_found():
            return

        song = result['mus'][0]
        artist = result['art']
        translations = song.get('translate', [])

        self.artist = Artist(artist)
        self.song = Song(song)
        self.translations = [Song(translation) for translation in translations]

    def is_not_found(self):
        return self.status in (STATUS_ARTIST_NOT_FOUND, STATUS_SONG_NOT_FOUND)

    def get_translation_to(self, language):
        for translation in self.translations:
            if translation.language == LANGUAGES[language]:
                return translation

        return None
