import requests
from bs4 import BeautifulSoup
import os

class Parser:
    def __init__(self):
        pass

    def file_parser(self, dir_name):
        path = f'haiku_for_parsing/{dir_name}'
        file_names = os.listdir(path)
        for file_name in file_names:
            with open(f'{path}/{file_name}', 'r', encoding='utf-8') as haiku_r:
                haiku_text = haiku_r.read()
                haiku_text = haiku_text.replace('\n\n', '\n').split('\n')
                lines2 = []
                lines1_3 = []
                for y in haiku_text:
                    print(y)
                for i in range(0, len(haiku_text), 3):
                    for j in range(3):
                        if (j + 1) % 2 == 0:
                            lines2.append(haiku_text[i + j])
                        else:
                            lines1_3.append(haiku_text[i + j])
        with open('static/1_3.txt', 'a', encoding='utf-8') as haiku_w1_3:
            for x in lines1_3:
                haiku_w1_3.write(f'{x}\n')
        with open('static/2.txt', 'a', encoding='utf-8') as haiku_w2:
            for y in lines2:
                haiku_w2.write(f"{y}\n")

    def file_withurl_parser(self, dir_name):
        path = f'haiku_for_parsing/{dir_name}'
        pages = os.listdir(path)
        for num, page_name in enumerate(pages):
            print(num)
            with open(f'{path}/{page_name}', 'r') as file:
                soup = BeautifulSoup(file, 'lxml')
                lines = soup.find('div', id = 'rules').select('b')
                lines1 = []
                for line in lines:
                    line_new = str(line)
                    print(type(line_new))
                    line_new = line_new.replace('<b>', '').replace('</b>', '').split('<br/>')
                    lines1.extend(line_new)
                print(lines1)
                lines1_3 = []
                lines2 = []
                while len(lines1) % 3 != 0:
                    lines1.pop(-1)
                for i in range(0, len(lines1), 3):
                    for j in range(3):
                        if (j + 1) % 2 == 0:
                            lines2.append(lines1[i + j])
                        else:
                            lines1_3.append(lines1[i + j])
                with open('static/1_3.txt', 'a', encoding='utf-8') as haiku_w1_3:
                    for x in lines1_3:
                        haiku_w1_3.write(f'{x}\n')
                with open('static/2.txt', 'a', encoding='utf-8') as haiku_w2:
                    for y in lines2:
                        haiku_w2.write(f"{y}\n")


if __name__ == '__main__':
    parser = Parser()
    parser.file_parser('haiku1')
    parser.file_parser('haiku2')
    for y in range(3, 8):
        parser.file_withurl_parser(f'haiku{y}')






