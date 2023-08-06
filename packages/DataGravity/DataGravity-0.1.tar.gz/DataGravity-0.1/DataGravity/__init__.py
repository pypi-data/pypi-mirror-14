import csv

def read(dgexport):
    with open(dgexport, 'r') as f:
        reader = csv.reader(f)
        read_list = list(reader)
    master_list = read_list[1:len(read_list)]
    return master_list

def analyze(list_slice, selection):
    elements = []
    if selection == 'share_id':
        y = 0
        for x in list_slice:
            elements.append(x[y])
        elements_s = sorted(set(elements))
        return elements_s
    elif selection == 'owner':
        y = 1
        for x in list_slice:
            elements.append(x[y])
        elements_s = sorted(set(elements))
        return elements_s
    elif selection == 'lastmodtime':
        y = 2
        for x in list_slice:
            elements.append(x[y])
        elements_s = sorted(set(elements))
        return elements_s
    elif selection == 'mimetype':
        y = 3
        for x in list_slice:
            elements.append(x[y])
        elements_s = sorted(set(elements))
        return elements_s
    elif selection == 'tags':
        y = 4
        for x in list_slice:
            elements.append(x[y])
        elements_s = sorted(set(elements))
        return elements_s
    elif selection == 'size':
        y = 5
        for x in list_slice:
            elements.append(x[y])
        elements_s = sorted(set(elements))
        return elements_s
    elif selection == 'contentstate':
        y = 6
        for x in list_slice:
            elements.append(x[y])
        elements_s = sorted(set(elements))
        return elements_s
    elif selection == 'filepath':
        y = 7
        for x in list_slice:
            elements.append(x[y])
        elements_s = sorted(set(elements))
        return elements_s
    elif selection == 'filename':
        y = 7
        for x in list_slice:
            elements.append(x[y].split("/")[-1])
        elements_s = sorted(set(elements))
        return elements_s
    elif selection == 'fingerprint':
        y = 8
        for x in list_slice:
            elements.append(x[y])
        elements_s = sorted(set(elements))
        return elements_s
    elif selection == 'createdtime':
        y = 9
        for x in list_slice:
            elements.append(x[y])
        elements_s = sorted(set(elements))
        return elements_s
    else: print("Invalid column name")
