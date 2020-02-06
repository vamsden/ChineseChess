from kivy.utils import platform
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
import certifi
from json import dumps


class Player(EventDispatcher):
    nickname = ""
    is_red = BooleanProperty(False)  # Player is either red or black
    game_id = ""  # Could replace the game id in the client code
    elo = 0
    opponent_elo = 0

    def retrieve_elo_from_firebase(self):
        print("Trying to get saved elo ")
        app = App.get_running_app()
        local_id = app.root.ids.firebase_login_screen.localId
        UrlRequest(app.firebase_url + local_id + "/elo.json",
                   ca_file=certifi.where(),
                   on_success=self.got_elo_from_firebase,
                   on_failure=self.failed_to_get_elo_from_firebase,
                   on_error=self.failed_to_get_elo_from_firebase)

    def got_elo_from_firebase(self, thread, elo):
        print("Got elo from firebase: ", elo)
        self.elo = int(elo)

    def failed_to_get_elo_from_firebase(self, *args):
        print("failed_to_get_elo_from_firebase", args)
        pass

    def set_elo(self, elo):
        print("Setting elo to", elo)
        new_elo = '{"elo": %s}' %elo
        app = App.get_running_app()
        local_id = app.root.ids.firebase_login_screen.localId
        UrlRequest(App.get_running_app().firebase_url + local_id + ".json",
                   req_body=new_elo, method='PATCH', ca_file=certifi.where(),
                    on_success=self.updated_elo,
                    on_failure=self.failed_to_update_elo,
                    on_error=self.failed_to_update_elo)

    def updated_elo(self, thread, elo_data):
        print("Successfully updated elo")
        self.elo = elo_data['elo']

    def failed_to_update_elo(self, *args):
        print("failed_to_update_elo", *args)

    def set_nickname(self, nickname):
        """Overwrites the nickname saved firebase for this player

        :param nickname: The new nickname to save
        """
        print("Trying to update the nickname in firebase to", nickname)
        nickname_data = {"nickname": nickname}
        nickname_data = dumps(nickname_data)
        app = App.get_running_app()
        local_id = app.root.ids.firebase_login_screen.localId
        UrlRequest(app.firebase_url + local_id + ".json",
                   req_body=nickname_data, method='PATCH', ca_file=certifi.where(),
                   on_success=self.updated_nickname,
                   on_failure=self.failed_to_update_nickname,
                   on_error=self.failed_to_update_nickname)

    def updated_nickname(self, thread, nickname_data):
        app = App.get_running_app()
        app.root.current = 'home_screen'
        self.nickname = nickname_data['nickname']


    def failed_to_update_nickname(self, *args):
        print("failed_to_update_nickname", args)

    def get_saved_nickname(self):
        """Gets the saved nickname from firebase

        """
        print("Getting saved nickname now")
        app = App.get_running_app()
        local_id = app.root.ids.firebase_login_screen.localId
        UrlRequest(app.firebase_url + local_id + "/nickname.json",
                   ca_file=certifi.where(),
                   on_success=self.got_saved_nickname,
                   on_failure=self.failed_to_get_saved_nickname,
                   on_error=self.failed_to_get_saved_nickname)

    def got_saved_nickname(self, thread, nickname):
        print("Got the saved nickname: ", nickname)
        self.nickname = nickname

    def failed_to_get_saved_nickname(self, *args):
        print("failed_to_get_saved_nickname", args)

