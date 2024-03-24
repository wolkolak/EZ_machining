import os

def strings_count(directory: str, forbid: list):# -> Iterable[tuple]:
    for root, dirs, files in os.walk(directory):
        for file in files:
            count = 0
            you_can = True

            for f in forbid:
                if root.startswith(f):
                    you_can = False

            if os.path.join(root, file).endswith('.py') and you_can:
                curr_file = open(os.path.join(root, file), 'r', encoding='utf-8')
                for line in curr_file.readlines():
                    if not (line == '\n' or line.strip().startswith(('"', '#', "'"))):
                        count += 1
                #print('Файл "{}": строк кода - {}'.format(os.path.join(root, file), count))
                yield os.path.join(root, file), count



def setting_recive(project_name, forbidden_list):
    sum = 0
    len_p = len(project_name)
    itog = os.getcwd()
    k1 = itog.index(project_name)
    k2 = k1 + len_p
    print(itog[:k2])
    forbidden_list = [itog[:k2] + '\\' + ff for ff in forbidden_list ]
    for element in strings_count(directory=itog[:k2], forbid=forbidden_list):
        sum = sum + int(element[1])
    print('Итого = ', sum)

setting_recive(project_name = 'EZ_machining-master', forbidden_list=['build', 'venv'])






