#!/usr/bin/env python3
"""Materialize the fork-only localization into a disposable build checkout, never commit generated sources."""
from pathlib import Path
import argparse, json, re, shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
APP = ROOT / 'android/app/src/main'
JAVA = APP / 'java'
I18N = JAVA / 'dev/peanuts/i18n'
D = 'dev.peanuts.i18n.DisplayZh'
L = 'dev.peanuts.i18n.L10n'
LITERAL = r'"(?:[^"\\]|\\.)*"'
PAIR = re.compile(r'm\.put\(\s*(' + LITERAL + r')\s*,\s*(' + LITERAL + r')\s*\);')

def replace_exact(text, old, new, path, minimum=1):
    pattern = re.compile(r"(?<![\w$])" + re.escape(old))
    n = len(pattern.findall(text))
    if n < minimum:
        raise RuntimeError(f'{path}: expected display hook not found: {old}')
    return pattern.sub(lambda _: new, text)

def read_catalog():
    mapping = {}
    for p in sorted((HERE / 'java').rglob('*.java')):
        mapping.update(dict(PAIR.findall(p.read_text())))
    for line in (HERE / 'new-labels.tsv').read_text().splitlines():
        if not line: continue
        key, value = line.split('\t', 1)
        mapping[json.dumps(key, ensure_ascii=False)] = json.dumps(value, ensure_ascii=False)
    return mapping

def apply():
    if I18N.exists():
        raise RuntimeError('Localization already materialized; use a clean checkout.')
    mapping = read_catalog()
    shutil.copytree(HERE / 'java/dev/peanuts/i18n', I18N)
    # The new labels are separate from the inherited catalog and take precedence.
    rows = []
    for line in (HERE / 'new-labels.tsv').read_text().splitlines():
        if not line: continue
        key, value = line.split('\t', 1)
        rows.append('        m.put(' + json.dumps(key, ensure_ascii=False) + ', ' + json.dumps(value, ensure_ascii=False) + ');')
    (I18N/'NewZh.java').write_text('package dev.peanuts.i18n;\nfinal class NewZh {\n    static void addTo(java.util.Map<String, String> m) {\n' + '\n'.join(rows) + '\n    }\n}\n')
    p = I18N/'L10n.java'
    p.write_text(replace_exact(p.read_text(), 'OverlayZh.addTo(m);', 'OverlayZh.addTo(m);\n            NewZh.addTo(m);', p))
    dest = APP/'res/values-b+zh+Hans'
    dest.mkdir(exist_ok=True)
    shutil.copy(HERE/'res/strings.xml', dest/'strings.xml')
    (APP/'res/values/peanuts_locale_ids.xml').write_text('<resources><item type="id" name="peanuts_source_text"/></resources>\n')

    # Central UI factory boundaries. Explicitly preserve raw labels for SettingsPage/GamePage routing.
    changed = set()
    for rel in ('dev/nxnative/android/Ui.java', 'dev/peanuts/ui/PUi.java'):
        p = JAVA/rel
        t=p.read_text()
        for old,new in [
            ('t.setText(s);', f'{D}.set(t, s);'),
            ('b.setText(s);', f'{D}.set(b, s);'),
            ('value.setText(s);', f'{D}.set(value, s);'),
            ('label.setText(s);', f'{D}.set(label, s);'),
        ]:
            t=replace_exact(t,old,new,p)
        for name in ('status','tag','note'):
            t=t.replace(f'{name}.setText(s);', f'{D}.set({name}, s);')
        t=t.replace('badge.setText(s == null ? "" : s);', f'{D}.set(badge, s == null ? "" : s);')
        t=t.replace('.setTitle(title)', f'.setTitle({L}.tr(title))').replace('.setMessage(message)', f'.setMessage({L}.tr(message))')
        p.write_text(t); changed.add(p)

    # Keep row titles, groups, icon selection, and control checks on source keys.
    for rel in ('dev/peanuts/ui/SettingsPage.java','dev/peanuts/ui/GamePage.java','dev/peanuts/ui/PagePlace.java'):
        p=JAVA/rel
        t=p.read_text()
        t=re.sub(r'\(\(TextView\) ([^;\n]+?)\)\.getText\(\)', lambda m: D+'.source((TextView) '+m.group(1)+')',t)
        if p.name=='GamePage.java':
            t=t.replace('((Button) v).getText()',D+'.source((Button) v)')
        for var in ('v','val'):
            t=re.sub(r'(?<![\w$])'+var+r'\.getText\(\)',D+'.source('+var+')',t)
        if p.name=='SettingsPage.java':
            # Include both canonical and translated strings when searching; preserve help lookup.
            old='texts.add(SettingsSearch.text(x.title, s.label, SettingsSections.MORE.equals(x.place.group) ? null : x.place.group, '+D+'.source(v)'+'));'
            # actual source includes a null guard
            old='texts.add(SettingsSearch.text(x.title, s.label, SettingsSections.MORE.equals(x.place.group) ? null : x.place.group, v == null ? null : '+D+'.source(v)'+'));'
            new='texts.add(SettingsSearch.text(x.title, s.label, SettingsSections.MORE.equals(x.place.group) ? null : x.place.group, v == null ? null : '+D+'.source(v)'+') + " " + '+L+'.tr(x.title) + " " + '+L+'.tr(s.label) + " " + '+L+'.tr(x.place.group) + " " + (v == null ? "" : v.getText()));'
            t=replace_exact(t,old,new,p)
        p.write_text(t); changed.add(p)

    # Only known dictionary literals at UI call sites; leave persisted values, IDs, comparisons,
    # user-entered names, and protocol strings untouched. Apply to fresh upstream each build.
    methods = r'\.(?:setTitle|setMessage|setPositiveButton|setNegativeButton|setNeutralButton|setContentDescription|setHint|setText|setLabel)\(\s*'
    pattern = re.compile('('+methods+')('+LITERAL+r')(?=\s*[,\)])')
    # Only choice arrays passed to Android display APIs, not arrays used for storage.
    array = re.compile(r'(\.set(?:SingleChoiceItems|MultiChoiceItems|Items)\(\s*)(new (?:String|CharSequence)\[\]\s*\{[^{}]*\}|(?:[A-Za-z_$][\w$]*\.)+[A-Z_][A-Z_0-9]*|(?:items|labels|names|choices))(?=\s*,)')
    skip={'HudSettings.java','Overlay.java'}  # direct text-based logic handled below
    for p in JAVA.rglob('*.java'):
        if I18N in p.parents: continue
        t=p.read_text()
        orig=t
        if p.name not in skip:
            t=pattern.sub(lambda m: m[1]+L+'.tr('+m[2]+')' if m[2] in mapping else m[0], t)
        t=array.sub(lambda m:m[1]+L+'.items('+m[2]+')',t)
        # Explicit dynamic dialog labels and buttons in shared builder are safe since callbacks use indices.
        if p.name=='PadFocus.java':
            t=t.replace('super.setPositiveButton(text,',f'super.setPositiveButton({L}.tr(text),')
        if p.name=='CatalogActivity.java':
            t=replace_exact(t, '"Remove".contentEquals(b.getText())', '"Remove".contentEquals('+D+'.source(b))', p)
        if p.name=='Overlay.java':
            t=replace_exact(t,'b.setText(it[1]);',D+'.set(b, it[1]);',p)
            t=replace_exact(t,'master.setText("Show the overlay over the game" + (masterNote != null ? masterNote : ""));',D+'.set(master, "Show the overlay over the game" + (masterNote != null ? masterNote : ""));',p)
        if p.name=='BottomPanel.java':
            for name, value in [('exTitle','e.title'), ('exPlace','e.place'), ('exText','e.text'), ('exNow','e.value'), ('cardState','k.state'), ('buildBody','b.body')]:
                t=replace_exact(t,name+'.setText('+value+');',D+'.set('+name+', '+value+');',p)
            t=t.replace('exDefault.setText("App default: " + e.deflt);','exDefault.setText(String.format('+L+'.tr("App default: %s"), '+L+'.tr(e.deflt)));')
        if p.name=='SidePanel.java':
            for name, value in [('t','TAB_NAMES[i]'),('h','t'),('n','t'),('b','ScreenMode.NAMES[k]'),('b','Prefs.paceLabel(choices[i])'),('cb','opt.label'),('b','p.modeLabel(k)'),('b','names[i]'),('l','what[k]'),('b','PanelLook.NAMES[i]')]:
                t=t.replace(name+'.setText('+value+');',D+'.set('+name+', '+value+');')
        if p.name=='HudSettings.java':
            t=t.replace('((CheckBox) v).getText()', D+'.source((CheckBox) v)').replace('b.getText()',D+'.source(b)')
            t=t.replace('name.setText(title);',f'{D}.set(name, title);').replace('val.setText(names[i] +',f'val.setText({L}.tr(names[i]) +')
            t=t.replace('.setTitle(title)',f'.setTitle({L}.tr(title))').replace('.setNegativeButton("Cancel",',f'.setNegativeButton({L}.tr("Cancel"),')
        if t!=orig:
            p.write_text(t); changed.add(p)
    print(f'Materialized {len(mapping)} label mappings and {len(changed)} generated UI source files.')

if __name__ == '__main__':
    apply()
