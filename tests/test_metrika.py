import unittest
from pathlib import Path


DIST = Path(__file__).resolve().parents[1] / "dist"


class MetrikaTest(unittest.TestCase):
    def test_counter_is_loaded_on_site_pages_and_thank_you(self):
        app = (DIST / "assets/app.js").read_text()
        thanks = (DIST / "spasibo.html").read_text()
        for content in (app, thanks):
            self.assertIn("mc.yandex.ru/metrika/tag.js", content)
            self.assertIn("32011556", content)


if __name__ == "__main__":
    unittest.main()
