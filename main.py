import threading
import time
from pathlib import Path
from multiprocessing import Manager, Process

# Lock for shared resources by threading
lock = threading.Lock()
shared_dict = {}

# Function that searching word in text and add it to shared dictionary
def find_words_thread(locker, file: str, words):
    global shared_dict

    # Opening file with context manager
    try:
        with open(Path(file)) as f:
            text = f.readlines()

            # Searching the word in lines one by one and if it is there add to the dictionary
            for word in words:
                for line in text:   
                    formated_word: str = word.strip()
                    if formated_word in line:
                        with locker:
                            if formated_word in shared_dict.keys():
                                shared_dict[f"{formated_word}"] = [*shared_dict.get(formated_word), file]
                            else:
                                shared_dict[f"{formated_word}"] = [file]
                            break
    except FileNotFoundError as not_found:
        print(f"{not_found.filename} is not exist, please check name of the file!")
    except:
        print("Something went wrong, please try again!")

def find_words_process(val, file: str, words: str):

    # Opening file with context manager
    try:
        with open(Path(file)) as f:
            text = f.readlines()

            # Searching the word in lines one by one and if it is there add to the manager dictionary
            for word in words:
                for line in text:
                    formated_word: str = word.strip()
                    if formated_word in line:
                        if formated_word in val.keys():
                            val[formated_word] = [*val[formated_word], file]
                        else:
                            val[formated_word] = [file]
                        break
    except FileNotFoundError as not_found:
        print(f"{not_found.filename} is not exist, please check name of the file!")
    except:
        print("Something went wrong, please try again!")

def main():
    text_files = ["text_1.txt", "text_2.txt", "text_3.txt", "text_4.txt", "text_5.txt"]
    
    start_1 = time.perf_counter()
    # Create threads
    threads = [threading.Thread(target=find_words_thread, args=(lock, file_name, ["maximus", "sit", "fnwekrf"])) for file_name in text_files]

    for t in threads: t.start()
    for t in threads: t.join()

    end_1 = time.perf_counter()
    print(f"Time of execution: {end_1 - start_1:.5f}")

    print(shared_dict)

    start_2 = time.perf_counter()
    # Create processes
    with Manager() as manager:
        m = manager.dict()
        processes = [Process(target=find_words_process, args=(m, file_name, ["maximus", "sit"])) for file_name in text_files]
       
        for p in processes: p.start()
        for p in processes: p.join()

        end_2 = time.perf_counter()
        print(f"Time of execution: {end_2 - start_2:.5f}")

        print(m)

if __name__ == "__main__":
    main()