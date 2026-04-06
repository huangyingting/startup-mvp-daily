# startup-mvp-daily

每天在 Startup 新闻里选一个最值得下注的方向，快速做成一个可展示的 MVP，并自动发布到 GitHub Pages。

## 已上线地址

- 网站首页：<https://huangyingting.github.io/startup-mvp-daily/>
- 仓库地址：<https://github.com/huangyingting/startup-mvp-daily>

## 仓库结构

- `content/projects/*.json`：每天的项目定义文件
- `scripts/build_site.py`：将 JSON 编译成 GitHub Pages 静态站点
- `docs/`：GitHub Pages 发布目录

## 本地构建

```bash
python3 scripts/build_site.py
```

## 每日自动化工作流

1. 搜索最近 7 天内的 Startup 新闻（AI / 教育 / 科技 / 养老 / 商业等）
2. 选出最有创意或潜力的一条
3. 生成一个新的 `content/projects/YYYY-MM-DD-slug.json`
4. 运行 `python3 scripts/build_site.py`
5. `git add . && git commit && git push`
6. 由 GitHub Pages 自动发布 `docs/`
