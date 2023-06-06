from pathlib import Path
import yaml
import unittest

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.resolve().joinpath("_data")
EVENTS_PATH = DATA.joinpath("events.yml")


class TestIntegrity(unittest.TestCase):
    def test_events(self):
        events = yaml.safe_load(EVENTS_PATH.read_text())
        for event in events:
            self.assertIn("name", event)
            with self.subTest(name=event['name']):
                talk = event.get("talk")
                if talk:
                    self.assertIsInstance(talk, dict)
                    self.assertIn("invited", talk)
                    self.assertIn("name", talk)
                    self.assertIn("url", talk)
                    if "date" not in event:
                        self.assertIn("date", talk)
                poster = event.get("poster")
                if poster:
                    self.assertIsInstance(poster, dict)
                    self.assertIn("name", poster)
                    self.assertIn("url", poster)

