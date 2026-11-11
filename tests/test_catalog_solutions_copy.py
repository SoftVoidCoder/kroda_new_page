"""Validate copy approved for the catalog solutions page."""
from pathlib import Path
import unittest

from lxml import html


ROOT = Path(__file__).resolve().parents[1] / "dist"


class CatalogSolutionsCopyTest(unittest.TestCase):
    def test_approved_labels(self):
        tree = html.fromstring((ROOT / "catalog-solutions.html").read_text())
        hero_label = tree.xpath("//section[contains(@class, 'catalog-hero')]//*[contains(@class, 'eyebrow')]")[0]
        intro = tree.xpath("//section[contains(@class, 'catalog-intro')]")[0]
        self.assertEqual(" ".join(hero_label.text_content().split()), "Собственное производство")
        self.assertEqual(" ".join(intro.xpath(".//*[contains(@class, 'eyebrow')]")[0].text_content().split()), "Каталог")
        self.assertEqual(" ".join(intro.xpath("./div/p")[0].text_content().split()), "Выберите направление, чтобы посмотреть изделия и услуги")


if __name__ == "__main__":
    unittest.main()
