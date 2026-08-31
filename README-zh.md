# Callirra 媒体生成 Skill

一个开源的 AI Agent 技能包，让 Claude Code、Codex、Cursor 等 Agent 可以直接调用 Callirra 生成图像和视频。

## 快速开始

```bash
python3 scripts/callirra_api.py setup-api-key "<你的-API-Key>"
```

然后让 Agent 使用 `$callirra-media-generator-skill` 创建图像或视频任务。

## 命令

```bash
python3 scripts/callirra_api.py models
python3 scripts/callirra_api.py balance
python3 scripts/callirra_api.py templates
python3 scripts/callirra_api.py enhance --template-id cinematic-city --idea "雨夜东京街头" --kind video
python3 scripts/callirra_api.py creative
python3 scripts/callirra_api.py generate-image --model nano-banana --prompt "电影感产品图" --out hero.png
python3 scripts/callirra_api.py generate-video --model seedance-2.5 --prompt "航拍镜头" --duration 10 --wait
```

## 文件结构

- `SKILL.md` — 主技能说明
- `scripts/callirra_api.py` — 零依赖 Python CLI
- `references/callirra-api-reference.md` — API 参考
- `references/creative-knowledge.json` — 完整创意知识库（110 资源、8 分类、39 风格）
- `workflows/` — 可复用工作流

---

→ 在 [callirra.com](https://callirra.com?utm_source=github-skill) 免费开始
