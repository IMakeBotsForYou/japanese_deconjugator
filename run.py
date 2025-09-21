import re
import json 

jisho = {}
with open("jisho.json", "r", encoding='utf-8') as f:
	jisho = json.load(f)

word = "食べさせたい"


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






a_conj = ["れる", "れ", "ない", "せる", "せ"]
a_conj_ichidan = ["られる", "られ", "ない", "させる", "させ"]


i_conj = ["", "たい", "ます", "にくい", "がたい", "やすい"]

u_conj = ["な"]
e_conj = ["", "る", "ば"]
e_conj_ichidan = ["ろ"]

o_conj = ["う"]

godan_deconjugatable = re.compile(rf"(?:([{a_regex}](?:{'|'.join(a_conj)}))|"
									 rf"([{i_regex[1:]}](?:{'|'.join(i_conj)}))|"
									 rf"([{u_regex}](?:{'|'.join(u_conj)}))|"
									 rf"([{e_regex[1:]}](?:{'|'.join(e_conj)}))|"
									 rf"([{o_regex}](?:{'|'.join(o_conj)})))$")

ichidan_deconjugatable = re.compile(rf"[{e_regex}{i_regex}](?:{'|'.join(a_conj_ichidan+i_conj+u_conj+e_conj_ichidan+o_conj)})$")

te_deconjugations = {
	"てくる": ["て"],
	"ていく": ["て"],
	"てくれる": ["て"],
	"ておく": ["て"],
	"てやる": ["て"],
	"てもらう": ["て"],
	"ていただく": ["て"],
	"って": ["う", "つ", "る"],
	"いて": ["く"],
	"いで": ["いる", "ぐ"],
	"んで": ["む", "ぬ", "ぶ"],
	"して": ["する", "す"],
	"て": ["る"]
}

suru_conjugations = ["させる", "される", "しない", "したい", "します", "するな", "しろ", "しよう"]
kuru_conjugations =  ["来させる", "来られる", "来たい", "来ます", "来るな", "来い", "来よう"]
kuru_conjugations += ["こさせる", "こられる", "来たい", "来ます", "来るな", "こい", "こよう"]

suru_deconjugatable = re.compile(rf"(?:{'|'.join(suru_conjugations)})$")
kuru_deconjugatable = re.compile(rf"(?:{'|'.join(kuru_conjugations)})$")

def deconjugate_te(word):

	if word[-1] not in ["で", "て", "る"]:
		return []
	for key, values in te_deconjugations.items():
		if word.endswith(key):
			return [word[:-len(key)] + value for value in values if word[:-len(key)] + value in jisho or f"{word[:-len(key)] + value}"[-1] == "て"]

class Tree:
	def __init__(self, value=None, parent=None):
		self.branches = []
		self.is_leaf = True
		self.value = value
		self.parent = parent

	def add_node(self, node):
		self.branches.append(node)
		self.is_leaf = False

	def set_value(self, value):
		self.value = value

	def clean(self):
		num_deleted = 0
		for i, branch in enumerate(self.branches.copy()):
			if branch.is_leaf:
				if branch.value[0] not in jisho:
					del self.branches[i-num_deleted]
					num_deleted += 1
			else:
				branch.clean()

	def __str__(self, level=0): 
		indent = "  " * level
		if self.value is None:
			node_repr = "<empty>"
		else:
			word, conj = self.value
			node_repr = f"{word} [{conj}]" if conj else word
		result = indent + node_repr + "\n"
		for branch in self.branches:
			result += branch.__str__(level + 1)
		return result

def deconjugate(word, last_conjugation=None, depth=0, parent=None):

	if depth > 10:
		return Tree((word, last_conjugation))

	godan = godan_deconjugatable.search(word)
	ichidan = ichidan_deconjugatable.search(word) 
	suru = suru_deconjugatable.search(word)
	kuru = kuru_deconjugatable.search(word)
	te = deconjugate_te(word)

	if not (godan or ichidan or te or suru or kuru):
		return Tree((word, last_conjugation))

	tree = Tree((word, last_conjugation))
	if depth == 0:
		parent = tree

	if godan:
		for c in a_conj:
			changed_index = len(word)-len(c)-1
			changed_letter = word[changed_index]
			if word.endswith(c) and changed_letter in a_:
				new_word = word[:changed_index] + u_[a_.index(changed_letter)]
				if word in jisho:
					parent.add_node(Tree((word, None)))
				tree.add_node(deconjugate(new_word, c, depth+1, tree))

		for c in i_conj:
			changed_index = len(word)-len(c)-1
			changed_letter = word[changed_index]
			if word.endswith(c) and changed_letter in i_:
				new_word = word[:changed_index] + u_[i_.index(changed_letter)]
				if word in jisho:
					parent.add_node(Tree((word, None)))
				tree.add_node(deconjugate(new_word, c, depth+1, tree))

		for c in u_conj:
			changed_index = len(word)-len(c)-1
			changed_letter = word[changed_index]
			if word.endswith(c) and changed_letter in u_:
				new_word = word[:changed_index] + u_[u_.index(changed_letter)]
				if word in jisho:
					parent.add_node(Tree((word, None)))
				tree.add_node(deconjugate(new_word, c, depth+1, tree))

		for c in e_conj:
			changed_index = len(word)-len(c)-1
			changed_letter = word[changed_index]
			if word.endswith(c) and changed_letter in e_:
				new_word = word[:changed_index] + u_[e_.index(changed_letter)]
				if word in jisho:
					parent.add_node(Tree((word, None)))
				tree.add_node(deconjugate(new_word, c, depth+1, tree))

		for c in o_conj:
			changed_index = len(word)-len(c)-1
			changed_letter = word[changed_index]
			if word.endswith(c) and changed_letter in o_:
				new_word = word[:changed_index] + u_[o_.index(changed_letter)]
				if word in jisho:
					parent.add_node(Tree((word, None)))
				tree.add_node(deconjugate(new_word, c, depth+1, tree))

	if ichidan:
		for c in a_conj_ichidan:
			changed_index = len(word)-len(c)-1
			changed_letter = word[changed_index]
			if word.endswith(c) and (changed_letter in i_ or changed_letter in e_):
				new_word = word[:changed_index+1] + "る"
				if word in jisho:
					parent.add_node(Tree((word, None)))
				tree.add_node(deconjugate(new_word, c, depth+1, tree))
				

		for c in i_conj:

			changed_index = len(word)-len(c)-1
			changed_letter = word[changed_index]
			
			if word.endswith(c) and (changed_letter in i_ or changed_letter in e_):
				if len(word) > 2:
					if word[changed_index-1] == "な":
						continue
				new_word = word[:changed_index+1] + "る"
				if word in jisho:
					parent.add_node(Tree((word, None)))
				print(new_word)
				tree.add_node(deconjugate(new_word, c, depth+1, tree))
				
		for c in u_conj:
			changed_index = len(word)-len(c)-1
			changed_letter = word[changed_index]
			if word.endswith(c) and (changed_letter in i_ or changed_letter in e_):
				new_word = word[:changed_index+1] + "る"
				if word in jisho:
					parent.add_node(Tree((word, None)))
				tree.add_node(deconjugate(new_word, c, depth+1, tree))
				
		for c in e_conj_ichidan:
			changed_index = len(word)-len(c)-1
			changed_letter = word[changed_index]
			if word.endswith(c) and (changed_letter in i_ or changed_letter in e_):
				new_word = word[:changed_index+1] + "る"
				if word in jisho:
					parent.add_node(Tree((word, None)))
				tree.add_node(deconjugate(new_word, c, depth+1, tree))	

		for c in o_conj:
			changed_index = len(word)-len(c)-1
			changed_letter = word[changed_index]
			if word.endswith(c) and (changed_letter in i_ or changed_letter in e_):
				new_word = word[:changed_index+1] + "る"
				if word in jisho:
					parent.add_node(Tree((word, None)))
				tree.add_node(deconjugate(new_word, c, depth+1, tree))
								
	if suru:
		for c in suru_conjugations:

			changed_index = len(word)-len(c)-1
			changed_letter = word[changed_index]

			if word.endswith(c):
				new_word = word[:changed_index+1] + "する"
				if word in jisho:
					parent.add_node(Tree((word, None)))
				tree.add_node(deconjugate(new_word, c, depth+1, tree))

	if kuru:
		print(0, kuru)
		for c in kuru_conjugations:

			changed_index = len(word)-len(c)-1
			changed_letter = word[changed_index]
			
			if word.endswith(c):
				new_word = word[:changed_index+1] + "くる"
				if word in jisho:
					parent.add_node(Tree((word, None)))
				tree.add_node(deconjugate(new_word, c, depth+1, tree))

	if te:
		for option in te:
			tree.add_node(deconjugate(option, "て", depth+1))


	if depth == 0:
		tree.clean()

	return tree

print(deconjugate(word))

