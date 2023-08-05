# python-vagalume

A simple Python client for Vagalume API. Also a command-line utility to search
song lyrics and translations.

## Install

    $ pip install vagalume

## Usage 

You can use it from the **command line**:

    $ vagalume lyric 'radiohead' 'there, there'
    
With the -t flag, you can find translations (by default to pt-br):

    $ vagalume lyric 'radiohead' 'there, there' -t

But is possible to define another language supported by API ('fr', 'en', 'pt-br', 'pt', 'nl', 'de', 'jp', 'it' or 'es'):

    $ vagalume lyric 'radiohead' 'there, there' -t es

Also, you can use the **module** on your own code:

```python
from vagalume import lyrics

artist_name = 'radiohead'
song_name = 'there, there'

result = lyrics.find(artist_name, song_name)

if result.is_not_found():
    print 'Song not sound'
else:
    print result.song.name
    print result.artist.name
    print
    print result.song.lyric
    print
    
    translation = result.get_translation_to('pt-br')
    if not translation:
        print 'Translation not found'
    else:
        print translation.name
        print translation.lyric
```
