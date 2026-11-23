package dev.peanuts.i18n;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

/** Fork-local UI translation. Never use for protocols, IDs, stored settings or diagnostics. */
public final class L10n {
    private L10n() {}

    static boolean usesSimplifiedChinese(Locale locale) {
        if (!"zh".equals(locale.getLanguage())) return false;
        String script = locale.getScript();
        if (!script.isEmpty()) return "Hans".equals(script);
        String region = locale.getCountry();
        return !"TW".equals(region) && !"HK".equals(region) && !"MO".equals(region);
    }

    private static final class Catalog {
        static final Map<String, String> TEXT = build();

        static Map<String, String> build() {
            Map<String, String> m = new HashMap<>();
            m.put("OK", "确定");
            m.put("Cancel", "取消");
            m.put("Done", "完成");
            m.put("Back", "返回");
            m.put("Close", "关闭");
            m.put("Save", "保存");
            m.put("Delete", "删除");
            m.put("Remove", "移除");
            m.put("Continue", "继续");
            m.put("Open", "打开");
            m.put("Choose", "选择");
            m.put("Select", "选择");
            m.put("Edit", "编辑");
            m.put("Reset", "重置");
            m.put("Reset to defaults", "恢复默认设置");
            m.put("Clear", "清除");
            m.put("Search", "搜索");
            m.put("Default", "默认");
            m.put("System", "系统");
            m.put("Unknown", "未知");
            m.put("None", "无");
            m.put("Auto", "自动");
            m.put("On", "开");
            m.put("Off", "关");
            m.put("Enabled", "已启用");
            m.put("Disabled", "已停用");
            m.put("Details", "详细信息");
            m.put("Copy details", "复制详细信息");
            m.put("Start", "开始");
            m.put("Reset all settings", "重置所有设置");
            m.put("Details copied", "已复制详细信息");
            m.put("Hide details", "隐藏详细信息");
            m.put("Show details", "显示详细信息");
            m.put(": tap for details", "：点按查看详情");
            m.put(", tab", "，标签页");
            m.put(", tab, selected", "，已选中标签页");
            m.put("Recommended", "推荐");
            m.put("Changed", "已修改");
            m.put("Available", "可用");
            m.put("Unavailable", "不可用");
            m.put("Try again", "重试");
            m.put("Copy", "复制");
            m.put("Import", "导入");
            m.put("Export", "导出");
            m.put("Settings", "设置");
            m.put("Game", "游戏");
            m.put("Library", "游戏库");
            m.put("Help", "帮助");
            m.put("About", "关于");
            LauncherZh.addTo(m);
            SettingsZh.addTo(m);
            BuildZh.addTo(m);
            UpdatePackZh.addTo(m);
            UpdateSettingsZh.addTo(m);
            ProfilesZh.addTo(m);
            OverlayZh.addTo(m);
            return m;
        }
    }

    public static String tr(String s) {
        if (s == null || !usesSimplifiedChinese(Locale.getDefault())) return s;
        return Catalog.TEXT.getOrDefault(s, s);
    }

    /** Keep styled text and its existing spans intact. */
    public static CharSequence tr(CharSequence s) { return s instanceof String ? tr((String) s) : s; }

    public static CharSequence[] items(CharSequence[] items) {
        if (items == null || !usesSimplifiedChinese(Locale.getDefault())) return items;
        CharSequence[] display = new CharSequence[items.length];
        for (int i = 0; i < items.length; ++i) display[i] = tr(items[i]);
        return display;
    }
}
