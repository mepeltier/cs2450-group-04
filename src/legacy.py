from src.memory import Memory


def legacy_word_to_new(word: str):

    if len(word) != 5 or word[0] not in ("-", "+") or not word[1:].isdigit():
        raise ValueError("Word %s is not in legacy format", word)

    word = f"{word[0]}0{word[1:3]}0{word[3:]}"
    Memory.validate_word(word)

    return word


def convert_file(file_path: str):
    errors = []
    instructions = []

    with open(file_path, "r") as f:
        for line in f:
            word = line.split()
            word = word[0]
            try:
                instruction = legacy_word_to_new(word)
                instructions.append(f"{instruction}\n")
            except ValueError as e:
                errors.append(word)
                print(
                    f'Invalid instruction "{word}" in file: {file_path}\nNulling that line',
                )
                instructions.append("+000000\n")
        instructions[-1] = instructions[-1].rstrip()

    # Create a more intuitive filename for the converted file
    idx = file_path.rfind(".")
    base_name = file_path[:idx]
    extension = file_path[idx:]
    copy_file = f"{base_name}_converted{extension}"

    with open(copy_file, "w") as file:
        file.writelines(instructions)

    if errors:
        raise ValueError(
            f"Invalid instructions '{" ".join(errors)}' in file: {file_path}. "
            f"\nThose lines have been nulled. \n\nFile saved at {copy_file}"
        )
    return copy_file
