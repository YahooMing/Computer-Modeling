import re
from collections import defaultdict
import matplotlib.pyplot as plt

def zipf(file):
    words = defaultdict(int)
    with open(file, 'r', encoding='utf-8') as txt:
        lines = txt.readlines()
        file_content = ''.join(lines)
        clean_string = re.sub('[^A-Za-z0-9]+', ' ', file_content)
        clean_string = clean_string.lower()
        #print(clean_string)
        for word in clean_string.split():
            if word not in words:
                words[word] = 1
            else:
                words[word] +=  1
        #print(dict)

    sorted_dict = dict(
        sorted(
            words.items(),
            key=lambda x: x[1],
            reverse=True)
        )
    rank = []
    frequency = []
    x = 0

    for freq in sorted_dict.values():
        x += 1
        rank.append(x)
        frequency.append(freq)

    plt.plot(rank, frequency)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Ranga")
    plt.ylabel("Częstotliwość")
    plt.title("Prawo Zipfa")
    plt.show()








if __name__ == '__main__':
    zipf('PanTadeusz.txt')