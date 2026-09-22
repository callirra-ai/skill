# Callirra 媒体生成 Skill

开源 AI Agent 技能包，让 Claude Code、Codex、Cursor 等 Agent 可以直接调用 Callirra 生成图像和视频。

## 环境要求

- Python 3.10+
- Callirra API Key（`sk-cal-...`）

## 安装

> ⚠️ **内置模板目录与 `enhance`（一句话扩写）已下线（2026-09），不再恢复**：`PROMPT_TEMPLATES` 现为空数组，
> `GET /api/v1/prompts/templates` 返回空列表，`POST /v1/prompts/enhance` 依赖的 `templateId` 已不存在（404）。
>
> **替代方案是随 skill 一起分发的配方库**（离线、不需要 key）：`recipes` 列出 172 条配方、`recipe <slug>` 打印
> 完整提示词与参数、`scenes` 是 6 个实测场景。这些偏视频；**图片**提示词请用网站的 Image Prompts Studio 模板。

```bash
npx skills add callirra-ai/skill --all
```

然后保存一次 API Key：

```bash
python3 scripts/callirra_api.py setup-api-key "<你的-API-Key>"
```

在 [callirra.com](https://callirra.com?utm_source=github-skill) 获取 API Key。

## 命令

```bash
# 账户
python3 scripts/callirra_api.py balance
python3 scripts/callirra_api.py usage --limit 10

# 模型
python3 scripts/callirra_api.py models

# 提示词库（随 skill 分发，离线可用、不需要 key）
python3 scripts/callirra_api.py recipes
python3 scripts/callirra_api.py recipe bridge-pursuit-headlights
python3 scripts/callirra_api.py scenes
python3 scripts/callirra_api.py scenes wedding

# 创意知识库（加 --full 输出完整 JSON）
python3 scripts/callirra_api.py creative
python3 scripts/callirra_api.py creative --full

# 生成
python3 scripts/callirra_api.py generate-image \
  --model nano-banana-2 \
  --prompt "电影感产品图" \
  --size 1024x1024 \
  --out hero.png

python3 scripts/callirra_api.py generate-video \
  --model seedance-2.5 \
  --prompt "航拍镜头" \
  --duration 10 \
  --resolution 720p \
  --wait \
  --out clip.mp4

# 任务管理
python3 scripts/callirra_api.py task <TASK_ID>
python3 scripts/callirra_api.py cancel <TASK_ID>

# 上传参考图
python3 scripts/callirra_api.py upload --file ./frame.png --content-type image/png
```

## 文件结构

- `SKILL.md` — 主技能说明
- `scripts/callirra_api.py` — 零依赖 Python CLI
- `references/callirra-api-reference.md` — API 参考
- `references/creative-knowledge.json` — 完整创意知识库（110 资源、8 分类、39 风格）
- `workflows/` — 可复用工作流

## License

MIT. 源码：[github.com/callirra-ai/skill](https://github.com/callirra-ai/skill?utm_source=github-skill)

---

在 [callirra.com](https://callirra.com?utm_source=github-skill) 免费开始。