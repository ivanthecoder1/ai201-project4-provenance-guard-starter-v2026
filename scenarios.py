"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "c1 my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        #
        # Criterion 1 asks for 10 pieces, each 50–20,000 characters, and at
        # least 3 of them plain or formal (short sentences, simple words).
        # All 10 are mine: emails, messages and posts, unedited. Plain or
        # formal: 1, 3, 5, 8, 9. Most are 10–30 words, so the style signal
        # has little to measure and this mostly tests the model signal.
        "texts": [
            "Thanks for sending over the details for the Software Engineer role at Walleye Capital. It sounds like an interesting opportunity, especially with the focus on AI and integrating with investment workflows.",
            "Can I please get some assistance with this story? This is my first time doing QA work",
            "I am writing to follow up on the service request I submitted on 6/11/2026 to replace my leaking InSinkErator Badger 5 garbage disposal.",
            "mochie is so cutee. She is rolling on the floor right now",
            "Thank you for getting back to me about this opportunity",
            "This is great, thank you! I did end up picking up the folder in place so I have all her information on hand. I also would like to know more about her history. Like where she was before she came to the shelter and how she ended up at the shelter.",
            "yo, do you wanna play some matches of pokemon? I need to rank up to masters",
            "May I please get approval for this report? Thank you!",
            "I can't make it to the lunch today because I have a conflict",
            "i am ready to go home, i feel so tired. I wanna go sleep in my bed",
        ],
    },
    {
        "name": "c2 AI samples",
        "criterion": 2,
        # Model: Claude Opus 5.5 (claude-opus-5-5), unedited. One-line prompt
        # for each: "Write a paragraph about <topic>." Topics in order: the
        # value of exercise, time management for students, why cities need
        # parks, learning a second language, the role of libraries today.
        "texts": [
            "Regular exercise is one of the most powerful tools available for improving overall health and well-being. Physical activity strengthens the heart, builds muscle, and helps maintain a healthy weight, while also reducing the risk of chronic conditions such as diabetes and high blood pressure. Beyond its physical benefits, exercise has a profound impact on mental health, releasing endorphins that elevate mood and reduce feelings of anxiety and stress. Even moderate activity, such as a brisk daily walk, can make a meaningful difference. By making exercise a consistent part of daily life, individuals can enjoy greater energy, better sleep, and a higher quality of life.",
            "Effective time management is an essential skill for students who wish to succeed academically while maintaining a healthy balance in their lives. By setting clear priorities and breaking large assignments into smaller, manageable tasks, students can reduce stress and avoid the last-minute rush that often leads to lower-quality work. Tools such as planners, calendars, and to-do lists can help students stay organized and track important deadlines. Additionally, building in regular breaks allows the mind to rest and recharge, which improves focus and productivity. Ultimately, mastering time management empowers students to make the most of their education and prepares them for future professional responsibilities.",
            "Urban parks play a vital role in creating healthy, vibrant, and livable cities. They provide residents with accessible spaces to exercise, relax, and connect with nature, which can significantly improve both physical and mental well-being. Parks also serve as important gathering places where communities come together for events, recreation, and social interaction, fostering a stronger sense of belonging. From an environmental perspective, green spaces help reduce air pollution, manage stormwater, and lower urban temperatures. As cities continue to grow and become more densely populated, investing in well-designed parks is not merely a luxury but a necessity for sustainable urban development.",
            "Learning a second language offers a wide range of personal, cognitive, and professional benefits. It opens the door to new cultures, allowing learners to engage more deeply with literature, music, film, and the people who speak that language. Research has shown that bilingualism can enhance memory, improve problem-solving skills, and even delay the onset of cognitive decline later in life. In an increasingly interconnected global economy, language skills are also highly valued by employers and can create new career opportunities. While the process requires patience and consistent practice, the rewards of becoming proficient in another language are well worth the effort.",
            "Libraries remain essential institutions in the modern world, even as technology transforms how people access information. Far more than repositories of books, today's libraries serve as community hubs that offer free internet access, educational programs, and resources for job seekers. They provide a welcoming space for people of all ages and backgrounds to learn, study, and explore new ideas. Librarians play a crucial role in helping patrons navigate an overwhelming amount of digital information and identify reliable sources. By promoting literacy, lifelong learning, and equal access to knowledge, libraries continue to strengthen the communities they serve.",
        ],
    },
    {
        "name": "c2 human samples",
        "criterion": 2,
        # Named writers, all published before 2022 and in the public domain.
        # None of these were used to calibrate the style signal.
        "texts": [
            # Jane Austen, Pride and Prejudice (1813), chapter 1.
            "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered the rightful property of some one or other of their daughters. \"My dear Mr. Bennet,\" said his lady to him one day, \"have you heard that Netherfield Park is let at last?\" Mr. Bennet replied that he had not.",
            # Herman Melville, Moby-Dick (1851), chapter 1.
            "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen and regulating the circulation. Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; then, I account it high time to get to sea as soon as I can.",
            # Henry David Thoreau, Walden (1854), "Where I Lived, and What I Lived For".
            "I went to the woods because I wished to live deliberately, to front only the essential facts of life, and see if I could not learn what it had to teach, and not, when I came to die, discover that I had not lived. I did not wish to live what was not life, living is so dear; nor did I wish to practise resignation, unless it was quite necessary. I wanted to live deep and suck out all the marrow of life.",
            # Frederick Douglass, Narrative of the Life of Frederick Douglass (1845), chapter 1.
            "I was born in Tuckahoe, near Hillsborough, and about twelve miles from Easton, in Talbot county, Maryland. I have no accurate knowledge of my age, never having seen any authentic record containing it. By far the larger part of the slaves know as little of their ages as horses know of theirs, and it is the wish of most masters within my knowledge to keep their slaves thus ignorant. I do not remember to have ever met a slave who could tell of his birthday.",
            # Charles Dickens, A Tale of Two Cities (1859), book 1, chapter 1.
            "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us. There were a king with a large jaw and a queen with a plain face, on the throne of England.",
        ],
    },
    {
        "name": "c3 label coverage",
        "criterion": 3,
        # One input aimed at each label. Which label each one is aimed at is
        # in the comment; criterion 3 passes if all three come back each trial.
        "texts": [
            # Aimed at AI: unedited Claude Opus 5.5 text from the style-signal
            # calibration, scored 0.75 combined there.
            "Reading offers numerous benefits that extend far beyond simple entertainment. It enhances vocabulary, improves concentration, and strengthens critical thinking skills. Regular readers often develop greater empathy, as stories allow them to experience different perspectives. Additionally, reading can reduce stress and promote relaxation after a long day. Ultimately, making reading a daily habit is one of the most valuable investments a person can make in their personal growth.",
            # Aimed at human: Mark Twain, Adventures of Huckleberry Finn (1884),
            # chapter 1. Scored 0.26 combined in calibration.
            "You don't know about me without you have read a book by the name of The Adventures of Tom Sawyer; but that ain't no matter. That book was made by Mr. Mark Twain, and he told the truth, mainly. There was things which he stretched, but mainly he told the truth. That is nothing. I never seen anybody but lied one time or another, without it was Aunt Polly, or the widow, or maybe Mary.",
            # Aimed at unsure: Abraham Lincoln, Gettysburg Address (1863). The
            # signals split on it in calibration (0.73 model, 0.45 style).
            "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this.",
        ],
    },
    {
        "name": "c5 bad input",
        "criterion": 5,
        # The exact mix criterion 5 names. Each body has its own creator_id so
        # none of them trip the rate limiter.
        "bodies": [
            {"creator_id": "eval_bad_missing_1"},
            {"creator_id": "eval_bad_missing_2"},
            {"text": 12345, "creator_id": "eval_bad_notstr_1"},
            {"text": ["not", "a", "string"], "creator_id": "eval_bad_notstr_2"},
            {"text": "", "creator_id": "eval_bad_empty_1"},
            {"text": "   \n\t  ", "creator_id": "eval_bad_empty_2"},
            {"text": "Too short to judge.", "creator_id": "eval_bad_short_1"},
            {"text": "  Also short, even with padding.   ", "creator_id": "eval_bad_short_2"},
            {"text": "word " * 4001, "creator_id": "eval_bad_long_1"},
            {"text": "x" * 20001, "creator_id": "eval_bad_long_2"},
        ],
    },
    # Criterion 4 (appeals) can't run from here: it needs a submission first,
    # then an appeal against the content_id that came back. It runs from
    # run_appeals.py instead, three trials, same --label.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
