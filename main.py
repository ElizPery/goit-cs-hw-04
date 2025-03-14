import threading
from pathlib import Path
from multiprocessing import Manager, Process

# Lock for shared resources by threading
lock = threading.Lock()
shared_dict = {}

# Function that searching word in text and add it to shared dictionary
# def find_word_thread(locker, file: str, word: str):
#     global shared_dict
#     formated_word: str = word.strip()

#     # Opening file with context manager
#     with open(Path(file)) as f:
#         text = f.readlines()

#         # Searching the word in lines one by one and if it is there add to the dictionary
#         for line in text:
#             if formated_word in line:
#                 with locker:
#                     if formated_word in shared_dict.keys():
#                         shared_dict[f"{formated_word}"] = [*shared_dict.get(formated_word), file]
#                     else:
#                         shared_dict[f"{formated_word}"] = [file]
#                     print(file)
#                     return

def find_word_process(val, file: str, word: str):
    formated_word: str = word.strip()

    # Opening file with context manager
    with open(Path(file)) as f:
        text = f.readlines()

        # Searching the word in lines one by one and if it is there add to the manager dictionary
        for line in text:
            if formated_word in line:
                if formated_word in val.keys():
                    val[formated_word] = [*val[formated_word], file]
                else:
                    val[formated_word] = [file]
                return

def main():
    text_files = ["text_1.txt", "text_2.txt", "text_3.txt", "text_4.txt", "text_5.txt"]

    # Create threads
    # threads = [threading.Thread(target=find_word_thread, args=(lock, file_name, "maximus")) for file_name in text_files]

    # for t in threads: t.start()
    # for t in threads: t.join()

    # print(shared_dict)

    # Create processes
    with Manager() as manager:
        m = manager.dict()
        processes = [Process(target=find_word_process, args=(m, file_name, "maximus")) for file_name in text_files]
       
        for p in processes: p.start()
        for t in processes: t.join()

        print(m)

if __name__ == "__main__":
    main()