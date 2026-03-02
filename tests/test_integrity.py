from collections import defaultdict
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
        xx = defaultdict(lambda: defaultdict(list))
        for path in sorted(POSTS.glob("*.md")):
            with self.subTest(post=path.name):
                data = _read_frontmatter(path)
                self.assertIn("tags", data)
                tags = data['tags']
                self.assertIsInstance(tags, list, msg=f"\n -> {path.name}")
                for tag in tags:
                    self.assertNotIn("-", tag, msg=f"\n -> {path.name}")
                    xx[tag.lower().rstrip("s")][tag].append(path)

        for k, v in xx.items():
            with self.subTest(name=k):
                all_path_names = "\n".join(sorted(f"- {i.name} ({kk})" for kk, ii in v.items() for i in ii))
                self.assertEqual(1, len(v), msg=f"unstandardized capitalization of {k} in\n\n{all_path_names}")


def _read_frontmatter(path: Path) -> dict:
    text = path.read_text()
    t = text.split("---")[1]
    return yaml.safe_load(t)
