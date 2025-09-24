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

word = "されし"


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
# Ichidan endings grouped by vowel row
ichidan_deconjugatable_a = re.compile(
    rf"[{a_regex}]({'|'.join(a_conj_ichidan.keys())})$"
)
ichidan_deconjugatable_i = re.compile(rf"[{i_regex}]({'|'.join(i_conj.keys())})$")
ichidan_deconjugatable_u = re.compile(rf"[{u_regex}]({'|'.join(u_conj.keys())})$")
ichidan_deconjugatable_e = re.compile(
    rf"[{e_regex}]({'|'.join(e_conj_ichidan.keys())})$"
)
ichidan_deconjugatable_o = re.compile(
    rf"[{o_regex}]({'|'.join(o_conj_ichidan.keys())})$"
)


def ichidan_deconjugatable(word):
    return [
        ichidan_deconjugatable_a.search(word),
        ichidan_deconjugatable_i.search(word),
        ichidan_deconjugatable_u.search(word),
        ichidan_deconjugatable_e.search(word),
        ichidan_deconjugatable_o.search(word),
    ]


adj_keys = list(i_adj_conjugations.keys()) + list(na_adj_conjugations.keys())


def te_deconjugatable(word):
    return word[-1] in [form[-1] for form in te_deconjugations.keys()]


def past_deconjugatable(word):
    return word[-1] in [form[-1] for form in past_deconjugations.keys()]


def adj_deconjugatable(word):
    return word[-1] in [form[-1] for form in adj_keys]


# Regex patterns for suru/kuru
suru_deconjugatable = re.compile(rf"(?:{'|'.join(suru_conjugations)})$")

kuru_deconjugatable = re.compile(rf"(?:{'|'.join(kuru_conjugations)})$")


def deconjugate_te(word):
    if not te_deconjugatable(word):
        return []

    results = []
    for key, (values, name) in te_deconjugations.items():
        if word.endswith(key):
            # Special case: avoid false positives for "て"
            if key == "て" and word[-2] not in i_ + e_:
                continue

            for value in values:
                new_word = word[: -len(key)] + value
                results.append((new_word, name))

    return results


def deconjugate_past(word):
    if not past_deconjugatable(word):
        return []

    for key, values in past_deconjugations.items():
        if word.endswith(key):
            if key == "た" and word[-2] not in i_ + e_:
                continue
            return [word[: -len(key)] + value for value in values]

    return []


def deconjugate_adjective(word):
    if not adj_deconjugatable(word):
        return []

    conjugations = []
    for key, (options, name) in list(i_adj_conjugations.items()) + list(
        na_adj_conjugations.items()
    ):
        if word.endswith(key):
            if key == "く" and len(word) > 1 and word[-2] == "い":
                continue
            for option in options:
                conjugations.append((word[: -len(key)] + option, name))

    return conjugations


def deconjugate(word, last_conjugation=None, depth=0, parent=None, hinsi=None):
    # I see no reason to not keep this, but this shouldn't be needed
    # because of the no previous forms allowed thing
    # I'll keep it as a safety measure, I guess
    if depth > 15:
        return Tree((word, last_conjugation), parent, jisho)

    godan = godan_deconjugatable(word)
    ichidan = ichidan_deconjugatable(word)
    suru = suru_deconjugatable.search(word)
    kuru = kuru_deconjugatable.search(word)
    adj = deconjugate_adjective(word)
    te = deconjugate_te(word)
    past = deconjugate_past(word)
    if not (godan or ichidan or te or suru or kuru or adj or past):
        return Tree((word, last_conjugation), parent, jisho)
    tree = Tree((word, last_conjugation), parent, jisho)

    if depth == 0:
        parent = tree

    godan_a, godan_i, godan_u, godan_e, godan_o = godan
    if godan_a:
        c = godan_a.groups()[0]
        name = a_conj[c]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in a_ and word[changed_index - 1] != "来":
            new_word = word[:changed_index] + u_[a_.index(changed_letter)]
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, last_conjugation), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, depth + 1, tree, "動詞"))

    if godan_i:
        c = godan_i.groups()[0]
        name = i_conj[c]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in i_:
            new_word = word[:changed_index] + u_[i_.index(changed_letter)]
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, last_conjugation), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, depth + 1, tree, "動詞"))

    if godan_u:
        c = godan_u.groups()[0]
        name = u_conj[c]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in u_:
            new_word = word[:changed_index] + u_[u_.index(changed_letter)]
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, last_conjugation), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, depth + 1, tree, "動詞"))
    if godan_e:
        c = godan_e.groups()[0]
        name = e_conj[c]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in e_ and not (
            changed_letter == "れ" and word[changed_index - 1] in ["く", "す"]
        ):
            new_word = word[:changed_index] + u_[e_.index(changed_letter)]
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, last_conjugation), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, depth + 1, tree, "動詞"))
    if godan_o:
        c = godan_o.groups()[0]
        name = o_conj[c]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in o_:
            new_word = word[:changed_index] + u_[o_.index(changed_letter)]
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, last_conjugation), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, depth + 1, tree, "動詞"))

    ichidan_a, ichidan_i, ichidan_u, ichidan_e, ichidan_o = ichidan
    if ichidan_a:
        c = ichidan_a.groups()[0]
        name = a_conj_ichidan[c]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in i_ or changed_letter in e_:
            new_word = word[: changed_index + 1] + "る"
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, last_conjugation), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, depth + 1, tree, "動詞"))
    if ichidan_i:
        c = ichidan_i.groups()[0]
        name = i_conj[c]
        # ["たい", "やすい", "にくい", "がたい", "づらい"]
        if not (
            hinsi == "形容詞" and not c.endswith("い")
        ):  # 強(つよ)く ADJ →強(つよ)い ADJ →強(し)いる VERB?!
            changed_index = len(word) - len(c) - 1
            changed_letter = word[changed_index]
            if changed_letter in i_ or changed_letter in e_:
                if not (len(word) > 2 and word[changed_index - 1] == "な"):
                    new_word = word[: changed_index + 1] + "る"

                    if word in jisho and word not in tree.previous_forms:
                        parent.add_node(Tree((word, last_conjugation), parent, jisho))
                    if changed_letter == "れ" and word[changed_index - 1] == "く":
                        name += "／命令形"
                    if new_word not in tree.previous_forms:
                        tree.add_node(
                            deconjugate(new_word, name, depth + 1, tree, "動詞")
                        )
    if ichidan_u:
        c = ichidan_u.groups()[0]
        name = u_conj[c]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in i_ or changed_letter in e_:
            new_word = word[: changed_index + 1] + "る"
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, last_conjugation), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, depth + 1, tree, "動詞"))
    if ichidan_e:
        c = ichidan_e.groups()[0]
        name = e_conj_ichidan[c]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in i_ or changed_letter in e_:
            new_word = word[: changed_index + 1] + "る"
            print(new_word)
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, last_conjugation), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, depth + 1, tree, "動詞"))

    if ichidan_o:
        c = ichidan_o.groups()[0]
        name = o_conj_ichidan[c]
        changed_index = len(word) - len(c) - 1
        changed_letter = word[changed_index]
        if changed_letter in i_ or changed_letter in e_:
            new_word = word[: changed_index + 1] + "る"
            if word in jisho and word not in tree.previous_forms:
                parent.add_node(Tree((word, last_conjugation), parent, jisho))
            if new_word not in tree.previous_forms:
                tree.add_node(deconjugate(new_word, name, depth + 1, tree, "動詞"))

    if suru:
        for c, name in suru_conjugations.items():
            if word.endswith(c):
                changed_index = len(word) - len(c) - 1
                new_word = word[: changed_index + 1] + "する"
                if word in jisho and word not in tree.previous_forms:
                    parent.add_node(Tree((word, last_conjugation), parent, jisho))
                if new_word not in tree.previous_forms:
                    tree.add_node(deconjugate(new_word, name, depth + 1, tree, "動詞"))

    if kuru:
        for c, name in kuru_conjugations.items():
            if word.endswith(c):
                changed_index = len(word) - len(c) - 1
                if "来" in c:
                    add = "来る"
                else:
                    add = "くる"
                new_word = word[: changed_index + 1] + add
                if word in jisho and word not in tree.previous_forms:
                    parent.add_node(Tree((word, last_conjugation), parent, jisho))
                if new_word not in tree.previous_forms:
                    tree.add_node(deconjugate(new_word, name, depth + 1, tree, "動詞"))

    if te:
        for option, name in te:
            tree.add_node(deconjugate(option, name, depth + 1, tree, "動詞"))

    if adj:
        for option, name in adj:
            if hinsi == "動詞" and "副動詞" not in name:
                continue
            tree.add_node(deconjugate(option, name, depth + 1, tree, "形容詞"))

    if past and hinsi in ["動詞", None]:
        for option in past:
            tree.add_node(deconjugate(option, "過去形", depth + 1, tree, "動詞"))

    if depth == 0:
        print("BEFORE CLEAN")
        print(tree)
        tree.clean()
        print("AFTER CLEAN")
        print(tree)

    return tree


# while 1:
base_form = deconjugate(word)
base_form.invert_print()
print("-" * 30)
