#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""expression_dna.py — 计算表达 DNA 的 6 个机读指标(优化项 #4)。
中英混排都适用:CJK 按字计 token,拉丁按词计 token。
用法:  python expression_dna.py <textfile|->
输出:  {avg_sentence_len, interrogative_ratio, analogy_per_1k, first_person_ratio,
         certainty_ratio, transition_per_1k, n_sentences, n_tokens, n_chars}
"""
import sys, re, json, argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CJK = r"一-鿿㐀-䶿"
SENT_SPLIT = re.compile(r"[。！？!?\n]+|\.(?=\s|$)")
TOKEN = re.compile(rf"[{CJK}]|[A-Za-z0-9]+")

ANALOGY = ["像", "如同", "好比", "就像", "仿佛", "好像", "类似", "犹如",
           "like a", "as if", "such as", "analogy", "metaphor"]
FIRST_PERSON = ["我们", "我", "咱", r"\bI\b", r"\bme\b", r"\bmy\b", r"\bwe\b", r"\bus\b", r"\bour\b"]
CERTAIN = ["一定", "必然", "肯定", "绝对", "必须", "毫无疑问", "always", "never",
           "definitely", "certainly", "must", "undoubtedly"]
HEDGE = ["可能", "也许", "或许", "大概", "似乎", "估计", "兴许", "maybe", "perhaps",
         "might", "probably", "possibly", "i think", "i guess", "seems"]
TRANSITION = ["但是", "然而", "因此", "所以", "不过", "而且", "因为", "于是", "其实",
              "however", "but ", "therefore", "because", "moreover", "thus", "so "]


def count_any(text_low: str, terms) -> int:
    n = 0
    for t in terms:
        if t.startswith("\\b") or t.endswith("\\b") or "\\b" in t:
            n += len(re.findall(t, text_low))
        else:
            n += text_low.count(t.lower())
    return n


def dna(text: str) -> dict:
    chars = len(re.findall(rf"[{CJK}A-Za-z0-9]", text))
    sents = [s for s in SENT_SPLIT.split(text) if s.strip()]
    n_sent = len(sents) or 1
    tokens = TOKEN.findall(text)
    n_tok = len(tokens) or 1
    low = text.lower()

    interro = sum(1 for s in sents if re.search(r"[?？]", s) or re.search(r"(吗|呢|么)\s*[?？]?$", s.strip()))
    per1k = lambda c: round(c / chars * 1000, 2) if chars else 0.0
    certain_c = count_any(low, CERTAIN)
    hedge_c = count_any(low, HEDGE)

    return {
        "avg_sentence_len": round(n_tok / n_sent, 2),
        "interrogative_ratio": round(interro / n_sent, 3),
        "analogy_per_1k": per1k(count_any(low, ANALOGY)),
        "first_person_ratio": round(count_any(low, FIRST_PERSON) / n_tok, 3),
        "certainty_ratio": round(certain_c / (certain_c + hedge_c), 3) if (certain_c + hedge_c) else None,
        "transition_per_1k": per1k(count_any(low, TRANSITION)),
        "n_sentences": n_sent, "n_tokens": n_tok, "n_chars": chars,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile", help="文本文件路径,或 - 读 stdin")
    args = ap.parse_args()
    text = sys.stdin.read() if args.infile == "-" else Path(args.infile).read_text(encoding="utf-8", errors="replace")
    print(json.dumps(dna(text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
