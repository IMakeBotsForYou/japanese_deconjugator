import os
import json

def operation(data, filename):
    """
    'data' is a list of entries (each entry itself is a list).
    We take: word (0), reading (1), wordtype (2).
    """
    print(f"Processing {filename} with {len(data)} items")
    new_dict = {}

    for item in data:
        if len(item) < 3:
            print(f"Skipping invalid item in {filename}: {item}")
            continue

        word = item[0]
        reading = item[1]
        wordtype = item[2]

        # Word entry: accumulate wordtypes
        if word not in new_dict:
            new_dict[word] =\ wordtype.split(" ")
        else:
            if wordtype not in new_dict[word]:
                new_dict[word].extend(wordtype.split(" "))

        new_dict[word] = [x for x in list(set(new_dict[word])) if x>"9" and x!="forms"]

        # Reading entry: overwrite with the required structure
        new_dict[reading] = new_dict[word].copy()

    return new_dict

def main():
    cwd = os.getcwd()
    merged = {}

    for file in os.listdir(cwd):
        if file.endswith(".json") and file != "jisho.json":
            filepath = os.path.join(cwd, file)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        print(f"Skipping {file}: not a list")
                        continue
                except json.JSONDecodeError:
                    print(f"Skipping {file}: invalid JSON")
                    continue

            # Run operation
            new_dict = operation(data, file)

            # Merge into global dict
            for k, v in new_dict.items():
                if k not in merged:
                    merged[k] = v
                else:
                    if isinstance(v, list) and isinstance(merged[k], list):
                        # For word entries (list of wordtypes)
                        for wt in v:
                            if wt not in merged[k]:
                                merged[k].append(wt)
                    else:
                        # For reading entries: overwrite
                        merged[k] = v

    # Save merged dictionary
    with open(os.path.join(cwd, "jisho.json"), "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"Merged {len(merged)} entries into jisho.json")

if __name__ == "__main__":
    main()
