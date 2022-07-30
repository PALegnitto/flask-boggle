from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            # test that you're getting a template
            self.assertEqual(response.status_code, 200)
            self.assertIn('<table class="board">', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post("/api/new-game")
            json = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(json["board"] == "list"))
            self.assertTrue(type(json["gameId"] == "string"))
            #assertIsInstance
            self.assertTrue(games[json["gameId"]])

    def test_api_score_word(self):
        """Test scoring a word."""

        with self.client as client:
            response = client.post("/api/new-game")
            json = response.get_json()
            gameId = json["gameId"]
            current_game = games[gameId]

            current_game.board = [["B","E","E","E","S"],
                                  ["X","X","X","X","X"],
                                  ["X","X","X","X","X"],
                                  ["X","X","X","X","X"],
                                  ["X","X","X","X","X"]]
            
            score_response = client.post("/api/score-word",
                                        json={"gameId":gameId,"word":"BEE"})
            json_response = score_response.get_json()
            self.assertEqual({'result': 'ok'}, json_response)
            
            score_response = client.post("/api/score-word",
                                        json={"gameId":gameId,"word":"XXXX"})
            json_response = score_response.get_json()
            self.assertEqual({'result': 'not-word'}, json_response)
            
            score_response = client.post("/api/score-word",
                                        json={"gameId":gameId,"word":"SEA"})
            json_response = score_response.get_json()
            self.assertEqual({'result': 'not-on-board'}, json_response)
            