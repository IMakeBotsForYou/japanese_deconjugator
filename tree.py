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
        node.parent = self
        self.branches.append(node)
        self.is_leaf = False

    def set_value(self, value):
        self.value = value

    def clean(self):
        num_deleted = 0
        seen = set()  # track leaves under this branch

        for i, branch in enumerate(self.branches.copy()):
            if branch.is_leaf:
                # key to detect duplicates
                key = branch.value
                word, conj_name, conj_type = branch.value
                # print(branch.value)  # debugging
                if conj_type[0] in ["1", "5", "k", "v"]:
                    conj_type = (
                        conj_type[0]
                        if conj_type[0] != "5"
                        else conj_type[0] + u_dan_to_letter[word[-1]]
                    )
                    # 1a -> 1
                    # 5a -> 5 + u-row
                    # kuru -> k
                    # suru -> s
                    conj_type = f"v{conj_type}"
                    # 1 -> 1v
                    # 5 -> v5u
                    # kuru -> vk
                    # suru -> vs

                delete = False
                # Not a valid word, or the conjugation used to get there
                # doesn't match the target word's word type
                if word not in self.jisho or conj_type not in self.jisho[word]:
                    delete = True

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
