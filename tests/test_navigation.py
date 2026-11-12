"""Keep the compact information navigation consistent across published pages."""
from pathlib import Path
import unittest

from lxml import html


ROOT = Path(__file__).resolve().parents[1] / "dist"
LEGACY_PAGES = {
    "pipe-freeze-protection.html",
    "pipeline-temperature-maintenance.html",
    "underfloor-heating.html",
    "household-reservoir-heating.html",
    "household-soil-heating.html",
}


class NavigationTest(unittest.TestCase):
    def test_information_navigation(self):
        pages = list(ROOT.glob("*.html"))
        self.assertTrue(pages)
        for path in pages:
            tree = html.fromstring(path.read_text())
            navs = tree.xpath(
                "//*[contains(concat(' ', normalize-space(@class), ' '), ' site-header ')]"
                "//*[contains(concat(' ', normalize-space(@class), ' '), ' nav-row-small ')]"
            )
            if path.name in LEGACY_PAGES:
                self.assertFalse(navs, path.name)
                continue
            self.assertEqual(len(navs), 1, path.name)
            links = navs[0].xpath("./a")
            self.assertEqual(
                [" ".join(link.text_content().split()) for link in links],
                ["О компании", "Каталог решений", "Контакты"],
                path.name,
            )
            expected = [
                "about.html",
                "catalog-solutions.html",
                "#contacts" if path.name in {"index.html", "about.html"} else "index.html#contacts",
            ]
            self.assertEqual([link.get("href") for link in links], expected, path.name)

    def test_navigation_script_is_cache_busted(self):
        for path in ROOT.glob("*.html"):
            tree = html.fromstring(path.read_text())
            self.assertIn(
                "assets/app.js?v=20261112-questionnaires-1",
                tree.xpath("//script[contains(@src, 'assets/app.js')]/@src"),
                path.name,
            )


if __name__ == "__main__":
    unittest.main()
