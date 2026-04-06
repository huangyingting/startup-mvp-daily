#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "projects"
DOCS_DIR = ROOT / "docs"
PROJECTS_DIR = DOCS_DIR / "projects"
ASSETS_DIR = DOCS_DIR / "assets"
FEED_PATH = DOCS_DIR / "feed.json"

SITE_TITLE = "Startup MVP Daily"
SITE_TAGLINE = "每天挑一条值得下注的 Startup 新闻，把它落成一个能上 GitHub Pages 的最小可行产品。"
SITE_URL = "https://huangyingting.github.io/startup-mvp-daily/"


def load_projects() -> list[dict[str, Any]]:
    projects: list[dict[str, Any]] = []
    for path in sorted(CONTENT_DIR.glob("*.json")):
        if path.name.startswith("."):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_source_file"] = path.name
        projects.append(data)
    projects.sort(key=lambda item: item["date"], reverse=True)
    return projects


def html_list(items: list[str], class_name: str = "bullet-list") -> str:
    return "".join(f"<li>{escape(item)}</li>" for item in items)


def cards(items: list[dict[str, str]]) -> str:
    return "".join(
        f"""
        <article class=\"info-card\">
          <h3>{escape(item['name'])}</h3>
          <p>{escape(item['description'])}</p>
        </article>
        """ for item in items
    )


def scenario_buttons(items: list[dict[str, Any]], project_slug: str) -> str:
    buttons = []
    panels = []
    for index, item in enumerate(items):
        active = "true" if index == 0 else "false"
        hidden = "" if index == 0 else "hidden"
        button_id = f"{project_slug}-scenario-{index}"
        panel_id = f"{project_slug}-panel-{index}"
        buttons.append(
            f'<button class="scenario-tab" data-tab-target="#{panel_id}" aria-pressed="{active}" id="{button_id}">{escape(item["name"])}</button>'
        )
        workflow = "".join(f"<li>{escape(step)}</li>" for step in item.get("workflow", []))
        panels.append(
            f"""
            <section class=\"scenario-panel\" id=\"{panel_id}\" {hidden}>
              <p class=\"eyebrow\">Use case</p>
              <h3>{escape(item['name'])}</h3>
              <p class=\"scenario-hook\">{escape(item['hook'])}</p>
              <ul class=\"workflow-list\">{workflow}</ul>
              <div class=\"metric-pill\">北极星指标：{escape(item['metric'])}</div>
            </section>
            """
        )
    return f"""
    <div class=\"scenario-shell\">
      <div class=\"scenario-tabs\">{''.join(buttons)}</div>
      <div class=\"scenario-panels\">{''.join(panels)}</div>
    </div>
    """


def layout(title: str, body: str, description: str, *, canonical: str = SITE_URL) -> str:
    return f"""<!doctype html>
<html lang=\"zh-CN\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>{escape(title)}</title>
    <meta name=\"description\" content=\"{escape(description)}\" />
    <meta property=\"og:title\" content=\"{escape(title)}\" />
    <meta property=\"og:description\" content=\"{escape(description)}\" />
    <meta property=\"og:type\" content=\"website\" />
    <meta property=\"og:url\" content=\"{escape(canonical)}\" />
    <link rel=\"canonical\" href=\"{escape(canonical)}\" />
    <link rel=\"stylesheet\" href=\"/startup-mvp-daily/assets/styles.css\" />
  </head>
  <body>
    {body}
    <script src=\"/startup-mvp-daily/assets/app.js\" defer></script>
  </body>
</html>
"""


def build_project_page(project: dict[str, Any]) -> str:
    source = project["source"]
    feature_cards = cards(project.get("features", []))
    scenarios = scenario_buttons(project.get("scenarios", []), project["slug"])
    signals = "".join(f"<li>{escape(item)}</li>" for item in project.get("news_signals", []))
    stack = html_list(project.get("stack", []))
    risks = html_list(project.get("risks", []))
    next_steps = html_list(project.get("next_steps", []))
    audiences = html_list(project.get("audiences", []))

    body = f"""
    <main class=\"page-shell\">
      <a class=\"top-link\" href=\"/startup-mvp-daily/\">← 返回首页</a>
      <section class=\"hero-card hero-card--project\">
        <p class=\"eyebrow\">{escape(project['date'])} · {escape(project['category'])}</p>
        <h1>{escape(project['title'])}</h1>
        <p class=\"lede\">{escape(project['tagline'])}</p>
        <div class=\"score-pill\">潜力评分 {escape(str(project['potential_score']))}/100</div>
        <div class=\"hero-grid\">
          <article>
            <p class=\"label\">新闻来源</p>
            <h2>{escape(source['title'])}</h2>
            <p>{escape(project['summary'])}</p>
            <a class=\"inline-link\" href=\"{escape(source['url'])}\" target=\"_blank\" rel=\"noreferrer\">查看原文 ↗</a>
          </article>
          <article>
            <p class=\"label\">为什么值得做</p>
            <p>{escape(project['why_now'])}</p>
            <p class=\"creative-edge\">{escape(project['creative_edge'])}</p>
          </article>
        </div>
      </section>

      <section class=\"content-grid\">
        <article class=\"section-card\">
          <p class=\"eyebrow\">Problem</p>
          <h2>要解决什么问题？</h2>
          <p>{escape(project['problem'])}</p>
          <h3>目标用户</h3>
          <ul class=\"bullet-list\">{audiences}</ul>
        </article>

        <article class=\"section-card\">
          <p class=\"eyebrow\">Signals</p>
          <h2>来自新闻的关键信号</h2>
          <ul class=\"bullet-list\">{signals}</ul>
        </article>
      </section>

      <section class=\"section-card\">
        <div class=\"section-heading\">
          <div>
            <p class=\"eyebrow\">MVP</p>
            <h2>这个原型包含什么</h2>
          </div>
          <p>{escape(project['mvp_thesis'])}</p>
        </div>
        <div class=\"card-grid\">{feature_cards}</div>
      </section>

      <section class=\"section-card\">
        <div class=\"section-heading\">
          <div>
            <p class=\"eyebrow\">Interactive demo</p>
            <h2>三种最先能打动市场的使用场景</h2>
          </div>
          <p>点击不同场景，查看从体验入口到北极星指标的 MVP 路线。</p>
        </div>
        {scenarios}
      </section>

      <section class=\"content-grid\">
        <article class=\"section-card\">
          <p class=\"eyebrow\">Stack</p>
          <h2>当前技术栈</h2>
          <ul class=\"bullet-list\">{stack}</ul>
        </article>
        <article class=\"section-card\">
          <p class=\"eyebrow\">Risks</p>
          <h2>主要风险</h2>
          <ul class=\"bullet-list\">{risks}</ul>
        </article>
      </section>

      <section class=\"section-card\">
        <p class=\"eyebrow\">Next steps</p>
        <h2>如果继续迭代，接下来做什么</h2>
        <ul class=\"bullet-list\">{next_steps}</ul>
      </section>
    </main>
    """
    return layout(
        f"{project['title']} · {SITE_TITLE}",
        body,
        project["tagline"],
        canonical=f"{SITE_URL}projects/{project['slug']}/",
    )


def build_home_page(projects: list[dict[str, Any]]) -> str:
    latest = projects[0]
    cards_html = []
    for project in projects:
        cards_html.append(
            f"""
            <article class=\"project-card\">
              <p class=\"eyebrow\">{escape(project['date'])} · {escape(project['category'])}</p>
              <h3>{escape(project['title'])}</h3>
              <p>{escape(project['tagline'])}</p>
              <div class=\"card-meta\">
                <span>潜力评分 {escape(str(project['potential_score']))}</span>
                <a href=\"/startup-mvp-daily/projects/{escape(project['slug'])}/\">查看 MVP →</a>
              </div>
            </article>
            """
        )

    body = f"""
    <main class=\"page-shell\">
      <section class=\"hero-card\">
        <p class=\"eyebrow\">Daily startup scouting → shipping</p>
        <h1>{escape(SITE_TITLE)}</h1>
        <p class=\"lede\">{escape(SITE_TAGLINE)}</p>
        <div class=\"hero-grid\">
          <article>
            <p class=\"label\">今天最新上线</p>
            <h2>{escape(latest['title'])}</h2>
            <p>{escape(latest['summary'])}</p>
            <a class=\"cta-button\" href=\"/startup-mvp-daily/projects/{escape(latest['slug'])}/\">进入 MVP</a>
          </article>
          <article>
            <p class=\"label\">工作流</p>
            <ul class=\"bullet-list\">
              <li>抓取 AI / 教育 / 科技 / 养老 / 商业等 Startup 新闻</li>
              <li>挑出最有创造力或增长潜力的一条</li>
              <li>沉淀为结构化项目 JSON</li>
              <li>自动编译静态站点并推送到 GitHub Pages</li>
            </ul>
          </article>
        </div>
      </section>

      <section class=\"section-card\">
        <div class=\"section-heading\">
          <div>
            <p class=\"eyebrow\">Archive</p>
            <h2>已发布的每日 MVP</h2>
          </div>
          <p>每一个项目都保留新闻出处、产品假设、MVP 功能和下一步路线。</p>
        </div>
        <div class=\"project-grid\">{''.join(cards_html)}</div>
      </section>
    </main>
    """
    return layout(SITE_TITLE, body, SITE_TAGLINE)


def main() -> None:
    projects = load_projects()
    if not projects:
        raise SystemExit("No project JSON files found under content/projects/")

    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    for project in projects:
        out_dir = PROJECTS_DIR / project["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(build_project_page(project), encoding="utf-8")

    (DOCS_DIR / "index.html").write_text(build_home_page(projects), encoding="utf-8")
    FEED_PATH.write_text(json.dumps(projects, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Built {len(projects)} project(s) into {DOCS_DIR}")


if __name__ == "__main__":
    main()
