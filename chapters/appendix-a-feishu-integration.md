# 附录 A：接入飞书机器人

> 将 OpenClaw 接入飞书，在聊天软件中指挥 AI 干活

---

## A.1 为什么接入飞书？

OpenClaw 原生支持 WhatsApp、Telegram、Discord 等海外平台，但国内用户更习惯使用飞书、钉钉等国产即时通讯软件。

**接入飞书的好处**：
- ✅ 在飞书中直接指挥 AI 干活
- ✅ 支持个人聊天和群组聊天
- ✅ 消息实时推送
- ✅ 可访问飞书文档、日历等能力

---

## A.2 创建飞书机器人

### A.2.1 进入飞书开发者后台

1. 访问飞书开放平台：https://open.feishu.cn
2. 登录飞书账号（没有账号需要先注册）
3. 点击右上角 **开发者后台**

![飞书开发者后台入口](images/feishu-dev-portal.png)

### A.2.2 创建应用

1. 点击 **创建应用**
2. 选择 **自建应用**
3. 填写应用名称（如：OpenClaw 助手）
4. 选择应用类型：**企业自建**
5. 点击 **创建**

![创建飞书应用](images/feishu-create-app.png)

### A.2.3 填写应用信息

1. 填写应用名称、描述
2. 上传应用图标（可选）
3. 点击 **保存**

![填写应用信息](images/feishu-app-info.png)

### A.2.4 获取应用凭证

1. 进入 **凭证管理** 页面
2. 记录 **App ID** 和 **App Secret**

> ⚠️ 重要：App Secret 只显示一次，请立即保存！

![获取应用凭证](images/feishu-credentials.png)

### A.2.5 添加机器人

1. 进入 **添加机器人** 页面
2. 点击 **添加机器人**
3. 填写机器人名称（如：OpenClaw）
4. 上传机器人头像
5. 点击 **保存**

![添加机器人](images/feishu-add-bot.png)

### A.2.6 配置应用权限

1. 进入 **权限管理** 页面
2. 搜索并添加以下权限：
   - `im:message` - 发送和接收消息
   - `im:message:send` - 发送消息
   - `im:file` - 访问文件
   - `contact:contact` - 获取通讯录信息
3. 点击 **保存**

![配置权限](images/feishu-permissions.png)

### A.2.7 创建版本并发布

1. 进入 **版本管理与发布** 页面
2. 点击 **创建版本**
3. 填写版本号（如：1.0.0）
4. 填写更新说明
5. 点击 **提交审核**

![创建版本](images/feishu-create-version.png)

6. 等待审核通过（通常几分钟）
7. 点击 **发布为在线应用**

![发布应用](images/feishu-publish.png)

### A.2.8 在飞书中审批

1. 打开飞书客户端
2. 进入 **审批**
3. 找到应用发布审批
4. 点击 **同意**

![飞书审批](images/feishu-approve.png)

---

## A.3 安装飞书插件

### A.3.1 安装插件

打开 PowerShell，执行：

```bash
openclaw plugins install @m1heng-clawd/feishu
```

### A.3.2 配置飞书插件

1. 打开新的 PowerShell 窗口
2. 执行配置命令：

```bash
openclaw config
```

3. 选择配置项：**Feishu**
4. 输入之前获取的 **App ID** 和 **App Secret**
5. 域名选择：**中国**
6. 接受群组聊天：**Yes**
7. 选择 **Open** 打开配置
8. 选择 **Continue** 完成配置

![配置飞书插件](images/feishu-plugin-config.png)

### A.3.3 重启服务

配置完成后，重启 OpenClaw 服务：

```bash
openclaw gateway restart
```

---

## A.4 配置事件回调

### A.4.1 回到飞书后台

1. 进入 **事件订阅** 页面
2. 选择 **使用长连接接收事件**

![事件订阅](images/feishu-event-subscription.png)

### A.4.2 添加事件

1. 点击 **添加事件**（现在应该是可点击状态）
2. 搜索并添加：`im.message.receive_v1`（接收消息事件）
3. 点击 **保存**

![添加接收消息事件](images/feishu-add-event.png)

### A.4.3 获取用户信息权限

1. 进入 **权限管理**
2. 添加 **获取用户基本信息** 权限
3. 点击 **保存**

### A.4.4 重新发布版本

1. 进入 **版本管理与发布**
2. 创建新版本（如：1.0.1）
3. 提交审核并发布

---

## A.5 在飞书中与 AI 对话

### A.5.1 找到机器人

1. 打开飞书客户端或手机 App
2. 在联系人中找到刚才创建的机器人
3. 点击进入聊天窗口

![飞书机器人聊天](images/feishu-chat.png)

### A.5.2 测试对话

发送消息测试：

```
你好，请介绍一下你自己
```

机器人应该回复类似：

```
你好！我是你的 AI 助手 OpenClaw，可以帮你：
- 回答各种问题
- 执行电脑操作
- 管理文件和文档
- 查询信息和新闻
...

有什么我可以帮你的吗？
```

### A.5.3 访问本地文件

让机器人读取本地文件：

```
帮我读取 ~/.openclaw/workspace/MEMORY.md 文件的内容
```

> ⚠️ 注意：如果无法读取文件，需要在 OpenClaw 主配置文件中开启工具权限。

---

## A.6 常见问题

### Q1: 安装飞书插件提示"spawn npm ENOENT"

**问题原因**：npm 命令找不到，可能是 OpenClaw 的 bug。

**解决方法**：

1. 找到 exec.js 文件：
   ```
   C:\Users\Administrator\AppData\Roaming\fnm\node-versions\v22.14.0\installation\node_modules\openclaw\dist\process\exec.js
   ```

2. 修改 `runCommandWithTimeout` 函数中的 spawn 调用：

**修改前**：
```javascript
const stdio = resolveCommandStdio({ hasInput, preferInherit: true });
const child = spawn(argv[0], argv.slice(1), {
  stdio,
  cwd,
  env: resolvedEnv,
  windowsVerbatimArguments,
});
```

**修改后**：
```javascript
const stdio = resolveCommandStdio({ hasInput, preferInherit: true });
// On Windows, npm must be spawned with shell: true or use .cmd extension
let command = argv[0];
let useShell = false;
if (process.platform === "win32" && path.basename(command) === "npm") {
  useShell = true;
}
const child = spawn(command, argv.slice(1), {
  stdio,
  cwd,
  env: resolvedEnv,
  shell: useShell,
});
```

3. 保存文件，重启服务

### Q2: 飞书发送消息报错"Cannot convert argument to a ByteString"

**问题原因**：消息中包含中文字符，编码问题。

**解决方法**：
- 检查飞书插件版本，升级到最新版
- 或在 OpenClaw 配置中设置正确的字符编码

### Q3: 机器人不回复消息

**排查步骤**：

1. 检查飞书应用是否已发布为在线应用
2. 检查事件订阅是否配置正确
3. 检查权限是否已开通
4. 查看 OpenClaw 日志：
   ```bash
   openclaw logs
   ```

---

## A.7 成本说明

- **OpenClaw 软件**：完全免费
- **飞书平台**：免费使用
- **AI 模型 API**：需要付费（可选择国产大模型降低成本）

**建议**：
- 使用智谱 GLM、通义千问等国产模型
- 设置每日 token 预算
- 定期查看 API 使用量

---

## A.8 进阶配置

### A.8.1 群组聊天

在配置插件时选择 **接受群组聊天**，机器人就可以在群组中响应消息。

### A.8.2 访问飞书文档

配置飞书文档权限后，可以让 AI 读取和编辑飞书文档。

### A.8.3 定时任务

结合 OpenClaw 的 Heartbeat 功能，可以设置定时任务。

---

**本章完成时间**：2026-03-16
**最后更新**：2026-03-16
