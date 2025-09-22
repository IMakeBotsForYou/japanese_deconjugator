import re
import json 

jisho = {}
with open("jisho.json", "r", encoding='utf-8') as f:
	jisho = json.load(f)

word = "強く"


a_ = "あかがさざただなはばぱまやらわ"
i_ = "いきぎしじちぢにひびぴみゐり_"
u_ = "うくぐすずつづぬふぶぷむゆる_"
e_ = "えけげせぜてでねへべぺめゑれ_"
o_ = "おこごそぞとどのほぼぽもよろを"

a_regex = "あかがさざただなはばぱまやらわ"
i_regex = "いきぎしじちぢにひびぴみり"
u_regex = "うくぐすずつづぬふぶぷむゆる"
e_regex = "えけげせぜてでねへべぺめれ"
o_regex = "おこごそぞとどのほぼぽもよろを"


a_conj = {
	"れる": "受け身",
	"せる": "使役",
	"ない": "打ち消し"
}

a_conj_ichidan = {
	"られる": "受け身／可能",
	"させる": "使役",
	"ない": "打ち消し"
}

i_conj = {
	"": "連用形",
	"たい": "希望",
	"ます": "丁寧",
	"にくい": "難易",
	"がたい": "難易",
	"やすい": "容易"
}

u_conj = {
	"な": "禁止"
}

e_conj = {
	"": "命令形",
	"る": "可能形",
	"ば": "仮定形"
}

e_conj_ichidan = {
	"ろ": "命令形"
}

o_conj = {
	"う": "意向形"
}

# Godan endings grouped by vowel row
godan_deconjugatable = re.compile(
	rf"(?:"
	rf"([{a_regex}](?:{'|'.join(a_conj.keys())}))|"	   # A-row endings
	rf"([{i_regex}](?:{'|'.join(i_conj.keys())}))|"   # I-row endings
	rf"([{u_regex}](?:{'|'.join(u_conj.keys())}))|"	   # U-row endings
	rf"([{e_regex}](?:{'|'.join(e_conj.keys())}))|"   # E-row endings
	rf"([{o_regex}](?:{'|'.join(o_conj.keys())}))"		# O-row endings
	 f")$"
)

# Ichidan: must end in i/e-row + one of the valid suffixes
ichidan_deconjugatable = re.compile(
	rf"(?:[{e_regex}{i_regex}](?:{'|'.join(list(a_conj_ichidan.keys()) + list(i_conj.keys()) + list(u_conj.keys()) + list(e_conj_ichidan.keys()) + list(o_conj.keys()))}))$"
)

i_adj_conjugations = {
	"かった": (["い"], "過去形"), 
	"くて": (["い"], "連用形・て形"),
	"くない": (["い"], "打ち消し"),
	"く": (["い"], "連用形"),
	"よく": (["よい", "いい"], "連用形"),
	"かろう": (["い"], "意向形"),
	"くなる": (["く"], "副動詞 なる"),
	"くする": (["く"], "副動詞 する"),
}

na_adj_conjugations = {
	"な": ([""], "連体形"),
	"じゃない": ([""], "打ち消し"),
	"だった": ([""], "過去形"),
	"だ": ([""], "終止形"),
	"に": ([""], "連用形"),
	"の": ([""], "連体形"),
	"と": ([""], "引用"),
	"になる": ([""], "副動詞 なる"),
	"にする": ([""], "副動詞 する"),
}
te_deconjugations = {
    # Special irregular verbs
    "乞うて":   (["乞う"], "テ形 (特殊)"),
    "こうて":   (["こう"], "テ形 (特殊)"),
    "問うて":   (["問う"], "テ形 (特殊)"),
    "とうて":   (["とう"], "テ形 (特殊)"),
    "厭うて":   (["厭う"], "テ形 (特殊)"),
    "いとうて": (["いとう"], "テ形 (特殊)"),
    "宣うて":  (["宣う"], "テ形 (特殊)"),
    "曰うて":  (["曰う"], "テ形 (特殊)"),
    "のたまうて": (["のたまう"], "テ形 (特殊)"),

    # 補助動詞・複合
    "て来る":   (["て"], "補助動詞 来る"),
    "てくる":   (["て"], "補助動詞 くる"),
    "ていく":   (["て"], "補助動詞 行く"),
    "て行く":   (["て"], "補助動詞 行く"),
    "て呉れる": (["て"], "補助動詞 呉れる"),
    "てくれる": (["て"], "補助動詞 くれる"),
    "ておく":   (["て"], "補助動詞 おく"),
    "て置く":   (["て"], "補助動詞 置く"),
    "てやる":   (["て"], "補助動詞 やる"),
    "てもらう": (["て"], "補助動詞 もらう"),
    "て貰う":   (["て"], "補助動詞 貰う"),
    "ていただく": (["て"], "補助動詞 いただく"),
    "て頂く":   (["て"], "補助動詞 頂く"),
    "てしまう": (["て"], "補助動詞 しまう"),
    "ちゃう":   (["て"], "補助動詞 しまう (縮約形)"),
    "じゃう":   (["て"], "補助動詞 しまう (縮約形)"),
    "ちまう":   (["て"], "補助動詞 しまう (縮約形)"),
    "じまう":   (["で"], "補助動詞 しまう (縮約形)"),
    "でくる":   (["で"], "補助動詞 くる"),
    "で来る":   (["で"], "補助動詞 来る"),
    "でいく":   (["で"], "補助動詞 行く"),
    "で行く":   (["で"], "補助動詞 行く"),
    "でくれる": (["で"], "補助動詞 くれる"),
    "で呉れる": (["で"], "補助動詞 呉れる"),
    "でおく":   (["で"], "補助動詞 おく"),
    "で置く":   (["で"], "補助動詞 置く"),
    "でやる":   (["で"], "補助動詞 やる"),
    "でもらう": (["で"], "補助動詞 もらう"),
    "で貰う":   (["で"], "補助動詞 貰う"),
    "でいただく": (["で"], "補助動詞 いただく"),
    "で頂く":   (["で"], "補助動詞 頂く"),

    # Irregular 行く
    "行って": (["行く"], "テ形 (行く)"),
    "いって": (["いく"], "テ形 (行く)"),

    # Regular sound-change groups
    "って": (["う", "つ", "る"], "テ形"),
    "いて": (["く"], "テ形"),
    "いで": (["いる", "ぐ"], "テ形"),
    "んで": (["む", "ぬ", "ぶ"], "テ形"),
    "して": (["する", "す"], "テ形"),
    "て":   (["る"], "テ形")
}


past_deconjugations = {
	"乞うた": ["乞う"],
	"こうた": ["こう"],
	"問うた": ["問う"],
	"とうた": ["とう"],
	"厭うた": ["厭う"],
	"いとうた": ["いとう"],
	"宣うた": ["宣う"],
	"曰うた": ["曰う"],
	"のたまうた": ["のたまう"],
	"きた": ["くる", "きる"],
	"来た": ["くる"],
	"行った": ["行く"],
	"いった": ["いう", "いく", "いる", "いつ"],
	"した": ["する", "す"],
	"った": ["う", "る", "つ"],
	"いた": ["く"],
	"いだ": ["ぐ"],
	"んだ": ["む", "ぬ", "ぶ"],
	"た": ["る"]
}

adj_keys = list(i_adj_conjugations.keys()) + list(na_adj_conjugations.keys())

te_deconjugatable = lambda word: word[-1] in [form[-1] for form in te_deconjugations.keys()]
past_deconjugatable = lambda word: word[-1] in [form[-1] for form in past_deconjugations.keys()]

adj_deconjugatable = lambda word: word[-1] in [form[-1] for form in adj_keys]

suru_conjugations = {
	"させる": "使役",
	"される": "受け身",
	"しない": "否定",
	"したい": "希望",
	"します": "丁寧",
	"するな": "禁止",
	"しろ":   "命令",
	"しよう": "意向"
}

kuru_conjugations = {
	# Kanji forms
	"来させる": "使役",
	"来られる": "受け身",
	"来たい":   "希望",
	"来ます":   "丁寧",
	"来るな":   "禁止",
	"来い":	 "命令",
	"来よう":   "意向",
	# Hiragana forms
	"こさせる": "使役",
	"こられる": "受け身",
	"きたい":   "希望",   
	"きます":   "丁寧",   
	"くるな":   "禁止",  
	"こい":	 "命令",
	"こよう":   "意向"
}

# Regex patterns for suru/kuru
suru_deconjugatable = re.compile(
	rf"(?:{'|'.join(suru_conjugations)})$"
)

kuru_deconjugatable = re.compile(
	rf"(?:{'|'.join(kuru_conjugations)})$"
)


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
                new_word = word[:-len(key)] + value
                results.append((new_word, name))

    return results


def deconjugate_past(word):

	if not past_deconjugatable(word):
		return []

	for key, values in past_deconjugations.items():
		if word.endswith(key):
			if key == "た" and word[-2] not in i_+e_:
				continue
			return [word[:-len(key)] + value for value in values]
			
	return []

def deconjugate_adjective(word):

	if not adj_deconjugatable(word):
		return []
	
	conjugations = []
	for key, (options, name) in list(i_adj_conjugations.items())+list(na_adj_conjugations.items()):
		if word.endswith(key):
			if key == "く" and len(word) > 1 and word[-2] == "い":
				continue
			for option in options:		
				conjugations.append((word[:-len(key)] + option, name))
				
	return conjugations

class Tree:
	def __init__(self, value=None, parent=None):
		self.branches = []
		self.is_leaf = True
		self.value = value
		self.parent = parent

		# initialize previous forms
		if parent is None:
			self.previous_forms = set()
		else:
			# copy parent's history + include parent's current value
			self.previous_forms = set(parent.previous_forms)
			if parent.value:
				self.previous_forms.add(parent.value)

	def add_node(self, node):
		node.parent = self
		# update child’s previous_forms dynamically when attaching
		node.previous_forms = set(self.previous_forms)
		if self.value:
			node.previous_forms.add(self.value)

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

				if key in seen or key[0] not in jisho:
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
			word, conj = self.value
			node_repr = f"{word} [{conj}]" if conj else word
		result = indent + node_repr + f"  (prev: {len(self.previous_forms)})\n"
		for branch in self.branches:
			result += branch.__str__(level + 1)
		return result

	def go_up(self):
		if self.parent is None:
			word, conj = self.value
			return word
		else:
			word, conj = self.value
			return f"{word} --[{conj}]--> {self.parent.go_up()}"

	def invert_print(self, level=0):
		leaves = []
		for branch in self.branches:
			if branch.is_leaf:
				leaves.append(branch)
			else:
				branch.invert_print(level + 1)

		for leaf in leaves:
			print(leaf.go_up())

def deconjugate(word, last_conjugation=None, depth=0, parent=None, hinsi=None):
	# I see no reason to not keep this, but this shouldn't be needed
	# because of the no previous forms allowed thing
	# I'll keep it as a safety measure, I guess

	godan = godan_deconjugatable.search(word)
	ichidan = ichidan_deconjugatable.search(word) 
	suru = suru_deconjugatable.search(word)
	kuru = kuru_deconjugatable.search(word)
	adj  = deconjugate_adjective(word)
	te = deconjugate_te(word)
	past = deconjugate_past(word)
	if not (godan or ichidan or te or suru or kuru or adj or past):
		return Tree((word, last_conjugation), parent)

	if depth > 15:
		return Tree((word, last_conjugation))
	tree = Tree((word, last_conjugation), parent)

	if depth == 0:
		parent = tree

	if godan:
		for c, name in a_conj.items():
			if not word.endswith(c):
				continue
			changed_index = len(word) - len(c) - 1
			changed_letter = word[changed_index]
			if changed_letter in a_ and word[changed_index-1] != "来":
				new_word = word[:changed_index] + u_[a_.index(changed_letter)]
				if word in jisho:
					parent.add_node(Tree((word, last_conjugation), parent))
				if new_word not in tree.previous_forms:
					tree.add_node(deconjugate(new_word, name, depth+1, tree, "動詞"))

		for c, name in i_conj.items():
			if not word.endswith(c):
				continue
			changed_index = len(word) - len(c) - 1
			changed_letter = word[changed_index]
			if changed_letter in i_:
				new_word = word[:changed_index] + u_[i_.index(changed_letter)]
				if word in jisho:
					parent.add_node(Tree((word, last_conjugation), parent))
				if new_word not in tree.previous_forms:
					tree.add_node(deconjugate(new_word, name, depth+1, tree, "動詞"))

		for c, name in u_conj.items():
			if not word.endswith(c):
				continue
			changed_index = len(word) - len(c) - 1
			changed_letter = word[changed_index]
			if changed_letter in u_:
				new_word = word[:changed_index] + u_[u_.index(changed_letter)]
				if word in jisho:
					parent.add_node(Tree((word, last_conjugation), parent))
				if new_word not in tree.previous_forms:
					tree.add_node(deconjugate(new_word, name, depth+1, tree, "動詞"))

		for c, name in e_conj.items():
			if not word.endswith(c):
				continue
			changed_index = len(word) - len(c) - 1
			changed_letter = word[changed_index]
			if changed_letter in e_ and not (changed_letter == "れ" and word[changed_index-1] in ["く", "す"]):
				new_word = word[:changed_index] + u_[e_.index(changed_letter)]
				if word in jisho:
					parent.add_node(Tree((word, last_conjugation), parent))
				if new_word not in tree.previous_forms:
					tree.add_node(deconjugate(new_word, name, depth+1, tree, "動詞"))

		for c, name in o_conj.items():
			if not word.endswith(c):
				continue
			changed_index = len(word) - len(c) - 1
			changed_letter = word[changed_index]
			if changed_letter in o_:
				new_word = word[:changed_index] + u_[o_.index(changed_letter)]
				if word in jisho:
					parent.add_node(Tree((word, last_conjugation), parent))
				if new_word not in tree.previous_forms:
					tree.add_node(deconjugate(new_word, name, depth+1, tree, "動詞"))

	if ichidan:
		for c, name in a_conj_ichidan.items():
			if not word.endswith(c):
				continue
			changed_index = len(word) - len(c) - 1
			changed_letter = word[changed_index]
			if changed_letter in i_ or changed_letter in e_:
				new_word = word[:changed_index+1] + "る"
				if word in jisho:
					parent.add_node(Tree((word, last_conjugation), parent))
				if new_word not in tree.previous_forms:
					tree.add_node(deconjugate(new_word, name, depth+1, tree, "動詞"))

		for c, name in i_conj.items():
			if not word.endswith(c):
				continue			
			if hinsi == "形容詞": # 強(つよ)く ADJ →強(つよ)い ADJ →強(し)いる VERB?! 
				continue
			changed_index = len(word) - len(c) - 1
			changed_letter = word[changed_index]
			if changed_letter in i_ or changed_letter in e_:
				if len(word) > 2 and word[changed_index-1] == "な":
					continue
				new_word = word[:changed_index+1] + "る"
				if word in jisho:
					parent.add_node(Tree((word, last_conjugation), parent))
				if changed_letter == "れ" and word[changed_index-1] == "く":
					name += "／命令形"
				if new_word not in tree.previous_forms:
					hinsi = "動詞"
					tree.add_node(deconjugate(new_word, name, depth+1, tree, hinsi))

		for c, name in u_conj.items():
			if not word.endswith(c):
				continue
			changed_index = len(word) - len(c) - 1
			changed_letter = word[changed_index]
			if changed_letter in i_ or changed_letter in e_:
				new_word = word[:changed_index+1] + "る"
				if word in jisho:
					parent.add_node(Tree((word, last_conjugation), parent))
				if new_word not in tree.previous_forms:
					hinsi = "動詞"
					tree.add_node(deconjugate(new_word, name, depth+1, tree, hinsi))

		for c, name in e_conj_ichidan.items():
			if not word.endswith(c):
				continue
			changed_index = len(word) - len(c) - 1
			changed_letter = word[changed_index]
			if changed_letter in i_ or changed_letter in e_:
				new_word = word[:changed_index+1] + "る"
				if word in jisho:
					parent.add_node(Tree((word, last_conjugation), parent))
				if new_word not in tree.previous_forms:
					hinsi = "動詞"
					tree.add_node(deconjugate(new_word, name, depth+1, tree, hinsi))

		for c, name in o_conj.items():
			if not word.endswith(c):
				continue
			changed_index = len(word) - len(c) - 1
			changed_letter = word[changed_index]
			if changed_letter in i_ or changed_letter in e_:
				new_word = word[:changed_index+1] + "る"
				if word in jisho:
					parent.add_node(Tree((word, last_conjugation), parent))
				if new_word not in tree.previous_forms:
					hinsi = "動詞"
					tree.add_node(deconjugate(new_word, name, depth+1, tree, hinsi))

	if suru:
		for c, name in suru_conjugations.items():
			if word.endswith(c):
				changed_index = len(word) - len(c) - 1
				new_word = word[:changed_index+1] + "する"
				if word in jisho:
					parent.add_node(Tree((word, last_conjugation), parent))
				if new_word not in tree.previous_forms:
					tree.add_node(deconjugate(new_word, name, depth+1, tree, "動詞"))

	if kuru:
		for c, name in kuru_conjugations.items():
			if word.endswith(c):
				changed_index = len(word) - len(c) - 1
				if "来" in c:
					add = "来る"
				else:
					add = "くる"
				new_word = word[:changed_index+1] + add
				if word in jisho:
					parent.add_node(Tree((word, last_conjugation), parent))
				if new_word not in tree.previous_forms:
					tree.add_node(deconjugate(new_word, name, depth+1, tree, "動詞"))

	if te:
		for option, name in te: 
			tree.add_node(deconjugate(option, name, depth+1, tree, "動詞"))

	if adj and hinsi != "動詞":
		for option, name in adj: 
			tree.add_node(deconjugate(option, name, depth+1, tree, "形容詞"))

	if past and hinsi in ["動詞", None]:
		for option in past: 
			tree.add_node(deconjugate(option, "過去形", depth+1, tree, "動詞"))

	if depth == 0:
		tree.clean()

	return tree

base_form = deconjugate(word)

base_form.invert_print()

