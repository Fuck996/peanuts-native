package dev.peanuts.i18n;

import java.util.Map;

/** Display strings added with the 0.1.7 package import flow. */
public final class UpdatePackZh {
    private UpdatePackZh() {}

    public static void addTo(Map<String, String> m) {
        m.put("A .zip file (made by Export pack…)", "ZIP 文件（由「导出游戏包」生成）");
        m.put("A pack folder (with pack.tsv and shaders/)", "游戏包文件夹（包含 pack.tsv 和 shaders/）");
        m.put("Graphics self-test", "图形自检");
        m.put("Import %s's pack from…", "从哪里导入 %s 的游戏包？");
        m.put("Import pack", "导入游戏包");
        m.put("Importing %s's pack…", "正在导入 %s 的游戏包…");
        m.put("It is checked before it replaces anything.", "应用会先校验游戏包，校验通过后才替换现有文件。");
        m.put("Open Settings › Library › Storage to free some space.", "请打开「设置 › 游戏库 › 存储」释放空间。");
        m.put("Pack imported", "已导入游戏包");
        m.put("Pack not imported", "未能导入游戏包");
        m.put("Pick the new pack", "选择新的游戏包");
        m.put("Pick the pack folder (the one with pack.tsv and shaders/)", "选择包含 pack.tsv 和 shaders/ 的游戏包文件夹");
        m.put("Pick the pack's .zip file", "选择游戏包的 ZIP 文件");
        m.put("Replace the pack?", "要替换游戏包吗？");
        m.put("Share log…", "分享日志…");
        m.put("That %s is not on the phone's storage by a path the app can read. Pick it from the phone's storage (the menu, then the phone's name), not from Recent, Downloads or a cloud provider.", "应用无法通过本机路径读取此%s。请在文件选择器菜单中点选设备名称，从设备存储选择，不要从「最近使用」「下载」或云端选择。");
        m.put("The app needs All files access to read the pack and write it where Build looks for it.", "应用需要「所有文件访问」权限来读取游戏包，并将其写入构建功能读取的位置。");
        m.put("The app needs All files access to read the pack. Allow it, then import the pack.", "应用需要「所有文件访问」权限才能读取游戏包。请授权后再导入。");
        m.put("The build log is no longer there (it is kept for a day). Open Share log again.", "构建日志已过期（只保留一天）。请重新打开「分享日志」。");
        m.put("file", "文件");
        m.put("folder", "文件夹");
    }
}
