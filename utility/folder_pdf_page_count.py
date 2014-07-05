#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import re
import os
import json

folder_path = 'FOLDER PATH'
rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE | re.DOTALL)


def main():
    os.chdir(folder_path)
    ordered_cards = ordered_list(get_report_cards(get_filenames()))
    over_four = over_four_pages(ordered_cards)
    under_five = under_five_pages(ordered_cards)

    print "\n{} rc's over 4 pages:".format(len(over_four))
    for c in over_four:
        print c
        
    print "\n\n{} rc's under 5 pages.".format(len(under_five))
    # for c in under_five:
    #     print c


def ordered_list(unordered):
    ordered = []
    while len(unordered) > 0:
        # find highest remaining in unordered
        highest = unordered[0]
        for i in unordered:
            if i.compare(highest) > 1:
                highest = i
        ordered.append(highest)
        unordered.remove(highest)
    return ordered


def get_report_cards(filenames):
    all_cards = []
    for filename in filenames:
        all_cards.append(LongReportCard(filename, count_pages(filename)))
    return all_cards


def under_five_pages(cards):
    under_four_pages = []
    for card in cards:
        if card.length < 5:
            under_four_pages.append(card)
    return under_four_pages


def over_four_pages(cards):
    over_four_pages = []
    for card in cards:
        if card.length > 4:
            over_four_pages.append(card)
    return over_four_pages


def get_filenames():
    for root, dirs, files in os.walk(folder_path):
        return files


def count_pages(filename):
    data = file(filename, 'rb').read()
    return len(rxcountpages.findall(data))


class LongReportCard(object):
    def __init__(self, filename, length):
        self.name = self.get_filename(filename)
        self.length = length

    def __str__(self):
        return "{}: {} pp".format(self.name, self.length)


    def get_filename(self, name):
        name = os.path.splitext(name)[0]
        name = name[name.find('-') + 1:]
        return name.strip()
    
    def compare(self, other):
        if other.length > self.length:
            return -1
        elif other.length == self.length:
            return 0
        else:
            return 1


if __name__ == '__main__':
    main()
