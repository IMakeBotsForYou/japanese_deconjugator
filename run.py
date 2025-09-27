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
)
from tree import Tree

jisho = {}
with open("jisho.json", "r", encoding="utf-8") as f:
    jisho = json.load(f)

word = "つよく"

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

past_conjugatable = re.compile(rf"(?:{'|'.join(past_deconjugations.keys())})$")

te_conjugatable = re.compile(rf"(?:{'|'.join(te_deconjugations.keys())})$")


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
    adj = deconjugate_adjective(word)
    te = deconjugate_te(word)
    past = deconjugate_past(word)
    if not (godan or ichidan or te or suru or kuru or adj or past):
        return Tree((word, last_conjugation, conj_type), parent, jisho)

    tree = Tree((word, last_conjugation, conj_type), parent, jisho)

    if depth == 0:
        parent = tree

    godan_a, godan_i, godan_u, godan_e, godan_o = godan
    if godan_a:
        c = godan_a.groups()[0]
        name = a_conj[c]["name"]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in a_ and word[changed_index - 1] != "来":
            new_word = word[:changed_index] + u_[a_.index(changed_letter)]
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, name, conj_type), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, "5a", depth + 1, tree))

    if godan_i:
        c = godan_i.groups()[0]
        name = i_conj[c]["name"]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in i_ and not conj_type.endswith("adj"):
            # ~やすい など

            new_word = word[:changed_index] + u_[i_.index(changed_letter)]
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, name, conj_type), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, "5i", depth + 1, tree))

    if godan_u:
        c = godan_u.groups()[0]
        name = u_conj[c]["name"]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in u_:
            new_word = word[:changed_index] + u_[u_.index(changed_letter)]
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, name, conj_type), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, "5u" + 1, tree))

    if godan_e:
        c = godan_e.groups()[0]
        name = e_conj[c]["name"]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in e_ and not (
            changed_letter == "れ" and word[changed_index - 1] in ["く", "す"]
        ):
            new_word = word[:changed_index] + u_[e_.index(changed_letter)]
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, name, conj_type), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, "5e", depth + 1, tree))

    if godan_o:
        c = godan_o.groups()[0]
        name = o_conj[c]["name"]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in o_:
            new_word = word[:changed_index] + u_[o_.index(changed_letter)]
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(
                    Tree((word, last_conjugation, conj_type), parent, jisho)
                )
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, "5o", depth + 1, tree))

    ichidan_a, ichidan_i, ichidan_u, ichidan_e, ichidan_o = ichidan
    if ichidan_a:
        c = ichidan_a.groups()[0]
        name = a_conj_ichidan[c]["name"]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in i_ or changed_letter in e_:
            new_word = word[: changed_index + 1] + "る"
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(
                    Tree((word, last_conjugation, conj_type), parent, jisho)
                )
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, "1a", depth + 1, tree))

    if ichidan_i:
        c = ichidan_i.groups()[0]
        name = i_conj[c]["name"]

        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in i_ or changed_letter in e_:
            if not word.endswith("ない") and not conj_type.endswith("adj"):
                new_word = word[: changed_index + 1] + "る"

                if word in jisho and word not in tree.previous_forms:
                    parent.add_node(Tree((word, name, conj_type), parent, jisho))
                if changed_letter == "れ" and word[changed_index - 1] == "く":
                    name += "／命令形"
                if new_word not in tree.previous_forms:
                    tree.add_node(deconjugate(new_word, name, "1i", depth + 1, tree))

    if ichidan_u:
        c = ichidan_u.groups()[0]
        name = u_conj[c]["name"]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in i_ or changed_letter in e_:
            new_word = word[: changed_index + 1] + "る"
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, name, conj_type), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, "1u", depth + 1, tree))

    if ichidan_e:
        c = ichidan_e.groups()[0]
        name = e_conj_ichidan[c]["name"]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in i_ or changed_letter in e_:
            new_word = word[: changed_index + 1] + "る"
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, name, conj_type), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, "1e", depth + 1, tree))

    if ichidan_o:
        c = ichidan_o.groups()[0]
        name = o_conj_ichidan[c]["name"]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in i_ or changed_letter in e_:
            new_word = word[: changed_index + 1] + "る"
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, name, conj_type), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, "1o", depth + 1, tree))

    if kuru:
        for c, data in kuru_conjugations.items():
            add = data["return-options"][0]  # only one option
            name = data["name"]
            conj_type = data["type"]

            if word.endswith(c):
                changed_index = len(word) - len(c) - 1
                new_word = word[: changed_index + 1] + add
                if word in jisho and word not in tree.previous_forms:
                    parent.add_node(Tree((word, name, conj_type), parent, jisho))
                if new_word not in tree.previous_forms:
                    tree.add_node(deconjugate(new_word, name, "kuru", depth + 1, tree))

    if te:
        new_conjugation_type = None
        for option, name, new_conjugation_type in te:
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, name, conj_type), parent, jisho))
            tree.add_node(
                deconjugate(option, name, new_conjugation_type, depth + 1, tree)
            )

    if adj:
        for option, name, adj_conj_type in adj:
            if option in jisho and option not in tree.previous_forms:
                parent.add_node(Tree((option, name, adj_conj_type), parent, jisho))
            tree.add_node(deconjugate(option, name, adj_conj_type, depth + 1, tree))

    if past:
        for option, new_conjugation_type in past:
            if option in jisho and option not in tree.previous_forms:
                parent.add_node(
                    Tree((option, last_conjugation, conj_type), parent, jisho)
                )
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
