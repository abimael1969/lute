"""
AI autofill for reader term forms.
"""

import html
import json
import re
import requests


class TermAutofillClient:
    "OpenAI-compatible client for term translation suggestions."

    def __init__(self, config):
        self.config = config

    def suggest(self, language_name, term_text, sentence_context="", book_title=""):
        "Return autofill suggestion data."
        empty = {
            "translation": "",
            "parents": [],
            "confidence": "low",
            "provider_error": None,
        }
        if not self.config.ai_autofill_enabled:
            return {**empty, "provider_error": "AI autofill disabled"}
        if self.config.ai_autofill_api_key.strip() == "":
            return {**empty, "provider_error": "AI autofill API key missing"}
        if term_text.strip() == "":
            return {**empty, "provider_error": "No term text provided"}

        payload = {
            "model": self.config.ai_autofill_model,
            "messages": self._messages(
                language_name,
                term_text,
                sentence_context,
                book_title,
            ),
            "temperature": 0.1,
            "max_tokens": 160,
        }
        headers = {
            "Authorization": f"Bearer {self.config.ai_autofill_api_key}",
            "Content-Type": "application/json",
            "X-Title": "Lute term autofill",
        }
        try:
            response = requests.post(
                f"{self.config.ai_autofill_base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=20,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            suggestion = self._parse_content(content)
            if not self.config.ai_autofill_fill_parents:
                suggestion["parents"] = []
            return suggestion
        except Exception as e:  # pylint: disable=broad-exception-caught
            return {**empty, "provider_error": str(e)}

    def _messages(self, language_name, term_text, sentence_context, book_title):
        "Build strict JSON prompt messages."
        clean_context = _plain_text(sentence_context)
        system_prompt = """
You fill language-learning term form fields.
Return only valid JSON with keys translation, parents, confidence.
translation: brief Spanish translation of term_text using context.
parents: array with the source-language lemma/base form only if it is clear; otherwise [].
confidence: one of low, medium, high.
Do not explain. Do not include markdown. Do not add examples. Do not invent.
""".strip()
        user_prompt = {
            "source_language": language_name,
            "target_language": self.config.ai_autofill_target_lang,
            "term_text": term_text,
            "sentence_context": clean_context,
            "book_title": book_title,
        }
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=False)},
        ]

    def _parse_content(self, content):
        "Parse model output, accepting raw JSON or fenced JSON."
        data = json.loads(_extract_json_object(content))
        translation = str(data.get("translation") or "").strip()
        parents = data.get("parents") or []
        if not isinstance(parents, list):
            parents = []
        parents = [str(p).strip() for p in parents if str(p).strip()]
        confidence = data.get("confidence", "low")
        if confidence not in ("low", "medium", "high"):
            confidence = "low"
        return {
            "translation": translation,
            "parents": parents,
            "confidence": confidence,
            "provider_error": None,
        }


def _plain_text(value):
    "Convert hidden sentence HTML to prompt-safe plain text."
    text = re.sub(r"<[^>]+>", "", value or "")
    return html.unescape(text).replace("\u200b", "").strip()


def _extract_json_object(value):
    "Extract a JSON object from a model response."
    text = (value or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"```$", "", text).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("AI response did not contain a JSON object")
    return text[start : end + 1]
