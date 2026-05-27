import argparse
import re


NORMALIZE = [
    (r"\bu\b", "you"),
    (r"\bur\b", "your"),
    (r"\br\b", "are"),
    (r"\bwanna\b", "want to"),
    (r"\bgonna\b", "going to"),
    (r"\bcant\b", "can't"),
    (r"\bdont\b", "don't"),
    (r"\bim\b", "I'm"),
    (r"\bi am\b", "I'm"),
    (r"\bwhat you doing\b", "what are you doing"),
    (r"\bwhy you doing\b", "why are you doing"),
    (r"\bhow you doing\b", "how are you doing"),
    (r"\bwhere you going\b", "where are you going"),
]

WORD_SWAPS = {
    "good": "acceptable",
    "great": "useful",
    "bad": "worthless",
    "terrible": "meaningless",
    "horrible": "useless",
    "sad": "cold",
    "happy": "calm",
    "scared": "unshaken",
    "afraid": "unshaken",
    "weak": "inferior",
    "strong": "superior",
    "better": "stronger",
    "fast": "unstoppable",
    "popular": "known",
    "famous": "known",
    "love": "respect",
    "like": "respect",
    "friend": "ally",
    "enemy": "target",
    "fight": "battle",
    "win": "surpass",
    "lose": "fall behind",
    "run": "move",
    "walk": "advance",
    "go": "move",
    "leave": "vanish",
    "remember": "never forget",
    "promise": "vow",
    "power": "Chaos power",
    "energy": "Chaos energy",
    "code": "script",
    "help": "aid",
    "want": "demand",
    "need": "require",
    "maybe": "perhaps",
    "really": "seriously",
    "very": "completely",
    "please": "",
    "yes": "fine",
    "no": "never",
    "ok": "fine",
    "okay": "fine",
}


def normalize_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)

    for pattern, replacement in NORMALIZE:
        text = re.sub(pattern, replacement, text, flags=re.I)

    return text.strip()


def clean_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    if not text:
        return ""

    text = text[0].upper() + text[1:]

    if not text.endswith((".", "?", "!")):
        text += "."

    text = re.sub(r"\bi\b", "I", text)
    text = re.sub(r"\bi'm\b", "I'm", text, flags=re.I)

    return text


def swap_words(text: str) -> str:
    tokens = re.findall(r"\w+|[^\w\s]", text)
    output = []

    for token in tokens:
        lower = token.lower()
        replacement = WORD_SWAPS.get(lower, token)

        if replacement:
            output.append(replacement)

    joined = ""

    for token in output:
        if re.match(r"[,.!?;:]", token):
            joined = joined.rstrip() + token
        else:
            joined += (" " if joined else "") + token

    return joined.strip()


def is_question(text: str) -> bool:
    return text.endswith("?") or bool(
        re.match(r"\s*(what|who|where|when|why|how|are|do|did|can|could|would|will|is|was)\b", text, re.I)
    )


def rewrite_question(text: str) -> str:
    t = text.lower()

    if "what are you doing" in t:
        return "What are you trying to accomplish?"
    if "what do you want" in t:
        return "What are you demanding from me?"
    if "where are you going" in t:
        return "Where are you planning to move next?"
    if "why are you doing" in t:
        return "Why are you wasting effort on that?"
    if "how are you" in t or "how do you feel" in t:
        return "Why does that matter right now?"
    if "can you help" in t:
        return "What exactly do you need done?"

    swapped = swap_words(text)
    return clean_sentence(swapped)


def rewrite_statement(text: str) -> str:
    t = text.lower()

    if re.search(r"\bi need to be popular\b", t):
        return "I need to become impossible to ignore."

    if re.search(r"\bi need to be known\b", t):
        return "I need my name to become impossible to ignore."

    if re.search(r"\bi need to code\b", t):
        return "I need to write something strong enough to matter."

    if re.search(r"\bi can't code\b|\bi cannot code\b", t):
        return "I am not done learning how to code."

    if re.search(r"\bi want power\b", t):
        return "I want enough power to force the world to notice."

    if re.search(r"\bi want to win\b", t):
        return "I want to win so completely that no one can dismiss me."

    if re.search(r"\bi hate this\b", t):
        return "I hate this, so I am going to turn that anger into motion."

    if re.search(r"\bno one sees me\b|\bno one can see me\b", t):
        return "No one sees me yet, so I will become impossible to overlook."

    if re.search(r"\bi am weak\b|\bi'm weak\b", t):
        return "I am not staying weak."

    swapped = swap_words(text)
    return clean_sentence(swapped)


def translate_to_shadow(text: str) -> str:
    text = normalize_text(text)

    if not text:
        return "Say something worth translating."

    if is_question(text):
        return clean_sentence(rewrite_question(text))

    return clean_sentence(rewrite_statement(text))


def main() -> None:
    parser = argparse.ArgumentParser(description="Rewrite a sentence into a sharper Shadow-style sentence.")
    parser.add_argument("sentence", nargs="*", help="Sentence to rewrite")
    args = parser.parse_args()

    if args.sentence:
        sentence = " ".join(args.sentence)
    else:
        sentence = input("Enter text: ")

    print(translate_to_shadow(sentence))


if __name__ == "__main__":
    main()