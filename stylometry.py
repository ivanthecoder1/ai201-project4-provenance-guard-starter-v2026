"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics

# Window size for the moving-average type-token ratio.
TTR_WINDOW = 50

# Punctuation that shows up inside a sentence. `...` and `--` count once each.
MID_SENTENCE_PUNCTUATION = re.compile(r"\.\.\.|--|[,;:—–()\"“”]")

# (value that looks fully human, value that looks fully AI) for each measure.
SPREAD_RAMP = (0.65, 0.25)
TTR_RAMP = (0.70, 0.90)
PUNCT_RAMP = (0.10, 0.04)

# How much each measure counts inside the style signal. Spread separated the
# calibration samples best, punctuation worst.
WEIGHT_SPREAD = 0.50
WEIGHT_TTR = 0.35
WEIGHT_PUNCT = 0.15


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.

    Mine: coefficient of variation (stdev / mean) of words per sentence.
    0 = every sentence the same length. Higher = more varied = more human.
    Fewer than two sentences returns 0.0 here, and `style_signal` treats that
    case as "no evidence" rather than as perfectly even.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    return statistics.stdev(lengths) / statistics.mean(lengths)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words. ← TODO

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.

    Mine: the moving-average version. Plain unique/total on texts under
    TTR_WINDOW words; on longer texts, the average ratio over every window of
    TTR_WINDOW consecutive words, so a long piece isn't penalised for being long.
    """
    w = words(text)
    if not w:
        return 0.0
    if len(w) <= TTR_WINDOW:
        return len(set(w)) / len(w)
    windows = [w[i:i + TTR_WINDOW] for i in range(len(w) - TTR_WINDOW + 1)]
    return statistics.mean(len(set(win)) / TTR_WINDOW for win in windows)


def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length. ← TODO

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.

    Mine: marks inside sentences (commas, semicolons, colons, dashes,
    brackets, quotes, ellipses) per word. Full stops are left out — they mostly
    count sentences, which the spread measure already sees.
    """
    w = words(text)
    if not w:
        return 0.0
    return len(MID_SENTENCE_PUNCTUATION.findall(text)) / len(w)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.

    Mine: each measure goes onto 0–1 with a straight-line ramp between the
    value where it looks fully human (0) and fully AI (1), clamped at both
    ends, then a weighted average. The ramp ends come from calibration samples
    (see README, Signals and Scoring):

      spread   low = AI.  AI samples 0.19–0.34, human 0.44–0.70.
      ttr      HIGH = AI — the opposite of the hint above. AI samples used
               varied vocabulary (0.88–0.95); the human ones repeated
               themselves (0.73–0.76).
      punct    low = AI, weakly. Barely separated the samples, so it gets
               the smallest weight.

    Short text breaks two measures, so each counts as 0.5 (no evidence either
    way) when it has too little to go on: one sentence has no spread at all,
    and under TTR_WINDOW words nearly every word is unique, which would read
    as AI for any short post.
    """
    if len(sentences(text)) < 2:
        spread_ai = 0.5
    else:
        spread_ai = _ramp(sentence_length_spread(text), *SPREAD_RAMP)
    if len(words(text)) < TTR_WINDOW:
        ttr_ai = 0.5
    else:
        ttr_ai = _ramp(type_token_ratio(text), *TTR_RAMP)
    punct_ai = _ramp(punctuation_density(text), *PUNCT_RAMP)

    return (WEIGHT_SPREAD * spread_ai
            + WEIGHT_TTR * ttr_ai
            + WEIGHT_PUNCT * punct_ai)


def _ramp(value: float, human_at: float, ai_at: float) -> float:
    """0 at `human_at`, 1 at `ai_at`, a straight line between, clamped to 0–1."""
    position = (value - human_at) / (ai_at - human_at)
    return min(1.0, max(0.0, position))


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text):.4f}   (higher = more likely AI)")
