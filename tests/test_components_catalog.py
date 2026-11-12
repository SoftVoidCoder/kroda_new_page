"""Check the components catalog against the approved Word and TKR passport facts."""
from pathlib import Path
import unittest

from lxml import html


ROOT = Path(__file__).resolve().parents[1] / "dist"


class ComponentsCatalogTest(unittest.TestCase):
    def test_catalog_is_complete(self):
        tree = html.fromstring((ROOT / "components-accessories.html").read_text())
        self.assertEqual(len(tree.xpath("//*[@data-product]")), 21)
        self.assertEqual(
            len(tree.xpath("//*[@data-product]//a[normalize-space()='Заказать подбор']")),
            21,
        )
        self.assertEqual(len(tree.xpath("//*[contains(@class,'installation-gallery')]/figure")), 5)
        for section_id in (
            "termination-kits",
            "mounting-tapes",
            "cable-glands",
            "power-cables",
            "junction-boxes",
            "roof-fasteners",
        ):
            self.assertEqual(len(tree.xpath(f"//*[@id='{section_id}']")), 1)
        text = " ".join(tree.text_content().split())
        for value in ("1 050 ₽", "900 ₽", "1 150 ₽", "550 ₽", "850 ₽"):
            self.assertIn(value, text)
        for value in ("до 200 °C", "до 135 °C", "140 × 140 × 79 мм", "от −60 до +130 °C"):
            self.assertIn(value, text)

    def test_mockup_intro_and_pes_g_passport(self):
        tree = html.fromstring((ROOT / "components-accessories.html").read_text())
        text = " ".join(tree.text_content().split())
        self.assertIn("Всё необходимое для монтажа", text)
        self.assertIn("Подбор и монтаж электрических соединений", text)
        self.assertEqual(len(tree.xpath("//section[contains(@class,'components-directory')]//nav/a")), 6)
        passport = ROOT / "assets/components/passport-pes-g-lavita.pdf"
        self.assertGreater(passport.stat().st_size, 500_000)
        self.assertTrue(passport.read_bytes().startswith(b"%PDF"))
        self.assertEqual(
            tree.xpath("//a[contains(@href,'passport-pes-g-lavita.pdf')]/@href"),
            ["assets/components/passport-pes-g-lavita.pdf"],
        )

    def test_tkr_uses_tkr_values_only(self):
        tree = html.fromstring((ROOT / "component-tkr.html").read_text())
        text = " ".join(tree.text_content().split())
        self.assertIn("ESR", text)
        self.assertIn("от −60 до +125 °C", text)
        self.assertIn("125–170 °C", text)
        self.assertNotIn("+200 °C", text)
        self.assertNotIn("+250 °C", text)
        self.assertEqual(
            tree.xpath("//a[contains(@href,'passport-tkr-tks-tku-ekf.pdf')]/@href"),
            ["assets/components/passport-tkr-tks-tku-ekf.pdf"],
        )

    def test_assets_and_navigation_exist(self):
        passport = ROOT / "assets/components/passport-tkr-tks-tku-ekf.pdf"
        self.assertGreater(passport.stat().st_size, 600_000)
        self.assertTrue(passport.read_bytes().startswith(b"%PDF"))
        for path in ROOT.glob("*.html"):
            tree = html.fromstring(path.read_text())
            labels = tree.xpath("//a[normalize-space()='Комплектующие и аксессуары']/@href")
            if labels:
                self.assertTrue(all(link == "components-accessories.html" for link in labels), path)


if __name__ == "__main__":
    unittest.main()
