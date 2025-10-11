from rules import get_routes

u_dan_to_letter = {
    "う": "u",
    "く": "k",
    "ぐ": "g",
    "す": "s",
    "ず": "z",
    "つ": "t",
    "づ": "z",
    "ぬ": "n",
    "ふ": "f",
    "ぶ": "b",
    "ぷ": "p",
    "む": "m",
    "ゆ": "y",
    "る": "r",
}


def _infer_word_type(conj_type, word):
    """Infer the jisho key for the given conj_type + word (keeps your original convention)."""
    if not conj_type:
        return conj_type
    first = conj_type[0]
    if first in ("1", "5", "k", "v", "s"):
        if first == "5":
            u_letter = u_dan_to_letter.get(word[-1], "")
            base = first + u_letter
        else:
            base = first
        return "v" + base
    return conj_type


def _valid_in_jisho(jisho, word, word_type):
    if word not in jisho:
        return False
    if word_type in jisho[word]:
        return True
    # special-case you used before
    if word_type == "vs" and "vs-i" in jisho[word]:
        return True
    return False


class Tree:
    def __init__(self, value=None, parent=None, jisho=None):
        self.branches = []
        self.is_leaf = True
        self.value = value
        self.parent = parent
        if jisho is None:
            self.jisho = {}
        else:
            self.jisho = jisho

        # initialize previous forms
        if parent is None:
            self.previous_forms = set([self.value[0]])
        else:
            # copy parent's history + include parent's current value
            self.previous_forms = parent.previous_forms.copy()
            self.previous_forms.add(self.value[0])
            if parent.value:
                self.previous_forms.add(parent.value[0])

    def add_node(self, node):
        # parent.add_node(Tree((word, last_conjugation, conj_type), parent, jisho))
        word, conj_name, conj_type = node.value
        routes = get_routes(conj_name, conj_type, word)
        invalid_route = False
        if self.value[2] and not any(self.value[2].startswith(r) for r in routes):
            invalid_route = True

        if invalid_route:
            # invalid node
            return

        node.parent = self
        self.branches.append(node)
        self.is_leaf = False

    def clean(self):
        num_deleted = 0
        seen = set()  # track leaves under this branch

        for i, branch in enumerate(self.branches.copy()):
            if branch.is_leaf:
                # key to detect duplicates
                key = branch.value
                word, conj_name, conj_type = branch.value
                word_type = None
                if conj_type[0] in ["1", "5", "k", "s"]:
                    word_type = (
                        conj_type[0]
                        if conj_type[0] != "5"
                        else conj_type[0] + u_dan_to_letter[word[-1]]
                    )
                    # 1a -> 1
                    # 5a -> 5 + u-row
                    # kuru -> k
                    # suru -> s
                    word_type = f"v{word_type}"
                    # 1 -> 1v
                    # 5 -> v5u
                    # kuru -> vk
                    # suru -> vs

                delete = False
                # Not a valid word, or the conjugation used to get there
                # doesn't match the target word's word type
                if word not in self.jisho or word_type not in self.jisho[word]:
                    if (
                        word in self.jisho
                        and word_type not in self.jisho[word]
                        and word_type == "vs"
                        and "vs-i" in self.jisho[word]
                    ):
                        ...
                    else:
                        delete = True
                        # print(word, word_type, self.jisho[word] if word in self.jisho else "Not In Jisho")

                elif key in seen:
                    delete = True

                if delete:
                    if i - num_deleted < len(self.branches):
                        del self.branches[i - num_deleted]
                    num_deleted += 1

                    # if removing the last child, collapse
                    if len(self.branches) == 0:
                        self.is_leaf = True
                        if self.parent:
                            self.parent.clean()
                else:
                    seen.add(key)
            else:
                branch.clean()

    def set_value(self, value):
        self.value = value

    def __str__(self, level=0):
        indent = "  " * level
        if self.value is None:
            node_repr = "<empty>"
        else:
            word, conj, conj_type = self.value
            conj_string = f"[{conj}|{conj_type}]" if conj and conj_type else ""
            node_repr = f"{word} {conj_string}"
        result = f"{indent}{node_repr}\n"
        for branch in self.branches:
            result += branch.__str__(level + 1)
        return result

    def go_up(self):
        if self.parent is None:
            word, conj, conj_type = self.value
            return word
        else:
            word, conj, conj_type = self.value
            return f"{word} --[{conj}|{conj_type}]--> {self.parent.go_up()}"

    def invert_print(self, level=0):
        leaves = []
        for branch in self.branches:
            if branch.is_leaf:
                leaves.append(branch)
            else:
                branch.invert_print(level + 1)

        for leaf in leaves:
            print(leaf.go_up())
