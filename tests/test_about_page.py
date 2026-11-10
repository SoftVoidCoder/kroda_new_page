"""Validate the published About page and its five requested destinations."""
from pathlib import Path
import unittest

from lxml import html


ROOT = Path(__file__).resolve().parents[1] / "dist"


class AboutPageTest(unittest.TestCase):
    def setUp(self):
        self.tree = html.fromstring((ROOT / "about.html").read_text())

    def test_direction_links(self):
        links = self.tree.xpath("//nav[contains(@class, 'direction-links')]/a")
        self.assertEqual(
            [link.get("href") for link in links],
            [
                "industrial-solutions.html",
                "household-solutions.html",
                "heating-cable.html",
                "thermostats.html",
                "components-accessories.html",
            ],
        )
        for link in links:
            self.assertTrue((ROOT / link.get("href")).is_file(), link.get("href"))

    def test_shared_shell_and_contact_actions(self):
        self.assertEqual(len(self.tree.xpath("//header[contains(@class, 'site-header')]")), 1)
        self.assertEqual(len(self.tree.xpath("//footer[@id='contacts']")), 1)
        self.assertGreaterEqual(len(self.tree.xpath("//*[@data-lead-open]")), 4)

    def test_project_gallery_uses_existing_images(self):
        images = self.tree.xpath("//section[contains(@class, 'about-projects')]//img/@src")
        self.assertEqual(len(images), 3)
        for source in images:
            self.assertTrue((ROOT / source).is_file(), source)


if __name__ == "__main__":
    unittest.main()
