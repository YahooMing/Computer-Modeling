import re
from collections import defaultdict
import matplotlib.pyplot as plt

def zipf(file):
    dict = defaultdict(int)
    with open(file, 'r') as txt:
        lines = txt.readlines()
        file_content = ''.join(lines)
        clean_string = re.sub('[^A-Za-z0-9]+', ' ', file_content)
        clean_string = clean_string.lower()
        #print(clean_string)
        for word in clean_string.split():
            if word not in dict:
                dict[word] = 1
            else:
                dict[word] +=  1
        #print(dict)

    sorted_dict = sorted(dict.items(), key = lambda item: item[i], reverse = True)







if __name__ == '__main__':
    zipf('PanTadeusz.txt')