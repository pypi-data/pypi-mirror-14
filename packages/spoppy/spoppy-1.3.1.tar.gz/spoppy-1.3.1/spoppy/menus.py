import logging
from collections import namedtuple

from spotify import TrackAvailability
from .search import search
from . import responses
from .util import (format_album, format_track, single_char_with_timeout,
                   sorted_menu_items, get_duration_from_s)

logger = logging.getLogger(__name__)

MenuValue = namedtuple('MenuValue', ('name', 'destination'))
MockPlaylist = namedtuple('Playlist', ('name', 'tracks'))


class Options(dict):
    def __init__(self, *args, **kwargs):
        super(Options, self).__init__(*args, **kwargs)
        self._cached_matches = {}
        self._stripped_keys_mapper = {
            key.replace(' ', ''): key
            for key in self
        }
        self.check_unique_keys()

    def __setitem__(self, key, value):
        super(Options, self).__setitem__(key, value)
        self._stripped_keys_mapper[key.replace(' ', '')] = key
        self.check_unique_keys()

    def check_unique_keys(self):
        if not len(self) == len(self._stripped_keys_mapper):
            raise TypeError('Two keys cannot be the same')

    def get_possibilities_from_cache(self, pattern):
        return self._cached_matches.get(pattern)

    def get_possibilities(self, pattern):
        cached_match = self.get_possibilities_from_cache(pattern)
        if cached_match:
            logger.debug('Pattern %s found in cache' % pattern)
        else:
            logger.debug('Trying to match %s' % pattern)
            possibilities_key = []
            possibilities_name = []
            pattern = pattern.lower()
            for key, (name, destination) in self.items():
                if key.lstrip(' ').startswith(pattern):
                    possibilities_key.append(key)
                elif self.fuzzy_match(pattern, name.lower()):
                    possibilities_name.append(key)

            logger.debug('possibilities_key: %s' % possibilities_key)
            logger.debug('possibilities_name: %s' % possibilities_name)
            cached_match = self._cached_matches[pattern] = (
                list(set(possibilities_key + possibilities_name))
            )
        return cached_match

    def fuzzy_match(self, pattern, name):
        try:
            for key in pattern:
                name = name[name.index(key) + 1:]
            return True
        except ValueError:
            return False

    def filter(self, pattern):
        possibilities = self.get_possibilities(pattern)

        return Options({
            key: value
            for key, value in
            self.items()
            if key in possibilities
        })

    def match_best_or_none(self, pattern):
        logger.debug('Trying to match (%s)' % pattern)
        possibilities = self.get_possibilities(pattern)
        logger.debug('Available possibilities: %s' % possibilities)
        if len(possibilities) == 1:
            logger.debug('Exactly one possibility, returning that!')
            return self[possibilities[0]]
        if pattern in self._stripped_keys_mapper:
            logger.debug('Pattern matches stripped key, returning key %s' % (
                self._stripped_keys_mapper[pattern]
            ))
            return self[self._stripped_keys_mapper[pattern]]


class Menu(object):
    INCLUDE_UP_ITEM = True

    BACKSPACE = b'\x7f'
    UP_ARROW = b'\x1b[A'
    DOWN_ARROW = b'\x1b[B'
    PAGE = 0

    def __init__(self, navigator):
        self.navigator = navigator

    def get_options(self):
        raise NotImplementedError('Subclass must define this method')

    def initialize(self):
        self._options = Options(self.get_options())
        self._options['q'] = MenuValue('quit', responses.QUIT)
        if self.INCLUDE_UP_ITEM:
            self._options['u'] = MenuValue('..', responses.UP)
        if self.navigator.player.has_been_loaded():
            self._options['p'] = MenuValue('player', responses.PLAYER)
        self.filter = ''

    def get_response(self):
        response = None
        while response is None:
            response = single_char_with_timeout(60)
            self.navigator.player.check_end_of_track()
        if response == Menu.BACKSPACE:
            self.filter = self.filter[:-1]
            return responses.NOOP
        elif response == Menu.UP_ARROW:
            logger.debug('Got UP_ARROW')
            self.PAGE = max([self.PAGE - 1, 0])
            return responses.NOOP
        elif response == Menu.DOWN_ARROW:
            logger.debug('Got DOWN_ARROW')
            self.PAGE += 1
            return responses.NOOP

        self.filter += response.decode('utf-8')
        if self.filter.endswith('\n'):
            # The user wants to go someplace...
            self.filter = self.filter.replace('\n', '')
            # Gets set as the item to navigate to if we only found one
            is_valid = self.is_valid_response()
            if is_valid:
                # Ok, return
                return is_valid.destination
        # Trigger redraw!
        return responses.NOOP

    def is_valid_response(self):
        return self._options.match_best_or_none(self.filter)

    def get_ui(self):
        if self.filter:
            items = sorted_menu_items(
                self._options.filter(self.filter).items()
            )
        else:
            items = sorted_menu_items(
                self._options.items()
            )
        if not items:
            menu_items = ('No matches for "%s"' % self.filter, )
        else:
            menu_items = tuple(
                self.get_menu_item(key, value.name) for key, value in
                items
            )
            if self.filter:
                is_valid = self.is_valid_response()
                if is_valid:
                    menu_items += (
                        '',
                        'Press [return] to go to (%s)' % is_valid.name
                    )
        if menu_items:
            number_of_menu_items = self.navigator.get_ui_height() - 4
            if len(menu_items) >= number_of_menu_items:
                paginated_menu_items = []
                while not paginated_menu_items:
                    start_idx = self.PAGE * number_of_menu_items
                    end_idx = (self.PAGE + 1) * number_of_menu_items
                    paginated_menu_items = menu_items[start_idx:end_idx]
                    if not paginated_menu_items:
                        self.PAGE -= 1
                menu_items = paginated_menu_items
            else:
                self.PAGE = 0

        above_menu_items = self.get_header()
        return (
            (above_menu_items, '') +
            menu_items +
            ('', 'Query: %s' % self.filter, )
        )

    def get_menu_item(self, key, value):
        return '[%s]: %s' % (key, value)

    def get_header(self):
        return ''


class MainMenu(Menu):
    INCLUDE_UP_ITEM = False

    def get_options(self):
        return {
            'vp': MenuValue(
                'View playlists', PlayListOverview(self.navigator)
            ),
            'st': MenuValue('Search for tracks', TrackSearch(self.navigator)),
            'sa': MenuValue('Search for albums', AlbumSearch(self.navigator)),
        }


class PlayListOverview(Menu):

    def get_options(self):
        def include_playlist(playlist):
            return (
                playlist.name and
                hasattr(playlist, 'link') and
                any([
                    track for track in playlist.tracks
                    if track.availability != TrackAvailability.UNAVAILABLE
                ])
            )
        results = {}
        playlists = self.navigator.session.playlist_container
        playlists = enumerate(
            sorted(
                (
                    playlist for playlist in playlists
                    if include_playlist(playlist)
                ),
                key=lambda x: x.name
            )
        )
        for i, playlist in playlists:
            menu_item = PlayListSelected(self.navigator)
            menu_item.playlist = playlist.link.as_playlist()
            results[str(i+1).rjust(4)] = MenuValue(
                menu_item.playlist.name, menu_item
            )
        return results

    def get_header(self):
        return 'Select a playlist'


class TrackSearchResults(Menu):
    search = None
    paginating = False
    _cached_search_results = []

    def set_initial_results(self, search):
        self.search = search
        self.update_cache()

    def update_cache(self):
        self._cached_search_results.append(self.search)

    def get_cache(self):
        return self._cached_search_results

    def get_response(self):
        if self.paginating:
            self.search.loaded_event.wait()
            self.paginating = False
            return self
        return super(TrackSearchResults, self).get_response()

    def go_to(self, up_down):
        if up_down > 0:
            destination = 'next_page'
        else:
            destination = 'previous_page'

        def inner():
            self.paginating = True

            new_cache_idx = self.get_cache().index(self.search) + up_down

            try:
                self.search = self.get_cache()[new_cache_idx]
                logger.debug('Got search from cache, yahoo!')
            except IndexError:
                direct_endpoint = getattr(
                    self.search.results, destination
                )
                logger.debug('Initiating new search')
                self.search = search(
                    self.navigator.session, self.search.query,
                    search_type=self.search.search_type,
                    direct_endpoint=direct_endpoint
                )
                self.update_cache()
            return self
        return inner

    def select_song(self, track_idx):
        def song_selected():
            track = self.search.results[track_idx]
            if self.navigator.player.is_playing():
                # If the user is currently playing we want him to have the
                # choice to add this song to the list of current songs or
                # start playing this playlist from this song
                menu = SongSelectedWhilePlaying(self.navigator)
                menu.track = track
                return menu
            else:
                self.navigator.player.clear()
                self.navigator.player.add_to_queue(track)
                self.navigator.player.play_track(0)
                return self.navigator.player
        return song_selected

    def get_header(self):
        return 'Search results for %s (total %d results)' % (
            self.search.results.term, self.search.results.total
        )

    def get_res_idx(self, i):
        return i + 1 + self.search.results.offset

    def get_ui(self):
        if self.paginating:
            return 'Loading...'
        return super(TrackSearchResults, self).get_ui()

    def get_options(self):
        if self.paginating:
            return {}
        results = self.get_options_from_search()
        if self.search.results.previous_page:
            results['p'] = MenuValue(
                'Previous', self.go_to(-1)
            )
        if self.search.results.next_page:
            results['n'] = MenuValue(
                'Next', self.go_to(1)
            )
        return results

    def get_options_from_search(self):
        results = {}
        for i, track in enumerate(
            track for track in
            self.search.results
            if track.availability != TrackAvailability.UNAVAILABLE
        ):
            results[str(self.get_res_idx(i)).rjust(4)] = MenuValue(
                format_track(track), self.select_song(i)
            )
        return results


class AlbumSearchResults(TrackSearchResults):
    search = None

    def select_album(self, track_idx):
        def album_selected():
            res = AlbumSelected(self.navigator)
            res.album = self.search.results[track_idx]
            return res
        return album_selected

    def get_options_from_search(self):
        results = {}
        for i, album in enumerate(
            album for album in
            self.search.results
        ):
            results[str(self.get_res_idx(i)).rjust(4)] = MenuValue(
                format_album(album), self.select_album(i)
            )
        return results


class TrackSearch(Menu):
    is_searching = False
    search_pattern = ''
    search = None
    search_type = 'tracks'
    result_cls = TrackSearchResults

    def get_options(self):
        return {}

    def get_search_results(self):
        self.search_pattern = self.filter
        self.search = search(
            self.navigator.session, self.search_pattern,
            search_type=self.search_type
        )
        self.is_searching = True
        return self

    def get_response(self):
        if self.is_searching:
            self.search.loaded_event.wait()
            self.is_searching = False

            search_results = self.result_cls(self.navigator)
            search_results.set_initial_results(self.search)

            self.is_searching = False
            self.search_pattern = ''
            self.search = None

            return search_results
        return super(TrackSearch, self).get_response()

    def is_valid_response(self):
        return super(TrackSearch, self).is_valid_response() or MenuValue(
            None, self.get_search_results
        )

    def get_ui(self):
        if self.is_searching:
            return 'Searching for %s' % self.search_pattern
        else:
            return '\n'.join((
                'Search query: %s' % self.filter,
                '',
                'Press [return] to search',
                '(Pro tip: you can also input "u" to go up or "q" to quit)'
            ))


class AlbumSearch(TrackSearch):
    search_type = 'albums'
    result_cls = AlbumSearchResults


class PlayListSelected(Menu):
    playlist = None
    deleting = False

    def shuffle_play(self):
        self.navigator.player.load_playlist(
            self.playlist,
            shuffle=True
        )
        self.navigator.player.play_current_song()
        return self.navigator.player

    def select_song(self, track_idx):
        def song_selected():
            if self.navigator.player.is_playing():
                # If the user is currently playing we want him to have the
                # choice to add this song to the list of current songs or
                # start playing this playlist from this song
                menu = SongSelectedWhilePlaying(self.navigator)
                menu.playlist = self.playlist
                menu.track = self.get_tracks()[track_idx]
                return menu
            else:
                self.navigator.player.load_playlist(
                    self.playlist
                )
                self.navigator.player.play_track(track_idx)
                return self.navigator.player
        return song_selected

    def add_to_queue(self):
        self.navigator.player.add_to_queue(self.playlist)
        return self.navigator.player

    def delete_playlist(self):
        self.deleting = True
        return self

    def do_delete_playlist(self):
        p_idx = self.navigator.session.playlist_container.index(
            self.playlist
        )
        self.navigator.session.playlist_container.remove_playlist(p_idx)
        return responses.UP

    def cancel_delete_playlist(self):
        self.deleting = False
        return self

    def get_tracks(self):
        return self.playlist.tracks

    def get_name(self):
        return self.playlist.name

    def get_options(self):
        results = {}
        if self.deleting:
            results['y'] = MenuValue('Yes', self.do_delete_playlist)
            results['n'] = MenuValue('No', self.cancel_delete_playlist)
        else:
            for i, track in enumerate(
                track for track in
                self.get_tracks()
                if track.availability != TrackAvailability.UNAVAILABLE
            ):
                results[str(i+1).rjust(4)] = MenuValue(
                    format_track(track), self.select_song(i)
                )
            if results:
                results['sp'] = MenuValue('Shuffle play', self.shuffle_play)
                if self.navigator.player.is_playing():
                    results['add_to_queue'] = MenuValue(
                        'Add %s to queue' % self.get_name(),
                        self.add_to_queue
                    )
            else:
                logger.debug('There are no songs in this playlist!')
            results['x'] = MenuValue('Delete playlist', self.delete_playlist)

        return results

    def get_header(self):
        if self.deleting:
            return 'Are you sure you want to delete playlist [%s]' % (
                self.get_name()
            )
        return 'Playlist [%s] selected' % self.get_name()


class AlbumSelected(PlayListSelected):
    album = None
    _tracks = None

    def initialize(self):
        super(AlbumSelected, self).initialize()
        self.playlist = MockPlaylist(self.get_name(), self.get_tracks())

    def get_tracks(self):
        if not self._tracks:
            self._tracks = self.album.tracks
        return self._tracks

    def get_name(self):
        return format_album(self.album)

    def get_header(self):
        return 'Album [%s] selected' % self.get_name()


class SongSelectedWhilePlaying(Menu):
    playlist = None
    track = None

    def add_to_queue(self):
        self.navigator.player.add_to_queue(self.track)
        return responses.UP

    def replace_current(self):
        self.navigator.player.load_playlist(
            self.playlist
        )
        self.navigator.player.play_track(
            self.playlist.tracks.index(self.track)
        )
        return self.navigator.player

    # Only thing we know here is that the player is currently playing something
    def get_options(self):
        results = {}
        if self.playlist:
            results['replace'] = MenuValue(
                'Replace currently playing with %s' % (self.playlist.name),
                self.replace_current
            )
        results['add_to_queue'] = MenuValue(
            'Add %s to queue' % format_track(self.track),
            self.add_to_queue
        )
        return results

    def get_header(self):
        info = [
            'Song: %s' % format_track(self.track),
            'Duration: %s' % get_duration_from_s(self.track.duration / 1000.0)
        ]
        if self.playlist:
            info.append('Playlist: %s' % self.playlist.name)
        if self.track.album:
            info.append('Album: %s' % self.track.album.name)
            info.append('Released: %s' % self.track.album.year)
        return '\n'.join(info)


class SavePlaylist(Menu):
    song_list = []
    is_saving = False
    callback = None
    original_playlist_name = None

    def get_options(self):
        return {}

    def save_playlist(self):
        self.new_playlist_name = (
            self.filter.strip() or self.original_playlist_name
        )
        self.is_saving = True
        return self

    def get_response(self):
        if self.is_saving:
            edited = False
            if self.new_playlist_name == self.original_playlist_name:
                try:
                    playlist = [
                        playlist for playlist in
                        self.navigator.session.playlist_container
                        if playlist.name == self.new_playlist_name
                    ][0]
                    playlist.load()
                except IndexError:
                    pass
                else:
                    # We found our playlist, now we have to edit it
                    # We kind of want to maintain when the songs were added,
                    # so we have to shuffle songs that were already in the
                    # playlist around
                    # These cases can come up:
                    #   1. Song is in the same place in song list and playlist
                    #   2. Song appears in playlist later than in song list
                    #   3. Song does not appear at all in playlist
                    for song_list_idx, song in enumerate(self.song_list):
                        try:
                            playlist_tracks_idx = playlist.tracks.index(song)
                        except ValueError:
                            # Case 3
                            playlist.add_tracks(song, song_list_idx)
                        else:
                            if playlist_tracks_idx == song_list_idx:
                                # Case 1
                                continue
                            elif playlist_tracks_idx >= song_list_idx:
                                # Case 2
                                playlist.reorder_tracks(
                                    playlist_tracks_idx, song_list_idx
                                )
                    # Now we have to remove all the tracks that are at indexes
                    # larger then the length of the song list
                    playlist.remove_tracks(
                        range(len(self.song_list), len(playlist.tracks))
                    )
                    edited = True
            if not edited:
                playlist = (
                    self.navigator.session.playlist_container.add_new_playlist(
                        self.new_playlist_name
                    )
                )
                playlist.add_tracks(self.song_list)

            playlist.load()
            self.is_saving = False
            while playlist.has_pending_changes:
                self.navigator.session.process_events()
            if self.callback:
                self.callback(playlist)
            return responses.UP
        return super(SavePlaylist, self).get_response()

    def is_valid_response(self):
        return super(SavePlaylist, self).is_valid_response() or (
            (
                self.filter.strip() or self.original_playlist_name
            ) and
            MenuValue(
                None, self.save_playlist
            )
        )

    def get_ui(self):
        if self.is_saving:
            return 'Saving playlist as %s' % self.new_playlist_name
        else:
            return '\n'.join((
                '%d songs to be added to new playlist' % len(self.song_list),
                'The original playlist name was [%s]. Leave the name empty '
                'to replace [%s] with the current song list' % (
                    self.original_playlist_name, self.original_playlist_name
                ) if self.original_playlist_name else '',
                'Playlist name: %s' % self.filter,
                '',
                'Press [return] to save your playlist',
                '(Pro tip: you can also input "u" to go up or "q" to quit)'
            ))
