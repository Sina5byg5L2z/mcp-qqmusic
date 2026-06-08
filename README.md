# mcp-qqmusic

基于 [QQMusicApi](https://github.com/L-1124/QQMusicApi) 的 [MCP](https://modelcontextprotocol.io/) 服务器，让 AI 助手可以直接搜索、播放和管理 QQ 音乐。

## 功能

9 个工具，覆盖 QQ 音乐核心能力：

| 工具 | 功能 | 参数 |
|------|------|------|
| `search` | 搜索歌曲/歌手/专辑/歌单/MV + 热搜榜 + 搜索联想 | `keyword`, `type`(song/singer/album/songlist/mv/hotkey/complete), `page`, `size` |
| `detail` | 查看歌曲/专辑/歌手/歌单/榜单详情 | `type`(song/album/singer/songlist/top), `id`, `page`, `size` |
| `lyric` | 获取歌词（自动解密 QRC） | `id`, `trans`, `roma` |
| `url` | 获取播放链接 | `mid`, `quality`(standard/high/lossless) |
| `recommend` | 推荐新歌/歌单/猜你喜欢 | `type`(song/songlist/guess) |
| `similar` | 相似歌曲/相似歌手推荐 | `id`, `type`(song/singer) |
| `producer` | 查看歌曲制作信息（词曲编录等） | `id` |
| `hot_comments` | 获取歌曲热门评论 | `id`, `size` |
| `top` | 排行榜分类/榜单详情 | `type`(category/detail), `id`, `page`, `size` |

## 安装

前置要求：Python >= 3.10，推荐使用 [uv](https://docs.astral.sh/uv/) 包管理器。

```bash
git clone https://github.com/Sina5byg5L2z/mcp-qqmusic.git
cd mcp-qqmusic
uv sync
```

## 登录

部分功能（播放链接、专辑详情等）需要 QQ 音乐登录凭证。运行登录脚本扫码：

```bash
uv run python login.py
```

支持三种扫码方式：

1. **QQ 扫码** — 手机 QQ 扫描二维码
2. **微信扫码** — 手机微信扫描二维码
3. **QQ音乐APP扫码** — QQ 音乐 APP 扫描二维码

登录成功后凭证自动保存到 `credential.json`，MCP Server 每次调用需要登录的功能时动态加载，无需重启即可生效。

> `credential.json` 包含登录密钥，请妥善保管，不要泄露或提交到公开仓库（已在 `.gitignore` 中排除）。

## 接入 MCP 客户端

### Claude Desktop

编辑配置文件（`%APPDATA%\Claude\claude_desktop_config.json` 或 `~/Library/Application Support/Claude/claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "qqmusic": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp-qqmusic", "mcp-qqmusic"]
    }
  }
}
```

### 其他客户端

以 stdio 模式运行：

```bash
uv run mcp-qqmusic
```

## 项目结构

```
mcp-qqmusic/
├── login.py                  # 登录脚本（扫码获取凭证）
├── credential.json           # 登录凭证（自动生成，不入 git）
├── pyproject.toml
├── README.md
├── LICENSE
└── src/mcp_qqmusic/
    ├── __init__.py
    ├── __main__.py
    ├── server.py             # MCP Server（9 个工具，直接调用 SDK）
    └── format.py             # 紧凑文本格式化（节省 LLM 上下文）
```

## 工作原理

MCP Server 直接调用 [QQMusicApi](https://github.com/L-1124/QQMusicApi) Python SDK 与 QQ 音乐 API 交互，无需额外启动 HTTP 中间层：

```
LLM 客户端  ←──MCP/stdio──→  mcp-qqmusic  ←──SDK──→  QQ 音乐 API
```

响应格式化为紧凑结构化文本，而非原始 JSON，以最小化占用 LLM 上下文。

## 致谢

- [L-1124/QQMusicApi](https://github.com/L-1124/QQMusicApi) — QQ 音乐 API Python SDK

## 免责声明

本项目仅用于对技术可行性的探索及研究，请勿将其用于任何商业用途或侵犯版权的行为。

⚠️ 由于使用本项目产生的包括由于本协议或由于使用或无法使用本项目而引起的任何性质的任何直接、间接、特殊、偶然或结果性损害（包括但不限于因商誉损失、停工、计算机故障或故障引起的损害赔偿，或任何及所有其他商业损害或损失）由使用者负责。

## 许可证

MIT
