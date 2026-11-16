"""Keep final punctuation consistent in short interface copy."""

from pathlib import Path
import unittest

from scripts.remove_short_copy_periods import strip_short_copy


DIST = Path(__file__).resolve().parents[1] / "dist"


class ShortCopyPunctuationTest(unittest.TestCase):
    def test_short_blocks_do_not_end_with_full_stop(self):
        offenders = []
        for path in sorted(DIST.glob("*.html")):
            _, changes = strip_short_copy(path.read_text(encoding="utf-8"))
            if changes:
                offenders.append(f"{path.name}: {changes}")
        self.assertEqual(offenders, [])

    def test_internal_and_long_form_punctuation_is_preserved(self):
        source = (
            "<p>Первое предложение. Второе предложение.</p>"
            f"<p>{'Длинный текст. ' * 20}</p>"
        )
        updated, changes = strip_short_copy(source)
        self.assertEqual(changes, 1)
        self.assertIn("Первое предложение. Второе предложение</p>", updated)
        self.assertIn("Длинный текст. Длинный текст.", updated)

    def test_abbreviation_period_is_preserved(self):
        updated, changes = strip_short_copy("<p>Кабели, оборудование и т.п.</p>")
        self.assertEqual(changes, 0)
        self.assertEqual(updated, "<p>Кабели, оборудование и т.п.</p>")

    def test_word_suffix_is_not_treated_as_abbreviation(self):
        updated, changes = strip_short_copy("<p>Рассчитываем длину и шаг.</p>")
        self.assertEqual(changes, 1)
        self.assertEqual(updated, "<p>Рассчитываем длину и шаг</p>")


if __name__ == "__main__":
    unittest.main()
