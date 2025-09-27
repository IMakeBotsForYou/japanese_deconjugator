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
    "れる": {"name": "受け身", "type": "5-a"},
    "せる": {"name": "使役", "type": "5-a"},
    "ない": {"name": "打ち消し", "type": "5-a"},
    "む": {"name": "打ち消し・助動詞 む(ん)", "type": "5-a"},
    "ん": {"name": "打ち消し・助動詞 む(ん)", "type": "5-a"},
}

a_conj_ichidan = {
    "られる": {"name": "受け身・可能", "type": "1-a"},
    "させる": {"name": "使役", "type": "1-a"},
    "ない": {"name": "打ち消し", "type": "1-a"},
    "む": {"name": "打ち消し・助動詞 む(ん)", "type": "1-a"},
    "ん": {"name": "打ち消し・助動詞 む(ん)", "type": "1-a"},
}

i_conj = {
    "": {"name": "連用形", "type": "5-i"},
    "たい": {"name": "希望", "type": "5-i"},
    "ます": {"name": "丁寧", "type": "5-i"},
    "にくい": {"name": "難易", "type": "5-i"},
    "がたい": {"name": "難易", "type": "5-i"},
    "づらい": {"name": "難易", "type": "5-i"},
    "やすい": {"name": "難易", "type": "5-i"},
    "始める": {"name": "補助動詞 始める", "type": "5-i"},
    "はじめる": {"name": "補助動詞 はじめる", "type": "5-i"},
    "出す": {"name": "補助動詞 出す", "type": "5-i"},
    "だす": {"name": "補助動詞 だす", "type": "5-i"},
    "続ける": {"name": "補助動詞 続ける", "type": "5-i"},
    "つづける": {"name": "補助動詞 つづける", "type": "5-i"},
    "終わる": {"name": "補助動詞 終わる", "type": "5-i"},
    "おわる": {"name": "補助動詞 おわる", "type": "5-i"},
    "かける": {"name": "補助動詞 かける", "type": "5-i"},
    "込む": {"name": "補助動詞 込む", "type": "5-i"},
    "こむ": {"name": "補助動詞 こむ", "type": "5-i"},
    "直す": {"name": "補助動詞 直す", "type": "5-i"},
    "なおす": {"name": "補助動詞 なおす", "type": "5-i"},
    "合う": {"name": "補助動詞 合う", "type": "5-i"},
    "あう": {"name": "補助動詞 あう", "type": "5-i"},
    "過ぎる": {"name": "補助動詞 過ぎる", "type": "5-i"},
    "すぎる": {"name": "補助動詞 すぎる", "type": "5-i"},
    "返す": {"name": "補助動詞 返す", "type": "5-i"},
    "かえす": {"name": "補助動詞 かえす", "type": "5-i"},
    "抜く": {"name": "補助動詞 抜く", "type": "5-i"},
    "ぬく": {"name": "補助動詞 ぬく", "type": "5-i"},
    "続く": {"name": "補助動詞 続く", "type": "5-i"},
    "つづく": {"name": "補助動詞 つづく", "type": "5-i"},
    "切る": {"name": "補助動詞 切る", "type": "5-i"},
    "きる": {"name": "補助動詞 きる", "type": "5-i"},
    "し": {"name": "助動詞 し(古文)", "type": "5-i"},
    "き": {"name": "助動詞 き(古文)", "type": "5-i"},
}

u_conj = {"な": {"name": "禁止", "type": "5-u"}}

e_conj = {
    "": {"name": "命令形", "type": "5-e"},
    "る": {"name": "可能形", "type": "5-e"},
    "ば": {"name": "仮定形", "type": "5-e"},
}

e_conj_ichidan = {
    "": {"name": "連用形", "type": "1-e"},
    "ろ": {"name": "命令形", "type": "1-e"},
    "たい": {"name": "希望", "type": "1-e"},
    "ます": {"name": "丁寧", "type": "1-e"},
    "にくい": {"name": "難易", "type": "1-e"},
    "がたい": {"name": "難易", "type": "1-e"},
    "づらい": {"name": "難易", "type": "1-e"},
    "やすい": {"name": "難易", "type": "1-e"},
    "始める": {"name": "補助動詞 始める", "type": "1-e"},
    "はじめる": {"name": "補助動詞 はじめる", "type": "1-e"},
    "出す": {"name": "補助動詞 出す", "type": "1-e"},
    "だす": {"name": "補助動詞 だす", "type": "1-e"},
    "続ける": {"name": "補助動詞 続ける", "type": "1-e"},
    "つづける": {"name": "補助動詞 つづける", "type": "1-e"},
    "終わる": {"name": "補助動詞 終わる", "type": "1-e"},
    "おわる": {"name": "補助動詞 おわる", "type": "1-e"},
    "かける": {"name": "補助動詞 かける", "type": "1-e"},
    "込む": {"name": "補助動詞 込む", "type": "1-e"},
    "こむ": {"name": "補助動詞 こむ", "type": "1-e"},
    "直す": {"name": "補助動詞 直す", "type": "1-e"},
    "なおす": {"name": "補助動詞 なおす", "type": "1-e"},
    "合う": {"name": "補助動詞 合う", "type": "1-e"},
    "あう": {"name": "補助動詞 あう", "type": "1-e"},
    "過ぎる": {"name": "補助動詞 過ぎる", "type": "1-e"},
    "すぎる": {"name": "補助動詞 すぎる", "type": "1-e"},
    "返す": {"name": "補助動詞 返す", "type": "1-e"},
    "かえす": {"name": "補助動詞 かえす", "type": "1-e"},
    "抜く": {"name": "補助動詞 抜く", "type": "1-e"},
    "ぬく": {"name": "補助動詞 ぬく", "type": "1-e"},
    "続く": {"name": "補助動詞 続く", "type": "1-e"},
    "つづく": {"name": "補助動詞 つづく", "type": "1-e"},
    "切る": {"name": "補助動詞 切る", "type": "1-e"},
    "きる": {"name": "補助動詞 きる", "type": "1-e"},
    "し": {"name": "助動詞 し(古文)", "type": "1-e"},
    "き": {"name": "助動詞 き(古文)", "type": "1-e"},
}

o_conj = {"う": {"name": "意向", "type": "5-o"}}

o_conj_ichidan = {"よう": {"name": "意向", "type": "1-o"}}

i_adj_conjugations = {
    "かった": {"return-options": ["い"], "name": "過去形", "type": "adj-i"},
    "くて": {"return-options": ["い"], "name": "連用形・て形", "type": "adj-i"},
    "くない": {"return-options": ["い"], "name": "打ち消し", "type": "adj-i"},
    "くなる": {"return-options": ["く"], "name": "副動詞 なる", "type": "adj-i"},
    "くする": {"return-options": ["く"], "name": "副動詞 する", "type": "adj-i"},
    "く": {"return-options": ["い"], "name": "連用形", "type": "adj-i"},
    "よく": {"return-options": ["よい", "いい"], "name": "連用形", "type": "adj-i"},
    "き": {"return-options": ["い"], "name": "連体形(古文)", "type": "adj-i"},
    "し": {"return-options": ["い"], "name": "終止形(古文)", "type": "adj-i"},
    "かろう": {"return-options": ["い"], "name": "意向", "type": "adj-i"},
    "からぬ": {"return-options": ["い"], "name": "打ち消し・連用形", "type": "adj-i"},
    "からず": {"return-options": ["い"], "name": "打ち消し", "type": "adj-i"},
    "過ぎる": {"return-options": [""], "name": "副動詞 過ぎる", "type": "adj-i"},
    "すぎる": {"return-options": [""], "name": "副動詞 すぎる", "type": "adj-i"},
}

na_adj_conjugations = {
    "な": {"return-options": [""], "name": "連体形", "type": "adj-na"},
    "じゃない": {"return-options": [""], "name": "打ち消し", "type": "adj-na"},
    "だった": {"return-options": [""], "name": "過去形", "type": "adj-na"},
    "だ": {"return-options": [""], "name": "終止形", "type": "adj-na"},
    "に": {"return-options": [""], "name": "連用形", "type": "adj-na"},
    "の": {"return-options": [""], "name": "連体形", "type": "adj-na"},
    "と": {"return-options": [""], "name": "引用", "type": "adj-na"},
    "になる": {"return-options": [""], "name": "副動詞 なる", "type": "adj-na"},
    "にする": {"return-options": [""], "name": "副動詞 する", "type": "adj-na"},
    "過ぎる": {"return-options": [""], "name": "副動詞 過ぎる", "type": "adj-na"},
    "すぎる": {"return-options": [""], "name": "副動詞 すぎる", "type": "adj-na"},
}

masu_conjugations = {
    "ません": {"return-options": ["ます"], "name": "打ち消し", "type": "masu"},
    "ました": {"return-options": ["ます"], "name": "過去形", "type": "masu"},
    "ませんでした": {"return-options": ["ません"], "name": "過去形", "type": "masu"},
    "まして": {"return-options": ["ます"], "name": "連用形", "type": "masu"},
    "まし": {
        "return-options": ["ます"],
        "name": "連用形",
        "type": "masu",
    },  # キモいけどね
}

suru_conjugations = {
    "させる": {"return-options": ["する"], "name": "使役", "type": "suru"},
    "される": {"return-options": ["する"], "name": "受け身", "type": "suru"},
    "しない": {"return-options": ["する"], "name": "打ち消し", "type": "suru"},
    "したい": {"return-options": ["する"], "name": "希望", "type": "suru"},
    "します": {"return-options": ["する"], "name": "丁寧", "type": "suru"},
    "するな": {"return-options": ["する"], "name": "禁止", "type": "suru"},
    "できる": {"return-options": ["する"], "name": "可能", "type": "suru"},
    "しろ": {"return-options": ["する"], "name": "命令", "type": "suru"},
    "しよう": {"return-options": ["する"], "name": "意向", "type": "suru"},
}

kuru_conjugations = {
    # Kanji forms
    "来させる": {"return-options": ["来る"], "name": "使役", "type": "kuru"},
    "来ない": {"return-options": ["来る"], "name": "打ち消し", "type": "kuru"},
    "来られる": {"return-options": ["来る"], "name": "受け身・可能", "type": "kuru"},
    "来たい": {"return-options": ["来る"], "name": "希望", "type": "kuru"},
    "来ます": {"return-options": ["来る"], "name": "丁寧", "type": "kuru"},
    "来るな": {"return-options": ["来る"], "name": "禁止", "type": "kuru"},
    "来い": {"return-options": ["来る"], "name": "命令", "type": "kuru"},
    "来よう": {"return-options": ["来る"], "name": "意向", "type": "kuru"},
    # Hiragana forms
    "こさせる": {"return-options": ["くる"], "name": "使役", "type": "kuru"},
    "こない": {"return-options": ["くる"], "name": "打ち消し", "type": "kuru"},
    "こられる": {"return-options": ["くる"], "name": "受け身・可能", "type": "kuru"},
    "きたい": {"return-options": ["くる"], "name": "希望", "type": "kuru"},
    "きます": {"return-options": ["くる"], "name": "丁寧", "type": "kuru"},
    "くるな": {"return-options": ["くる"], "name": "禁止", "type": "kuru"},
    "こい": {"return-options": ["くる"], "name": "命令", "type": "kuru"},
    "こよう": {"return-options": ["くる"], "name": "意向", "type": "kuru"},
}

te_deconjugations = {
    # Special irregular verbs
    "乞うて": {"return-options": ["乞う"], "name": "テ形 (特殊)", "type": "5-te-irr"},
    "こうて": {"return-options": ["こう"], "name": "テ形 (特殊)", "type": "5-te-irr"},
    "問うて": {"return-options": ["問う"], "name": "テ形 (特殊)", "type": "5-te-irr"},
    "とうて": {"return-options": ["とう"], "name": "テ形 (特殊)", "type": "5-te-irr"},
    "厭うて": {"return-options": ["厭う"], "name": "テ形 (特殊)", "type": "5-te-irr"},
    "いとうて": {
        "return-options": ["いとう"],
        "name": "テ形 (特殊)",
        "type": "5-te-irr",
    },
    "宣うて": {"return-options": ["宣う"], "name": "テ形 (特殊)", "type": "5-te-irr"},
    "曰うて": {"return-options": ["曰う"], "name": "テ形 (特殊)", "type": "5-te-irr"},
    "のたまうて": {
        "return-options": ["のたまう"],
        "name": "テ形 (特殊)",
        "type": "5-te-irr",
    },
    # 補助動詞・複合
    "て見る": {"return-options": ["て"], "name": "補助動詞 見る", "type": "te-aux"},
    "てみる": {"return-options": ["て"], "name": "補助動詞 みる", "type": "te-aux"},
    "で見る": {"return-options": ["て"], "name": "補助動詞 見る", "type": "te-aux"},
    "でみる": {"return-options": ["て"], "name": "補助動詞 みる", "type": "te-aux"},
    "て居る": {"return-options": ["て"], "name": "補助動詞 居る", "type": "te-aux"},
    "ている": {"return-options": ["て"], "name": "補助動詞 いる", "type": "te-aux"},
    "ておる": {"return-options": ["て"], "name": "補助動詞 おる", "type": "te-aux"},
    "で居る": {"return-options": ["て"], "name": "補助動詞 居る", "type": "te-aux"},
    "でいる": {"return-options": ["て"], "name": "補助動詞 いる", "type": "te-aux"},
    "でおる": {"return-options": ["て"], "name": "補助動詞 おる", "type": "te-aux"},
    "て在る": {"return-options": ["て"], "name": "補助動詞 在る", "type": "te-aux"},
    "てある": {"return-options": ["て"], "name": "補助動詞 ある", "type": "te-aux"},
    "て置く": {"return-options": ["て"], "name": "補助動詞 置く", "type": "te-aux"},
    "ておく": {"return-options": ["て"], "name": "補助動詞 おく", "type": "te-aux"},
    "で置く": {"return-options": ["で"], "name": "補助動詞 置く", "type": "te-aux"},
    "でおく": {"return-options": ["で"], "name": "補助動詞 おく", "type": "te-aux"},
    "とく": {
        "return-options": ["て"],
        "name": "補助動詞 おく (縮約形)",
        "type": "te-aux",
    },
    "どく": {
        "return-options": ["て"],
        "name": "補助動詞 おく (縮約形)",
        "type": "te-aux",
    },
    "て仕舞う": {"return-options": ["て"], "name": "補助動詞 仕舞う", "type": "te-aux"},
    "で仕舞う": {"return-options": ["で"], "name": "補助動詞 仕舞う", "type": "te-aux"},
    "て終う": {"return-options": ["て"], "name": "補助動詞 終う", "type": "te-aux"},
    "で終う": {"return-options": ["で"], "name": "補助動詞 終う", "type": "te-aux"},
    "て了う": {"return-options": ["て"], "name": "補助動詞 了う", "type": "te-aux"},
    "で了う": {"return-options": ["で"], "name": "補助動詞 了う", "type": "te-aux"},
    "てしまう": {"return-options": ["て"], "name": "補助動詞 しまう", "type": "te-aux"},
    "でしまう": {"return-options": ["で"], "name": "補助動詞 しまう", "type": "te-aux"},
    "ちゃう": {
        "return-options": ["て"],
        "name": "補助動詞 しまう (縮約形)",
        "type": "te-aux",
    },
    "じゃう": {
        "return-options": ["て"],
        "name": "補助動詞 しまう (縮約形)",
        "type": "te-aux",
    },
    "ちまう": {
        "return-options": ["て"],
        "name": "補助動詞 しまう (縮約形)",
        "type": "te-aux",
    },
    "じまう": {
        "return-options": ["で"],
        "name": "補助動詞 しまう (縮約形)",
        "type": "te-aux",
    },
    "て来る": {"return-options": ["て"], "name": "補助動詞 来る", "type": "te-aux"},
    "てくる": {"return-options": ["て"], "name": "補助動詞 くる", "type": "te-aux"},
    "で来る": {"return-options": ["で"], "name": "補助動詞 来る", "type": "te-aux"},
    "でくる": {"return-options": ["で"], "name": "補助動詞 くる", "type": "te-aux"},
    "て行く": {"return-options": ["て"], "name": "補助動詞 行く", "type": "te-aux"},
    "ていく": {"return-options": ["て"], "name": "補助動詞 行く", "type": "te-aux"},
    "で行く": {"return-options": ["で"], "name": "補助動詞 行く", "type": "te-aux"},
    "でいく": {"return-options": ["で"], "name": "補助動詞 行く", "type": "te-aux"},
    "て呉れる": {"return-options": ["て"], "name": "補助動詞 呉れる", "type": "te-aux"},
    "てくれる": {"return-options": ["て"], "name": "補助動詞 くれる", "type": "te-aux"},
    "で呉れる": {"return-options": ["で"], "name": "補助動詞 呉れる", "type": "te-aux"},
    "でくれる": {"return-options": ["で"], "name": "補助動詞 くれる", "type": "te-aux"},
    "て遣る": {"return-options": ["て"], "name": "補助動詞 遣る", "type": "te-aux"},
    "てやる": {"return-options": ["て"], "name": "補助動詞 やる", "type": "te-aux"},
    "で遣る": {"return-options": ["で"], "name": "補助動詞 遣る", "type": "te-aux"},
    "でやる": {"return-options": ["で"], "name": "補助動詞 やる", "type": "te-aux"},
    "てもらう": {"return-options": ["て"], "name": "補助動詞 もらう", "type": "te-aux"},
    "て貰う": {"return-options": ["て"], "name": "補助動詞 貰う", "type": "te-aux"},
    "でもらう": {"return-options": ["で"], "name": "補助動詞 もらう", "type": "te-aux"},
    "で貰う": {"return-options": ["で"], "name": "補助動詞 貰う", "type": "te-aux"},
    "て頂く": {"return-options": ["て"], "name": "補助動詞 頂く", "type": "te-aux"},
    "ていただく": {
        "return-options": ["て"],
        "name": "補助動詞 いただく",
        "type": "te-aux",
    },
    "で頂く": {"return-options": ["で"], "name": "補助動詞 頂く", "type": "te-aux"},
    "でいただく": {
        "return-options": ["で"],
        "name": "補助動詞 いただく",
        "type": "te-aux",
    },
    # Irregular 行く・来る
    "行って": {"return-options": ["行く"], "name": "テ形 (行く)", "type": "5-te"},
    "いって": {"return-options": ["いく"], "name": "テ形 (行く)", "type": "5-te"},
    "来て": {"return-options": ["来る"], "name": "テ形 (来る)", "type": "kuru-te"},
    "きて": {"return-options": ["くる"], "name": "テ形 (くる)", "type": "kuru-te"},
    # Regular sound-change groups
    "って": {"return-options": ["う", "つ", "る"], "name": "テ形", "type": "5-te"},
    "いて": {"return-options": ["く"], "name": "テ形", "type": "5-te"},
    "いで": {"return-options": ["いる", "ぐ"], "name": "テ形", "type": "5-te"},
    "んで": {"return-options": ["む", "ぬ", "ぶ"], "name": "テ形", "type": "5-te"},
    "して": {"return-options": ["する", "す"], "name": "テ形", "type": "5/suru-te"},
    "て": {"return-options": ["る"], "name": "テ形", "type": "1-te"},
}

past_deconjugations = {
    "乞うた": {"return-options": ["乞う"], "name": "過去形", "type": "5-ta"},
    "こうた": {"return-options": ["こう"], "name": "過去形", "type": "5-ta"},
    "問うた": {"return-options": ["問う"], "name": "過去形", "type": "5-ta"},
    "とうた": {"return-options": ["とう"], "name": "過去形", "type": "5-ta"},
    "厭うた": {"return-options": ["厭う"], "name": "過去形", "type": "5-ta"},
    "いとうた": {"return-options": ["いとう"], "name": "過去形", "type": "5-ta"},
    "宣うた": {"return-options": ["宣う"], "name": "過去形", "type": "5-ta"},
    "曰うた": {"return-options": ["曰う"], "name": "過去形", "type": "5-ta"},
    "のたまうた": {"return-options": ["のたまう"], "name": "過去形", "type": "5-ta"},
    "きた": {"return-options": ["くる", "きる"], "name": "過去形", "type": "kuru-ta"},
    "来た": {"return-options": ["くる"], "name": "過去形", "type": "kuru-ta"},
    "行った": {"return-options": ["行く"], "name": "過去形", "type": "5-ta"},
    "いった": {
        "return-options": ["いう", "いく", "いる", "いつ"],
        "name": "過去形",
        "type": "5-ta",
    },
    "した": {"return-options": ["する", "す"], "name": "過去形", "type": "5/suru-ta"},
    "った": {"return-options": ["う", "る", "つ"], "name": "過去形", "type": "5-ta"},
    "いた": {"return-options": ["く"], "name": "過去形", "type": "5-ta"},
    "いだ": {"return-options": ["ぐ"], "name": "過去形", "type": "5-ta"},
    "んだ": {"return-options": ["む", "ぬ", "ぶ"], "name": "過去形", "type": "5-ta"},
    "た": {"return-options": ["る"], "name": "過去形", "type": "1-ta"},
}

possible_routes = {
    # After a 使役 conjugation, we get a ～(さ)せる verb, which is always ichidan
    # This means it can get any 1(ichidan) conjugation after, or 補助動詞-te, like
    # ~(さ)せ[てくれる].
    # Same for 受け身(godan), or 受け身・可能(ichidan)
    # Example: 遊ばれる・食べられる・される・こられる result is always ichidan
    # Currently it is in a "conj_name": [options from now] format.
    # However, I am using a name-type duo system.
    # I want it in a format like so:
    # ""
    #
    #
    #
    "使役": ["1", "補助動詞"],
    "受け身": ["1", "補助動詞"],
    "可能": ["1", "補助動詞"],
    "受け身・可能": ["1", "補助動詞"],
    # all end in い
    "打ち消し": ["adj-i"],
    "希望": ["adj-i"],
    "難易": ["adj-i"],
    # This does not include ~くて for adjectives
    "テ形": ["補助動詞-te"],
    # ichidan te-aux-verbs
    # ~てすぎる can only now take ichidan conjugations,
    # seeing as すぎる is ichidan.
    "副動詞 過ぎる": ["1", "補助動詞-te"],
    "副動詞 すぎる": ["1", "補助動詞-te"],
    "副動詞 する": ["suru", "補助動詞-te"],
    "副動詞 なる": ["5", "補助動詞-te"],
    "補助動詞 見る": ["1", "補助動詞-te"],
    "補助動詞 みる": ["1", "補助動詞-te"],
    "補助動詞 居る": ["1", "補助動詞-te"],
    "補助動詞 いる": ["1", "補助動詞-te"],
    "補助動詞 呉れる": ["1", "補助動詞-te"],
    "補助動詞 くれる": ["1", "補助動詞-te"],
    # godan te-aux-verbs
    "補助動詞 おる": ["5", "補助動詞-te"],
    "補助動詞 在る": ["5", "補助動詞-te"],
    "補助動詞 ある": ["5", "補助動詞-te"],
    "補助動詞 置く": ["5", "補助動詞-te"],
    "補助動詞 おく": ["5", "補助動詞-te"],
    "補助動詞 おく (縮約形)": ["5", "補助動詞-te"],
    "補助動詞 仕舞う": ["5", "補助動詞-te"],
    "補助動詞 終う": ["5", "補助動詞-te"],
    "補助動詞 了う": ["5", "補助動詞-te"],
    "補助動詞 しまう": ["5", "補助動詞-te"],
    "補助動詞 しまう (縮約形)": ["5", "補助動詞-te"],
    "補助動詞 遣る": ["5", "補助動詞-te"],
    "補助動詞 やる": ["5", "補助動詞-te"],
    "補助動詞 もらう": ["5", "補助動詞-te"],
    "補助動詞 貰う": ["5", "補助動詞-te"],
    "補助動詞 頂く": ["5", "補助動詞-te"],
    "補助動詞 いただく": ["5", "補助動詞-te"],
    # irr te-aux-verbs
    "補助動詞 来る": ["kuru", "te-kuru", "補助動詞-te"],
    "補助動詞 くる": ["kuru", "te-kuru", "補助動詞-te"],
    "補助動詞 行く": ["5", "te-iku", "補助動詞-te"],
    "補助動詞 いく": ["5", "te-iku", "補助動詞-te"],
    "丁寧": ["masu"],
}
