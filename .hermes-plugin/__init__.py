import os
import re
from pathlib import Path

BOOTSTRAP_MARKER = "superpowers:using-superpowers bootstrap for hermes"


def _skills_dir() -> str:
    """Locate the stock skills/ tree for either supported install layout."""
    here = os.path.dirname(os.path.realpath(__file__))
    candidates = (
        os.path.realpath(os.path.join(here, "..", "skills")),
        os.path.realpath(os.path.join(here, "skills")),
    )
    for cand in candidates:
        if os.path.isfile(os.path.join(cand, "using-superpowers", "SKILL.md")):
            return cand
    raise RuntimeError(
        "superpowers 插件：找不到 skills/ 目录 "
        f"（已检查 {candidates}）。请使用 "
        "`hermes plugins install AreChen/superpowers-zh` 重新安装。"
    )


def _strip_frontmatter(content: str) -> str:
    match = re.match(r"^---\n[\s\S]*?\n---\n([\s\S]*)$", content)
    return (match.group(1) if match else content).strip()


def _frontmatter_value(content: str, key: str) -> str:
    """Return a flat ``key: value`` scalar from a SKILL.md frontmatter block.

    Hermes reads a skill's description from ``register_skill``'s ``description``
    argument, which defaults to "" — registering only the path left every stock
    skill with a blank description in the skill catalogue, so the model had
    nothing to select on. Stock frontmatter is a flat block of single-line
    scalars, so a line scan covers it without a YAML dependency.
    """
    match = re.match(r"^---\n([\s\S]*?)\n---\n", content)
    if not match:
        return ""
    for line in match.group(1).splitlines():
        name, sep, value = line.partition(":")
        if sep and name.strip() == key:
            return value.strip().strip("\"'")
    return ""


def _build_bootstrap(skills_dir: str) -> str:
    with open(
        os.path.join(skills_dir, "using-superpowers", "SKILL.md"),
        encoding="utf-8",
    ) as f:
        body = _strip_frontmatter(f.read())

    tools_path = os.path.join(
        skills_dir, "using-superpowers", "references", "hermes-tools.md"
    )
    with open(tools_path, encoding="utf-8") as f:
        tool_mapping = f.read().strip()

    return (
        f"<EXTREMELY_IMPORTANT>\n"
        f"{BOOTSTRAP_MARKER}\n\n"
        f"你拥有 Superpowers。\n\n"
        f"下面包含 using-superpowers 技能内容，并且已经在本次 Hermes 会话中加载。"
        f"现在遵循它。不要再次尝试加载 using-superpowers。\n\n"
        f"{body}\n\n"
        f"## 在 Hermes 上加载 Superpowers 技能\n\n"
        f"Superpowers 技能已注册到 Hermes 的原生技能加载器：使用 "
        f'`skill_view("superpowers:skill-name")` 调用技能（例如 '
        f'`skill_view("superpowers:brainstorming")`）。如果命名空间查找返回 '
        f"'not found'，请直接读取技能文件：\n"
        f'`read_file("{skills_dir}/skill-name/SKILL.md")`\n\n'
        f"Superpowers 技能目录：`{skills_dir}`\n\n"
        f"{tool_mapping}\n"
        f"</EXTREMELY_IMPORTANT>"
    )


def register(ctx):
    skills_dir = _skills_dir()
    bootstrap = _build_bootstrap(skills_dir)

    for name in sorted(os.listdir(skills_dir)):
        skill_md = os.path.join(skills_dir, name, "SKILL.md")
        if os.path.isfile(skill_md):
            with open(skill_md, encoding="utf-8") as f:
                description = _frontmatter_value(f.read(), "description")
            ctx.register_skill(name, Path(skill_md), description=description)

    def pre_llm_call(
        session_id=None,
        user_message=None,
        conversation_history=None,
        is_first_turn=None,
        model=None,
        platform=None,
        **kwargs,
    ):
        if is_first_turn:
            return {"context": bootstrap}
        return None

    ctx.register_hook("pre_llm_call", pre_llm_call)
