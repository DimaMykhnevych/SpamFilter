import pandas as pd
import codecs
import string
import matplotlib.pyplot as plt
import itertools
from collections import Counter
import math
import csv


data = pd.read_csv("Words.csv")


def get_user_input():
    print("Please, enter the text (double enter to finish the input):")
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    return ' '.join(lines)


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


def get_freq_dict(list_of_words):
    freq = {}
    for item_d in list_of_words:
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


def make_frequency_tables():
    dict_text_1 = get_freq_dict_class1()
    dict_text_2 = get_freq_dict_class2()
    write_dict_into_csv('Table_words_class_1.csv', dict_text_1)
    write_dict_into_csv('Table_words_class_2.csv', dict_text_2)


def write_dict_into_csv(file_name, dict_data):
    field_names = ['Word', 'Count']
    with open(file_name, 'w', newline='', encoding="utf-16") as f:
        wr = csv.writer(f)
        wr.writerow(field_names)
        for key in dict_data.keys():
            wr.writerow([key, dict_data[key]])


def calculate_bayes_classifier(input_text):
    input_word_arr = split_text(input_text)
    relative_class_frequency = math.log10(0.5)
    v = get_amount_of_unique_words()
    l_class_1 = len(get_splited_text_class_1())
    l_class_2 = len(get_splited_text_class_2())
    dict_class_1 = get_freq_dict_class1()
    dict_class_2 = get_freq_dict_class2()
    p_class_1 = calculate_class_probability(input_word_arr, relative_class_frequency, v, dict_class_1, l_class_1)
    p_class_2 = calculate_class_probability(input_word_arr, relative_class_frequency, v, dict_class_2, l_class_2)
    prob_class_1 = normalize_result(p_class_1, p_class_2)
    print('Probability of belonging to class 1: ', prob_class_1)
    print('Probability of belonging to class 2: ', 1-prob_class_1)


def calculate_class_probability(input_word_arr, rel_cl_freq, v, dict_class, l_class):
    res = rel_cl_freq
    for i in input_word_arr:
        p = math.log10((dict_class.get(i, 0) + 1)/(v + l_class))
        res += p
    return res


def normalize_result(value_class_1, value_class_2):
    a = math.e ** value_class_1
    b = math.e ** value_class_2
    return a/(a + b)


def get_amount_of_unique_words():
    dict_1 = Counter(get_freq_dict_class1())
    dict_2 = Counter(get_freq_dict_class2())
    return len(dict(dict_1 + dict_2))


def main():
    make_frequency_tables()
    print('Amount of words in text with class 1: ', len(get_splited_text_class_1()))
    print('Amount of words in text with class 2: ', len(get_splited_text_class_2()))
    calculate_bayes_classifier(get_user_input())
    draw_dict_class_1()
    draw_dict_class_2()


if __name__ == "__main__":
    main()
