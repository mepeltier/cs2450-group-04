from src.memory import Memory


def legacy_word_to_new(word: str):

    if len(word) != 5 or word[0] not in ("-", "+") or not word[1:].isdigit():
        raise ValueError("Word %s is not in legacy format", word)

    word = f"{word[0]}0{word[1:3]}0{word[3:]}"
    Memory.validate_word(word)

    return word


def convert_file(file_path: str):
    instructions = []

    with open(file_path, "r") as f:
        for line in f:
            word = line.strip()
            try:
                instruction = legacy_word_to_new(word)
                instructions.append(f"{instruction}\n")
            except ValueError as e:
                print(
                    f'Invalid instruction "{word}" in file: {file_path}\nNulling that line',
                )
                instructions.append("+000000\n")

    idx = file_path.rfind(".")
    copy_file = file_path[:idx] + " copy" + file_path[idx:]

    with open(copy_file, "w") as file:
        file.writelines(instructions)
