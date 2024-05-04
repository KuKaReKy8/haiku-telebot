from random import choices, choice


class HaikuM():
    def __init__(self):
        pass

    def make_haiku(self):
        with open('static/1_3.txt', 'r', encoding='utf-8') as lines1_3:
            line1_3 = choices(lines1_3.readlines(), k=2)
        with open('static/2.txt', 'r', encoding='utf-8') as lines2:
            line2 = choice(lines2.readlines())
        return f'{line1_3[0].capitalize()}{line2.capitalize()}{line1_3[1].capitalize()}'


if __name__ == '__main__':
    creator = HaikuM()
    print(creator.make_haiku())

