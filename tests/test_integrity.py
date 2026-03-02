from pathlib import Path
import yaml
import unittest

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.resolve()
DATA = ROOT.joinpath("_data")
EVENTS_PATH = DATA.joinpath("events.yml")
POSTS = ROOT.joinpath("_posts")


class TestIntegrity(unittest.TestCase):
    def test_events(self):
        events = yaml.safe_load(EVENTS_PATH.read_text())
        for event in events:
            self.assertIn("name", event)
            with self.subTest(name=event["name"]):
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

    def test_frontmatter(self) -> None:
        for path in sorted(POSTS.glob("*.md")):
            with self.subTest(post=path.name):
                data = _read_frontmatter(path)
                self.assertIn("tags", data)
                tags = data['tags']
                self.assertIsInstance(tags, list, msg=f"\n -> {path.name}")
                for tag in tags:
                    self.assertNotIn("-", tag, msg=f"\n -> {path.name}")


def _read_frontmatter(path: Path) -> dict:
    text = path.read_text()
    t = text.split("---")[1]
    return yaml.safe_load(t)
