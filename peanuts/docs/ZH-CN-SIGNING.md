# Peanuts Native 简体中文测试版：固定签名

本分支的 Actions 构建只上传用同一把专用密钥签名、且证书指纹已核对的 APK。应用名是
Peanuts Native，包名保持 `dev.nxnative.android.peanutszh`，不替代上游发行版。
如果 GitHub 没有配置密钥或指纹，构建会在安装依赖前停止，不会上传临时签名版本。

## 一次性设置

1. 在自己的电脑上用 JDK 的 `keytool` 创建此分支专用的 PKCS#12 密钥库。不要使用
   Android SDK 的默认调试密钥、上游发行密钥、密码样例或公开密钥。以下命令会
   提示输入自己的密码：

   ```sh
   keytool -genkeypair -keystore peanuts-zh-signing.p12 -storetype PKCS12 \
     -alias peanuts-zh -keyalg RSA -keysize 4096 -validity 10000 \
     -dname 'CN=Peanuts Native zh-CN'
   ```

2. 把 `peanuts-zh-signing.p12` 和密码安全备份在自己控制的地方，保持可以恢复。
   不要提交到 Git，不要放进聊天、Issue、Actions 缓存或制品。GitHub Secrets
   不能用来取回原文，不能代替备份。
3. 在仓库 **Settings → Secrets and variables → Actions** 配置：
   - Secret `PN_ZH_KEYSTORE_B64`：密钥库文件的 Base64 文本。
   - Secret `PN_ZH_KEYSTORE_PASSWORD`：同一密钥库密码。
   - Variable `PN_ZH_CERT_SHA256`：从密钥库导出的认证证书 SHA-256 十六进制指纹，
     64 个字符，不含空格或冒号。证书指纹是公开信息，不是密码。

   如已登录 GitHub CLI，macOS/Linux 也可在保存密钥库的目录中运行：

   ```sh
   base64 < peanuts-zh-signing.p12 | tr -d '\r\n' | \
     gh secret set PN_ZH_KEYSTORE_B64 --repo Fuck996/peanuts-native
   gh secret set PN_ZH_KEYSTORE_PASSWORD --repo Fuck996/peanuts-native
   # 上一条交互式输入密码，不要把实际密码写在命令参数里。
   # 这条仅输出公开证书的指纹。
   fingerprint="$(keytool -exportcert -storetype PKCS12 \
     -keystore peanuts-zh-signing.p12 -alias peanuts-zh | shasum -a 256 | cut -d ' ' -f 1)"
   gh variable set PN_ZH_CERT_SHA256 --repo Fuck996/peanuts-native --body "$fingerprint"
   ```

在本分支的 Actions 运行页点 **Re-run failed jobs**；新任务在排队时读取仓库
Secrets。Gradle 以及下载依赖的步骤不接收密钥。签名步骤在临时目录中解码，
结束（包括异常退出）后删除密钥副本。只在 APK 的证书与指纹相同后上传 APK。

签名工作流和能修改其受信分支的账号都要由仓库所有者控制。只合并已审核的代码，
不要给陌生的 Pull Request 暴露此工作流的签名秘密。不要在版本更新时替换密钥或指纹。

## 安装和更新

以前 Actions 自动生成的 0.1.6 / 0.1.7 测试密钥无法从 APK 恢复，因此第一个固定签名
版本不能覆盖那些旧测试版。请自己先备份存档、游戏包与设置，再卸载旧测试版并装入新的
固定签名 APK。之后保持应用包名、签名证书不变，同版本修正和新版可覆盖安装。
`versionCode = 主版本 × 1000000 + 次版本 × 1000 + 补丁版本 + 1`（迁移时让 0.1.7 由 1007 升至 1008），
同版本的不同提交使用同一 versionCode，正常的版本升级会递增。构建产物的短提交 SHA
区分同版本的不同 APK。源代码、应用名、LSFG 选项和正版 Lossless.dll 的要求不变。
