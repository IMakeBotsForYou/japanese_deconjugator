import re
import ujson as json

from rules import (
    a_,
    i_,
    u_,
    e_,
    o_,
    a_regex,
    i_regex,
    u_regex,
    e_regex,
    o_regex,
    a_conj,
    a_conj_ichidan,
    i_conj,
    u_conj,
    e_conj,
    e_conj_ichidan,
    o_conj,
    o_conj_ichidan,
    i_adj_conjugations,
    na_adj_conjugations,
    te_deconjugations,
    past_deconjugations,
    suru_conjugations,
    kuru_conjugations,
    masu_conjugations,
)
from tree import Tree

jisho = {}
with open("jisho.json", "r", encoding="utf-8") as f:
    jisho = json.load(f)

word = "なっちゃわない"

# Godan endings grouped by vowel row
godan_deconjugatable_a = re.compile(rf"[{a_regex}]({'|'.join(a_conj.keys())})$")
godan_deconjugatable_i = re.compile(rf"[{i_regex}]({'|'.join(i_conj.keys())})$")
godan_deconjugatable_u = re.compile(rf"[{u_regex}]({'|'.join(u_conj.keys())})$")
godan_deconjugatable_e = re.compile(rf"[{e_regex}]({'|'.join(e_conj.keys())})$")
godan_deconjugatable_o = re.compile(rf"[{o_regex}]({'|'.join(o_conj.keys())})$")


def godan_deconjugatable(word):
    return [
        godan_deconjugatable_a.search(word),
        godan_deconjugatable_i.search(word),
        godan_deconjugatable_u.search(word),
        godan_deconjugatable_e.search(word),
        godan_deconjugatable_o.search(word),
    ]


# Ichidan: must end in i/e-row + one of the valid suffixes
ichidan_deconjugatable_a = re.compile(
    rf"[{e_regex}{i_regex}]({'|'.join(a_conj_ichidan.keys())})$"
)
ichidan_deconjugatable_i = re.compile(
    rf"[{e_regex}{i_regex}]({'|'.join(i_conj.keys())})$"
)
ichidan_deconjugatable_u = re.compile(
    rf"[{e_regex}{i_regex}]({'|'.join(u_conj.keys())})$"
)
ichidan_deconjugatable_e = re.compile(
    rf"[{e_regex}{i_regex}]({'|'.join(e_conj_ichidan.keys())})$"
)
ichidan_deconjugatable_o = re.compile(
    rf"[{e_regex}{i_regex}]({'|'.join(o_conj_ichidan.keys())})$"
)


# Ichidan endings grouped by vowel row
def ichidan_deconjugatable(word):
    return [
        ichidan_deconjugatable_a.search(word),
        ichidan_deconjugatable_i.search(word),
        ichidan_deconjugatable_u.search(word),
        ichidan_deconjugatable_e.search(word),
        ichidan_deconjugatable_o.search(word),
    ]


adj_keys = list(i_adj_conjugations.keys()) + list(na_adj_conjugations.keys())

suru_deconjugatable = re.compile(rf"(?:{'|'.join(suru_conjugations.keys())})$")

kuru_deconjugatable = re.compile(rf"(?:{'|'.join(kuru_conjugations.keys())})$")

masu_deconjugatable = re.compile(rf"(?:{'|'.join(masu_conjugations.keys())})$")

past_conjugatable = re.compile(rf"(?:{'|'.join(past_deconjugations.keys())})$")

te_conjugatable = re.compile(rf"(?:{'|'.join(te_deconjugations.keys())})$")


# shared ichidan replacement
def ichidan_replace(w, i, c):
    return w[: i + 1] + "る"


def handle_wanai(w, i, c):
    if c == "わ" and w.endswith("ない"):
        return w[:i] + "う"
    else:
        return w


# w → the full word being checked.

# c → the changed_letter, i.e. the kana at the changed_index (the about to be swapped from e.g. あ→う, い→う, etc.).

# i → the changed_index, i.e. the position of that letter in w.

# t → previous conjugation type

rules = [
    # --- Godan ---
    dict(
        match=lambda g: g[0],
        table=a_conj,
        u_set=u_,
        source_set=a_,
        conj_type="5a",
        extra=lambda w, c, i, t: c in a_,
        replace=handle_wanai,  # Exception わない→う not ワ行のウ段 (doesn't exist)
    ),
    dict(
        match=lambda g: g[1],
        table=i_conj,
        u_set=u_,
        source_set=i_,
        conj_type="5i",
        extra=lambda w, c, i, t: c in i_ and not (t and t.startswith("adj")),
    ),
    dict(
        match=lambda g: g[2],
        table=u_conj,
        u_set=u_,
        source_set=u_,
        conj_type="5u",
        extra=lambda w, c, i, t: c in u_,
    ),
    dict(
        match=lambda g: g[3],
        table=e_conj,
        u_set=u_,
        source_set=e_,
        conj_type="5e",
        extra=lambda w, c, i, t: c in e_
        and not (c == "れ" and w[i - 1] in ["く", "す"]),
    ),
    dict(
        match=lambda g: g[4],
        table=o_conj,
        u_set=u_,
        source_set=o_,
        conj_type="5o",
        extra=lambda w, c, i, t: c in o_,
    ),
    # --- Ichidan ---
    dict(
        match=lambda g: g[0],
        table=a_conj_ichidan,
        u_set=u_,
        source_set=i_,
        conj_type="1a",
        extra=lambda w, c, i, t: c in i_ or c in e_,
        replace=ichidan_replace,
    ),
    dict(
        match=lambda g: g[1],
        table=i_conj,
        u_set=u_,
        source_set=i_,
        conj_type="1i",
        extra=lambda w, c, i, t: (c in i_ or c in e_)
        and not (t and t.startswith("adj")),
        replace=ichidan_replace,
    ),
    dict(
        match=lambda g: g[2],
        table=u_conj,
        u_set=u_,
        source_set=i_,
        conj_type="1u",
        extra=lambda w, c, i, t: c in i_ or c in e_,
        replace=ichidan_replace,
    ),
    dict(
        match=lambda g: g[3],
        table=e_conj_ichidan,
        u_set=u_,
        source_set=i_,
        conj_type="1e",
        extra=lambda w, c, i, t: (c in i_ or c in e_)
        and not (t and t.startswith("adj")),
        replace=ichidan_replace,
    ),
    dict(
        match=lambda g: g[4],
        table=o_conj_ichidan,
        u_set=u_,
        source_set=i_,
        conj_type="1o",
        extra=lambda w, c, i, t: c in i_ or c in e_,
        replace=ichidan_replace,
    ),
]


def te_deconjugatable(word):
    return te_conjugatable.search(word)


def past_deconjugatable(word):
    return past_conjugatable.search(word)


def adj_deconjugatable(word):
    return word[-1] in [form[-1] for form in adj_keys]


def deconjugate_te(word):
    if not te_deconjugatable(word):
        return []

    results = []
    for key, data in te_deconjugations.items():
        # (values, name)
        options = data["return-options"]
        name = data["name"]
        conj_type = data["type"]

        if word.endswith(key):
            # Special case: avoid false positives for "て"
            if key == "て" and word[-2] not in i_ + e_:
                continue

            for option in options:
                new_word = word[: -len(key)] + option
                results.append((new_word, name, conj_type))

    return list(set(results))


def deconjugate_past(word):
    if not past_deconjugatable(word):
        return []
    results = []
    for key, data in past_deconjugations.items():
        replacement_options = data["return-options"]
        conj_type = data["type"]
        if word.endswith(key):
            if conj_type == "1-ta" and word[-2] not in i_regex + e_regex:
                continue
            results.extend(
                [
                    (word[::-1].replace(key[::-1], option[::-1], 1)[::-1], conj_type)
                    for option in replacement_options
                ]
            )
    return list(set(results))


def deconjugate_adjective(word):
    if not adj_deconjugatable(word):
        return []

    results = []
    for key, data in list(i_adj_conjugations.items()):
        if word.endswith(key):
            # いい→よく not いく
            if key == "く" and len(word) > 1 and word[-2] == "い":
                continue
            options = data["return-options"]
            name = data["name"]
            conj_type = data["type"]
            for option in options:
                results.append((word[: -len(key)] + option, name, conj_type))

    for key, data in list(na_adj_conjugations.items()):
        options = data["return-options"]
        name = data["name"]
        conj_type = data["type"]
        if word.endswith(key):
            for option in options:
                results.append((word[: -len(key)] + option, name, conj_type))

    return list(set(results))


def handle_conjugation(
    match,
    word,
    table,
    previous_conj_type,
    u_set,
    source_set,
    parent,
    tree,
    jisho,
    depth,
    previous_conj_name,
    conj_type,
    extra_check=lambda w, c, i: True,
    replace_func=None,
):
    """
    Generic handler for godan/ichidan conjugations.
    - match: regex match object
    - table: conjugation dict (a_conj, i_conj, etc.)
    - u_set, source_set: character sets like u_, a_, i_, etc.
    - extra_check: function (word, changed_letter, changed_index) -> bool
    - replace_func: optional custom replacement for new_word
    - code: identifier like "5a", "1i"
    """
    if not match:
        return

    c = match.groups()[0]
    name = table[c]["name"]

    changed_index = len(word) - len(c) - 1
    changed_letter = word[changed_index]

    if not extra_check(word, changed_letter, changed_index, previous_conj_type):
        return

    if replace_func:
        new_word = replace_func(word, changed_index, changed_letter)
    else:
        new_word = word[:changed_index] + u_set[source_set.index(changed_letter)]

    if word in jisho and word not in tree.previous_forms:
        parent.add_node(
            Tree((word, previous_conj_name, previous_conj_type), parent, jisho)
        )

    if new_word not in tree.previous_forms:
        tree.add_node(deconjugate(new_word, name, conj_type, depth + 1, tree))


def handle_irregular(
    word,
    match,
    table,
    tree,
    parent,
    jisho,
    depth,
    previous_conj_name,
    previous_conj_type,
):
    """
    Generic handler for suru/kuru conjugations.
    - match: regex match object (truthy if matched)
    - table: suru_conjugations or kuru_conjugations
    """
    if not match:
        return

    for c, data in table.items():
        add = data["return-options"][0]
        name = data["name"]
        conj_type = data["type"]
        if word.endswith(c):
            changed_index = len(word) - len(c) - 1
            new_word = word[: changed_index + 1] + add

            if word in jisho and word not in tree.previous_forms:
                parent.add_node(
                    Tree((word, previous_conj_name, previous_conj_type), parent, jisho)
                )
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, conj_type, depth + 1, tree))


def deconjugate(word, last_conjugation=None, conj_type=None, depth=0, parent=None):
    # I see no reason to not keep this, but this shouldn't be needed
    # because of the no previous forms allowed thing
    # I'll keep it as a safety measure, I guess
    if len(word) < 2:
        raise ValueError("Word too short, fuck you")
    if depth > 15:
        return Tree((word, last_conjugation, conj_type), parent, jisho)
    godan = godan_deconjugatable(word)
    ichidan = ichidan_deconjugatable(word)
    suru = suru_deconjugatable.search(word)
    kuru = kuru_deconjugatable.search(word)
    masu = masu_deconjugatable.search(word)
    adj = deconjugate_adjective(word)
    te = deconjugate_te(word)
    past = deconjugate_past(word)

    if not (godan or ichidan or te or suru or kuru or adj or past):
        return Tree((word, last_conjugation, conj_type), parent, jisho)

    tree = Tree((word, last_conjugation, conj_type), parent, jisho)

    if depth == 0:
        parent = tree

    # --- Apply rules ---
    for rule in rules:
        match = rule["match"](godan if rule["conj_type"].startswith("5") else ichidan)
        handle_conjugation(
            match=match,
            word=word,
            table=rule["table"],
            previous_conj_type=conj_type,
            u_set=rule["u_set"],
            source_set=rule["source_set"],
            parent=parent,
            tree=tree,
            jisho=jisho,
            depth=depth,
            previous_conj_name=last_conjugation,
            conj_type=rule["conj_type"],
            extra_check=rule.get("extra", lambda w, c, i: True),
            replace_func=rule.get("replace"),
        )

    # --- Irregular verbs ---
    handle_irregular(
        word=word,
        match=kuru,
        table=kuru_conjugations,
        tree=tree,
        parent=parent,
        jisho=jisho,
        depth=depth,
        previous_conj_name=last_conjugation,
        previous_conj_type=conj_type,
    )

    handle_irregular(
        word=word,
        match=suru,
        table=suru_conjugations,
        tree=tree,
        parent=parent,
        jisho=jisho,
        depth=depth,
        previous_conj_name=last_conjugation,
        previous_conj_type=conj_type,
    )

    handle_irregular(
        word=word,
        match=masu,
        table=masu_conjugations,
        tree=tree,
        parent=parent,
        jisho=jisho,
        depth=depth,
        previous_conj_name=last_conjugation,
        previous_conj_type=conj_type,
    )

    if te:
        new_conjugation_type = None
        for option, name, new_conjugation_type in te:
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(
                    Tree((word, last_conjugation, conj_type), parent, jisho)
                )
            tree.add_node(
                deconjugate(option, name, new_conjugation_type, depth + 1, tree)
            )

    if adj:
        if word in jisho and word not in tree.previous_forms:
            parent.add_node(Tree((word, last_conjugation, conj_type), parent, jisho))

        for option, name, adj_conj_type in adj:
            if option not in tree.previous_forms:
                tree.add_node(deconjugate(option, name, adj_conj_type, depth + 1, tree))

    if past:
        if word in jisho and word not in tree.previous_forms:
            parent.add_node(Tree((word, last_conjugation, conj_type), parent, jisho))
        for option, new_conjugation_type in past:
            tree.add_node(
                deconjugate(option, "過去形", new_conjugation_type, depth + 1, tree)
            )

    if depth == 0:
        # print("BEFORE CLEAN")
        # print(tree)
        tree.clean()
        # print("AFTER CLEAN")
        print(tree)

    return tree


# while 1:
base_form = deconjugate(word)
base_form.invert_print()
print("-" * 30)
