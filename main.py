import threading
from pathlib import Path

lock = threading.Lock()
shared_dict = {}

def find_word_thread(locker, file: str, word: str):
    global shared_dict
    formated_word: str = word.strip()
    with open(Path(file)) as f:
        text = f.readlines()
        for line in text:
            if formated_word in line:
                with locker:
                    if formated_word in shared_dict.keys():
                        shared_dict[f"{formated_word}"] = [*shared_dict.get(formated_word), file]
                    else:
                        shared_dict[f"{formated_word}"] = [file]
                    print(file)
                    return

def find_word_process(file):
    pass

def main():
    text_files = ["text_1.txt", "text_2.txt", "text_3.txt", "text_4.txt", "text_5.txt"]

    threads = [threading.Thread(target=find_word_thread, args=(lock, file_name, "maximus")) for file_name in text_files]

    for t in threads: t.start()
    for t in threads: t.join()

    print(shared_dict)

if __name__ == "__main__":
    main()