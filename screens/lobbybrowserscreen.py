from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivymd.uix.list import TwoLineListItem


class LobbyItem(TwoLineListItem):
    host_elo = ""
    host_nickname = ""

    def on_release(self):
        # Tell the server that we are joining the lobby
        app = App.get_running_app()
        app.client.is_host = False
        app.player.game_id = self.game_id
        local_id = app.root.ids.firebase_login_screen.localId
        message = {"command": "join_game", "firebase_id": local_id}
        app.client.send_message(message)
        # Set the opponents host elo so we can change elo when game is over
        #TODO
        # Should this be done after receiving the message back from the server?
        app.player.opponent_elo = self.host_elo
        app.player.opponent_nickname = self.host_nickname
        app.player.time_limit = self.time_limit
        app.root.ids.lobby_screen.ids.player_two_image.source = 'images/kingpieceblack.png'
        app.is_turn_owner = False
        app.player.is_red = False


class LobbyBrowserScreen(Screen):
    def get_lobbies_from_server(self):
        app = App.get_running_app()
        message = {"command": "get_lobbies"}
        app.client.send_message(message)

    def display_lobbies(self, lobbies_list):
        app = App.get_running_app()
        if app.root.ids.screen_manager.current != 'lobby_browser_screen':
            return

        self.ids.list_layout.clear_widgets()
        for lobby in lobbies_list:
            game_id = lobby['game_id']
            name = lobby['host_name']
            host_elo = str(lobby['host_elo'])
            time_limit = str(lobby['time_limit'])
            s = '' if time_limit == '1' else 's'
            lobby_item = LobbyItem(text=name + "'s match, rating " + host_elo,
                                         secondary_text="Time Limit: " + time_limit + " minute" + s + ' per player')
            lobby_item.host_nickname = name
            lobby_item.game_id = game_id
            lobby_item.host_elo = host_elo
            lobby_item.time_limit = time_limit
            self.ids.list_layout.add_widget(lobby_item)

