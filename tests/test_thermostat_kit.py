"""Check the two KIT variants against supplied product content and price list."""
from pathlib import Path
import hashlib
import json
import sys
import unittest
from lxml import html
from docx import Document
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_thermostat_catalog import ROOT, KIT_I_DOC, KIT_I_PDF, prices

class KitProductsTest(unittest.TestCase):
    def test_variants_and_prices(self):
        products = json.loads((ROOT/'assets/thermostats/products.json').read_text())
        self.assertEqual(len(products), 40)
        expected = {'thermostat-termostat-kit-lavita.html': '3 700 ₽', 'thermostat-kit-i.html': '1 700 ₽'}
        for url, price in expected.items():
            item = next(p for p in products if p['url'] == url)
            self.assertEqual(item['price'], price)
            tree = html.fromstring((ROOT/url).read_text())
            self.assertEqual(tree.xpath('//section[contains(@class,"cable-detail-hero")]//strong/text()'), [price])
        self.assertEqual(prices()['kit-i'], 1700)

    def test_new_description_and_passport(self):
        tree = html.fromstring((ROOT/'thermostat-kit-i.html').read_text())
        text = ' '.join(tree.xpath('//section[@class="cable-description"]')[0].text_content().split())
        for paragraph in Document(KIT_I_DOC).paragraphs[1:]:
            content = ' '.join(paragraph.text.split())
            if not content or content == '(Паспорт отдельным файлом)': continue
            self.assertIn(content.replace(':', '', 1) if content.startswith('Технические') else content.split(':',1)[-1].strip(), text)
        self.assertEqual(hashlib.sha256(KIT_I_PDF.read_bytes()).digest(),hashlib.sha256((ROOT/'assets/thermostats/kit-i-passport.pdf').read_bytes()).digest())
        self.assertIn('без влагозащиты', tree.xpath('//h1')[0].text_content())
        wp = html.fromstring((ROOT/'thermostat-termostat-kit-lavita.html').read_text())
        self.assertIn('Автоматическое выключение', wp.text_content())
        self.assertNotIn('Диапазон регулирования температуры', wp.text_content())

if __name__ == '__main__': unittest.main()
