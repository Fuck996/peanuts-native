"""Checks that the generated localization leaves upstream routing and original option values intact."""
from pathlib import Path
import re, unittest
ROOT=Path(__file__).resolve().parents[2]
JAVA=ROOT/'android/app/src/main/java'
class Routes(unittest.TestCase):
    def test_factories(self):
        for p in (JAVA/'dev/nxnative/android/Ui.java',JAVA/'dev/peanuts/ui/PUi.java'):
            text=p.read_text()
            self.assertIn('DisplayZh.set(t, s)', text)
            self.assertIn('DisplayZh.set(value, s)', text)
        adapter=(JAVA/'dev/peanuts/i18n/DisplayZh.java').read_text()
        self.assertIn('setTag(R.id.peanuts_source_text, source)', adapter)
        self.assertIn('view.setText(L10n.tr(source))', adapter)
    def test_settings_and_games(self):
        for file in ('SettingsPage.java','GamePage.java','PagePlace.java'):
            text=(JAVA/'dev/peanuts/ui'/file).read_text()
            self.assertIn('DisplayZh.source(',text)
        settings=(JAVA/'dev/peanuts/ui/SettingsPage.java').read_text()
        self.assertIn('SettingsSearch.text(x.title, s.label',settings)
        self.assertIn('L10n.tr(x.title)',settings)
        game=(JAVA/'dev/peanuts/ui/GamePage.java').read_text()
        self.assertIn('"Reset to defaults".contentEquals(dev.peanuts.i18n.DisplayZh.source',game)
    def test_companion_remove_and_hud(self):
        self.assertIn('"Remove".contentEquals(dev.peanuts.i18n.DisplayZh.source(b))',(JAVA/'dev/peanuts/CatalogActivity.java').read_text())
        hud=(JAVA/'dev/peanuts/overlay/HudSettings.java').read_text()
        self.assertIn('DisplayZh.source((CheckBox) v)',hud)
        self.assertIn('pick.on(values[w])',hud)
if __name__=='__main__': unittest.main()
