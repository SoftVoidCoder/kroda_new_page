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

    def test_approved_copy_and_hero(self):
        page_text = " ".join(self.tree.text_content().split())
        hero = self.tree.xpath("//section[contains(@class, 'about-hero')]/img")[0]
        self.assertEqual(hero.get("src"), "assets/industrial/pipeline-node.webp")
        self.assertIn("Экспертиза и производственные компетенции", page_text)
        self.assertIn("Какой результат вы получите", page_text)
        self.assertIn("Расчёт, комплектное оборудование и решения для действующих промышленных объектов.", page_text)
        self.assertIn("В нашем портфолио компании — представители нефтяной, газовой, энергетической, химической и пищевой отраслей", page_text)
        self.assertNotIn("Инженерная экспертиза", page_text)
        self.assertNotIn("Инженерный результат", page_text)

    def test_client_section_uses_existing_logos(self):
        logos = self.tree.xpath("//div[contains(@class, 'client-list')]//img")
        self.assertEqual([logo.get("alt") for logo in logos], ["Газпром", "Транснефть", "Интер РАО", "PepsiCo"])
        for logo in logos:
            self.assertTrue((ROOT / logo.get("src")).is_file(), logo.get("src"))

    def test_other_tasks_link_to_tilda_pages(self):
        links = self.tree.xpath("//div[contains(@class,'expertise-grid')]/a/@href")
        self.assertEqual(len(links), 6)
        self.assertTrue(all(link.startswith("https://korda-izol.ru/") for link in links))
        self.assertIn("https://korda-izol.ru/tkanevye-kompensatory/", links)
        self.assertIn("https://korda-izol.ru/shumoizolyacionnye-chehly/", links)


if __name__ == "__main__":
    unittest.main()
