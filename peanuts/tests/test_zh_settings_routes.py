"""Settings navigation uses source keys; Chinese labels are never reverse-translated."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

APP = Path(__file__).resolve().parents[2] / "android/app/src/main"


class SettingsRoutes(unittest.TestCase):
    def test_both_row_factories_store_canonical_title_and_values(self):
        for relative in ("nxnative/android/Ui.java", "peanuts/ui/PUi.java"):
            source = (APP / "java/dev" / relative).read_text(encoding="utf-8")
            self.assertIn("view.setTag(R.id.peanuts_source_text, title)", source)
            self.assertIn("t.setTag(R.id.peanuts_source_text, s)", source)
            self.assertIn("value.setTag(R.id.peanuts_source_text, s); value.setText(L10n.tr(s))", source)
        ids = ET.parse(APP / "res/values/peanuts_locale_ids.xml").getroot()
        self.assertIsNotNone(ids.find("./item[@name='peanuts_source_text'][@type='id']"))

    def test_routing_help_and_icons_are_independent_of_display(self):
        source = (APP / "java/dev/peanuts/ui/SettingsPage.java").read_text(encoding="utf-8")
        self.assertIn("Object source = v.getTag(R.id.peanuts_source_text);", source)
        self.assertIn("heading = sourceText((TextView) v)", source)
        self.assertIn("group.equalsIgnoreCase(sourceText((TextView) v))", source)
        self.assertIn("SettingsSections.place(it.title, it.heading)", source)
        self.assertIn("SettingsHelp.of(x.title)", source)
        self.assertIn("SettingsSections.icon(x.place, x.title, v != null ? sourceText(v) : null", source)
        self.assertIn("SettingsSearch.text(x.title, s.label, group, source)", source)
        self.assertIn('(shown == null ? "" : shown) + " " + tr(x.title)', source)


if __name__ == "__main__":
    unittest.main()
