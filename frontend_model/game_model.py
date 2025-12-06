from itertools import  permutations


class GameModel:
    def __init__(self):
        self.all_players = []
        self.current_player_index = 0
        self.possible_pins = [list(pin) for pin in permutations(range(10), 4)]
        self.game_is_active = False




def make_album(artist_name,album_title,no_of_songs = None):
    album_dict = {
        'artist': artist_name,
        'album': album_title

    }
    if no_of_songs is not None:
        album_dict['total_songs'] = no_of_songs

    return album_dict


while True:
    musician_name = input('enter an artist name: ').lower()
    musician_album = input('enter the album title: ').lower()
    
    album = make_album(musician_name, musician_album)
    print('-' * 20)
    print(album)
    if musician_name == 'q':
        break
    if musician_album == 'q':
        break

album_1 = make_album(musician_name, musician_album, 12)
print(album_1)











