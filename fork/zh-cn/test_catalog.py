"""Validate fork-only language resources and keep translation separate from preferences."""
from collections import Counter
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / 'android/app/src/main'
I18N = APP / 'java/dev/peanuts/i18n'
PAIR = re.compile(r'm\.put\(\s*"((?:[^"\\]|\\.)*)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*\);')
FORMAT = re.compile(r'%\d*\$?(?:\.\d+)?[sdfoxXeEgG]')


class Catalog(unittest.TestCase):
    def test_translation_tables(self):
        known = {}
        for path in sorted(p for p in I18N.glob('*.java') if p.name != 'DisplayZh.java'):
            pairs = PAIR.findall(path.read_text(encoding='utf-8'))
            self.assertGreater(len(pairs), 0, path)
            self.assertEqual(len(pairs), len(dict(pairs)), path)
            for english, chinese in pairs:
                with self.subTest(resource=path.name, english=english):
                    self.assertEqual(Counter(FORMAT.findall(english)), Counter(FORMAT.findall(chinese)))
                    self.assertNotEqual(english, 'Peanuts Native')
                    self.assertNotIn('花生', chinese, 'keep the brand in English')
                known[english] = chinese
        for required in ('Library', 'Upscaler', 'Frame generation', 'Settings'):
            self.assertIn(required, known)

    def test_xml_formats_and_array_indices(self):
        base = ET.parse(APP / 'res/values/strings.xml').getroot()
        zh = ET.parse(APP / 'res/values-b+zh+Hans/strings.xml').getroot()
        src = {e.attrib['name']: e for e in base}
        for e in zh:
            n = e.attrib['name']
            self.assertIn(n, src)
            self.assertEqual(e.tag, src[n].tag, n)
            self.assertEqual(len(e), len(src[n]), n)
            self.assertEqual(FORMAT.findall(''.join(e.itertext())), FORMAT.findall(''.join(src[n].itertext())), n)
            self.assertNotEqual(n, 'app_name')

    @unittest.skipUnless(shutil.which('javac') and shutil.which('java'), 'no JDK')
    def test_locale_switch_jvm(self):
        with tempfile.TemporaryDirectory(prefix='peanuts_zh_') as tmp:
            test = Path(tmp) / 'CatalogSmoke.java'
            test.write_text("""
import java.util.Locale;
import dev.peanuts.i18n.L10n;
public final class CatalogSmoke {
    public static void main(String[] args) {
        Locale initial = Locale.getDefault();
        try {
            Locale.setDefault(Locale.forLanguageTag("zh-Hans-CN"));
            if (!"设置".equals(L10n.tr("Settings"))) throw new AssertionError("Simplified Chinese");
            if (!"Peanuts Native".equals(L10n.tr("Peanuts Native"))) throw new AssertionError("brand");
            String[] original = {"Cancel", "Peanuts Native"};
            CharSequence[] display = L10n.items(original);
            if (!"取消".equals(display[0]) || !"Cancel".equals(original[0])) throw new AssertionError("labels only");
            Locale.setDefault(Locale.TAIWAN);
            if (!"Settings".equals(L10n.tr("Settings"))) throw new AssertionError("Traditional Chinese fallback");
            Locale.setDefault(Locale.ENGLISH);
            if (!"Settings".equals(L10n.tr("Settings"))) throw new AssertionError("English fallback");
        } finally {
            Locale.setDefault(initial);
        }
    }
}
""", encoding='utf-8')
            subprocess.run(['javac', '-encoding', 'UTF-8', '-d', tmp, *map(str, sorted(p for p in I18N.glob('*.java') if p.name != 'DisplayZh.java')), str(test)], check=True)
            subprocess.run(['java', '-cp', tmp, 'CatalogSmoke'], check=True)


if __name__ == '__main__':
    unittest.main()
