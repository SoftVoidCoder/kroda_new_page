"""Check the four questionnaire routes and direct CTA wiring."""
from pathlib import Path
import unittest

from lxml import html


ROOT = Path(__file__).resolve().parents[1] / "dist"


class QuestionnaireTest(unittest.TestCase):
    def setUp(self):
        self.page = ROOT / "questionnaires.html"
        self.tree = html.fromstring(self.page.read_text())

    def test_four_questionnaires_exist(self):
        forms = self.tree.xpath("//form[@data-questionnaire-form]")
        self.assertEqual(
            [form.get("data-questionnaire-form") for form in forms],
            ["pipelines", "tanks", "roof", "open-areas"],
        )
        for form in forms:
            self.assertEqual(form.get("action"), "/api/questionnaire")
            self.assertEqual(form.get("enctype"), "multipart/form-data")
            names = form.xpath(".//*[@name]/@name")
            for common in ("questionnaire_type", "object_name", "contacts[0][name]", "attachments[]", "consent"):
                self.assertIn(common, names)

    def test_source_specific_fields_are_present(self):
        names = set(self.tree.xpath("//*[@name]/@name"))
        for name in (
            "pipelines[0][diameter_mm]",
            "fill_coefficient",
            "valleys[0][length_m]",
            "downpipes[0][funnel_diameter_mm]",
            "surface_thickness_cm",
            "delivery_scope[]",
        ):
            self.assertIn(name, names)

    def test_picker_has_direct_routes(self):
        self.assertEqual(
            self.tree.xpath("//nav[contains(@class,'questionnaire-picker')]/a/@href"),
            [
                "questionnaires.html?type=pipelines",
                "questionnaires.html?type=tanks",
                "questionnaires.html?type=roof",
                "questionnaires.html?type=open-areas",
            ],
        )

    def test_shared_script_routes_profile_pages(self):
        script = (ROOT / "assets/app.js").read_text()
        for page, form_type in (
            ("pipeline-heating.html", "pipelines"),
            ("household-reservoir-heating.html", "tanks"),
            ("household-roof-gutter-heating.html", "roof"),
            ("household-open-area-heating.html", "open-areas"),
        ):
            self.assertIn(f"'{page}': '{form_type}'", script)
        self.assertIn("Заполнить опросный лист", script)

    def test_required_checkbox_groups_are_checked(self):
        script = (ROOT / "assets/questionnaires.js").read_text()
        for name in ("heating_purpose[]", "insulation_coverage[]", "drawings_format[]", "heated_area_types[]", "delivery_scope[]"):
            self.assertIn(name, script)


if __name__ == "__main__":
    unittest.main()
