"""Translate clean article excerpts. Failures raise; they are never article content."""
import os
import re
import time

_PROPER_NOUNS = ["Constitutional AI", "Anthropic", "ChatGPT", "Claude", "Sonnet", "Haiku", "Opus", "GPT-4", "GPT-3", "OpenAI", "Gemini", "RLHF", "LLM", "API"]


def _protect_nouns(text):
    mapping = {}
    for i, noun in enumerate(_PROPER_NOUNS):
        if noun in text:
            token = f"{{{{{i}}}}}"
            mapping[token] = noun
            text = text.replace(noun, token)
    return text, mapping


def _restore_nouns(text, mapping):
    for token, noun in mapping.items():
        number = re.search(r"\d+", token)[0]
        text = re.sub(r"\{\s*\{\s*" + number + r"\s*\}\s*\}", lambda _: noun, text)
    return text


def valid_translation(text):
    return isinstance(text, str) and len(text.strip()) > 5 and bool(re.search(r"[\u4e00-\u9fff]", text)) and not re.search(r"\{\s*\{|\[.*(?:错误|失败|无法获取|不支持)|NOUN\d+", text)


def excerpt(content, limit=800):
    """Use whole sentences within the budget; never cut a sentence mid-word."""
    content = re.sub(r"\s+", " ", content).strip()
    sentences = re.split(r"(?<=[.!?。！？])\s+", content)
    chosen = []
    for sentence in sentences:
        if len(" ".join(chosen + [sentence])) > limit:
            break
        chosen.append(sentence)
    if not chosen:
        raise ValueError("no complete sentence within excerpt budget")
    return " ".join(chosen)


def _aliyun(text):
    from alibabacloud_alimt20181012.client import Client
    from alibabacloud_alimt20181012 import models
    from alibabacloud_tea_openapi.models import Config
    key, secret = os.getenv("ALIYUN_ACCESS_KEY_ID"), os.getenv("ALIYUN_ACCESS_KEY_SECRET")
    if not key or not secret:
        raise RuntimeError("Aliyun translation credentials are missing")
    client = Client(Config(access_key_id=key, access_key_secret=secret, endpoint="mt.aliyuncs.com", read_timeout=20000, connect_timeout=10000))
    protected, mapping = _protect_nouns(text)
    request = models.TranslateGeneralRequest(format_type="text", source_language="en", target_language="zh", source_text=protected, scene="general")
    response = client.translate_general(request)
    if str(response.body.code) != "200":
        raise RuntimeError(f"Aliyun translation response code {response.body.code}")
    result = _restore_nouns(response.body.data.translated, mapping)
    if re.search(r"\{\s*\{|NOUN\d+", result):
        raise ValueError("unrestored proper-noun token")
    return result.strip()


def _once(text, engine, mode, model):
    if engine == "aliyun":
        return _aliyun(text)
    if engine == "claude":
        import anthropic
        prompt = "请用3-5句简体中文总结以下文章，保留技术术语。" if mode == "summary" else "请将以下内容翻译为简体中文。"
        response = anthropic.Anthropic().messages.create(model=model, max_tokens=1600, messages=[{"role": "user", "content": prompt + "\n\n" + text}])
        return "\n".join(b.text for b in response.content if b.type == "text").strip()
    if engine == "deepl":
        import deepl
        return deepl.Translator(os.environ["DEEPL_API_KEY"]).translate_text(text, target_lang="ZH").text
    raise ValueError(f"unsupported translation engine: {engine}")


def translate(title, content, engine="aliyun", mode="summary", claude_model="claude-haiku-4-5-20251001"):
    # Title and body are separate calls; a translated title cannot masquerade as an excerpt.
    text = excerpt(content) if content and mode == "summary" else (content or title).strip()
    for attempt in range(3):
        try:
            result = _once(text, engine, mode, claude_model)
            if not result or (content and not valid_translation(result)):
                raise ValueError("invalid translation result")
            return result
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
