import pandas as pd
import codecs
import string
import matplotlib.pyplot as plt
import itertools

data = pd.read_csv("Words.csv")


def get_freq_dict_class1():
    return get_freq_dict(get_splited_text_class_1())


def get_freq_dict_class2():
    return get_freq_dict(get_splited_text_class_2())


def get_splited_text_class_1():
    text = " ".join(data["Text"]).replace("#", "")
    return split_text(text)


def get_splited_text_class_2():
    f = codecs.open("text_class2.txt", "r", "utf_8_sig")
    text = f.read()
    f.close()
    return split_text(text)


def split_text(text):
    split_string = text.maketrans(dict.fromkeys(string.punctuation + '«»–'))
    new_text = text.translate(split_string)
    split_arr = [x.lower() for x in new_text.split(' ') if x]
    return split_arr


def get_freq_dict(list):
    freq = {}
    for item_d in list:
        if item_d in freq:
            freq[item_d] += 1
        else:
            freq[item_d] = 1
    return {k: v for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True)}


def draw_dict_class_1():
    items = get_freq_dict_class1()
    dict_to_bar_chart(items, 'Most frequent words from text with class 1')


def draw_dict_class_2():
    items = get_freq_dict_class2()
    dict_to_bar_chart(items, 'Most frequent words from text with class 2')


def dict_to_bar_chart(info, title):
    x = []
    y = []
    first_30_items = dict(itertools.islice(info.items(), 30))
    plt.rcParams.update({'font.size': 8})

    for key in first_30_items:
        x.append(key)
        y.append(first_30_items[key])

    plt.bar(x, y, label='first')
    plt.xlabel('words')
    plt.ylabel('count')
    plt.xticks(rotation=270)
    plt.title(title, fontsize=15)
    plt.show()


def main():
    draw_dict_class_1()
    draw_dict_class_2()


if __name__ == "__main__":
    main()
