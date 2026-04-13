# 功能：将英文文章内容翻译为中文摘要
# 输入：文章标题（str）+ 正文文本（str）+ 翻译引擎配置
# 输出：中文摘要字符串
# 运行方式：被 main.py 调用，不单独运行
# 依赖：anthropic（claude 引擎）/ alibabacloud-alimt20181012（aliyun 引擎）
# 项目作用：翻译层，支持 aliyun / claude / deepl 三种引擎可切换
# 最后修改：2026-04-10

import os


# 专有名词保护：翻译前替换为占位符，翻译后还原
_PROPER_NOUNS = [
    "Claude", "Anthropic", "Sonnet", "Haiku", "Opus",
    "ChatGPT", "GPT-4", "GPT-3", "OpenAI", "Gemini",
    "Constitutional AI", "RLHF", "LLM", "API",
]


def _protect_nouns(text: str) -> tuple[str, dict]:
    """将专有名词替换为占位符（花括号格式，机器翻译通常原样保留）"""
    mapping = {}
    for i, noun in enumerate(_PROPER_NOUNS):
        placeholder = f"{{{{{i}}}}}"  # 例如 {{0}}, {{1}} ...
        if noun in text:
            mapping[placeholder] = noun
            text = text.replace(noun, placeholder)
    return text, mapping


def _restore_nouns(text: str, mapping: dict) -> str:
    """还原占位符为原始专有名词（完全匹配）"""
    for placeholder, noun in mapping.items():
        text = text.replace(placeholder, noun)
    return text


def translate(title: str, content: str, engine: str, mode: str, claude_model: str) -> str:
    """
    翻译文章标题和内容为中文。

    mode="summary": 生成 3-5 句中文摘要（省 token/字符）
    mode="full":    全文翻译（消耗更多资源）

    engine: "aliyun" | "claude" | "deepl"
    """
    # 截取正文前 3000 字符避免超出 API 限制
    content_preview = content[:3000] if content else ""

    if engine == "claude":
        return _translate_with_claude(title, content_preview, mode, claude_model)
    elif engine == "aliyun":
        return _translate_with_aliyun(title, content_preview, mode)
    elif engine == "deepl":
        return _translate_with_deepl(title, content_preview, mode)
    else:
        return f"[不支持的翻译引擎: {engine}]"


def _translate_with_claude(title: str, content: str, mode: str, model: str) -> str:
    """使用 Claude API 生成中文摘要"""
    try:
        import anthropic
    except ImportError:
        return "[错误：未安装 anthropic 包，请运行 pip install anthropic]"

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "[错误：未设置 ANTHROPIC_API_KEY 环境变量]"

    client = anthropic.Anthropic(api_key=api_key)

    if mode == "summary":
        prompt = (
            f"请用3-5句简体中文总结以下英文文章的核心内容，突出主要观点和技术亮点。\n\n"
            f"标题：{title}\n\n正文：{content}"
        )
    else:
        prompt = (
            f"请将以下英文文章翻译成通顺的简体中文，保留技术术语的英文原文（括号内附中文）。\n\n"
            f"标题：{title}\n\n正文：{content}"
        )

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()


def _translate_with_aliyun(title: str, content: str, mode: str) -> str:
    """使用阿里云机器翻译 API"""
    try:
        from alibabacloud_alimt20181012.client import Client
        from alibabacloud_alimt20181012 import models as alimt_models
        from alibabacloud_tea_openapi import models as open_api_models
    except ImportError:
        return "[错误：未安装阿里云翻译 SDK，请运行 pip install alibabacloud-alimt20181012]"

    access_key_id = os.environ.get("ALIYUN_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIYUN_ACCESS_KEY_SECRET")
    if not access_key_id or not access_key_secret:
        return "[错误：未设置 ALIYUN_ACCESS_KEY_ID 或 ALIYUN_ACCESS_KEY_SECRET 环境变量]"

    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint="mt.aliyuncs.com"
    )
    client = Client(config)

    if mode == "summary":
        # summary 模式：只翻译标题 + 正文前 500 字符
        text_to_translate = f"{title}\n\n{content[:500]}"
    else:
        text_to_translate = f"{title}\n\n{content}"

    # 保护专有名词
    protected_text, mapping = _protect_nouns(text_to_translate)

    request = alimt_models.TranslateGeneralRequest(
        format_type="text",
        source_language="en",
        target_language="zh",
        source_text=protected_text,
        scene="general"
    )

    try:
        response = client.translate_general(request)
        translated = response.body.data.translated
        # 还原专有名词
        translated = _restore_nouns(translated, mapping)
        if mode == "summary":
            return f"【机器翻译摘要】\n{translated}"
        return translated
    except Exception as e:
        return f"[阿里云翻译失败: {e}]"


def _translate_with_deepl(title: str, content: str, mode: str) -> str:
    """使用 DeepL API 翻译（需安装 deepl 包）"""
    try:
        import deepl
    except ImportError:
        return "[错误：未安装 deepl 包，请运行 pip install deepl]"

    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        return "[错误：未设置 DEEPL_API_KEY 环境变量]"

    translator = deepl.Translator(api_key)

    text = f"{title}\n\n{content[:500] if mode == 'summary' else content}"
    try:
        result = translator.translate_text(text, target_lang="ZH")
        return result.text
    except Exception as e:
        return f"[DeepL 翻译失败: {e}]"
