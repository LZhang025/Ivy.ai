#!/usr/bin/env python
# n-gram sort


from Test import ngram_counts
from nltk import ngrams
from collections import Counter
import csv

class Threshold:


    def sort(self, n_gram_quantity, x_most_frequent, output_csv_name):


        ngram_counts = Counter()

        d = {}


        # raw version # OrderedText.txt  # uncc_fin_aid.txt
        with open('uncc_financial_aid.txt') as bigtxt:
            for l in bigtxt:
                l = l.lower()
                l = l.replace('?', '')
                l = l.replace('!', '')
                l = l.replace('.', '')

                ngram_counts.update(Counter(ngrams(l.split(), n_gram_quantity)))

        print(ngram_counts.most_common(x_most_frequent))





        # non-raw version
        '''
        file = open('OrderedText.txt').read().splitlines()
        for line in file:
            #l = line.replace(line, line.capitalize())

            #l = [i[0].upper()+i[1:] for i in file]
            #l = l.capitalize()
            #l = l.replace(l, l.capitalize())
            #l = l.strip().capitalize()
            l = l.replace('?', '')
            l = l.replace('!', '')
            l = l.replace('.', '')
            l = l.replace(' i ', ' I ')


            if l:
                if l[-1] == 'i' and l[-2] == ' ':
                    l = l.replace(' i', ' I')


            ngram_counts.update(Counter(ngrams(l.split(), n_gram_quantity)))


        print(ngram_counts.most_common(x_most_frequent))
        '''










        for bigTuple in ngram_counts.most_common(x_most_frequent):
            for item in bigTuple:

                if isinstance(item, tuple):
                    currentPhrase = ''
                    for wordString in item:
                        currentPhrase += wordString + ' '

                    currentPhrase = currentPhrase.rstrip()
                    # print currentPhrase

                if isinstance(item, int):
                    # print item



                    d[currentPhrase] = item


        print d




        with open('intermediate.csv', 'wb') as intermediate:
            writer = csv.writer(intermediate)
            for key, value in d.iteritems():
                writer.writerow([key, value])

        intermediate.close()



        with open('intermediate.csv', 'r') as sample, open(output_csv_name, 'w') as out:

            reader = csv.reader(sample)
            writer = csv.writer(out)

            writer.writerows(sorted(reader, key = lambda x : int(x[1]), reverse = True))




        '''
        for bigTuple in ngram_counts.most_common(x_most_frequent):
            for item in bigTuple:
        '''

        return d





if __name__ == '__main__':
    a = Threshold()


    three = a.sort(3, 500, 'three.csv')
    four = a.sort(4, 500, 'four.csv')


    new_d = {}


    for key4 in four:
        for key3 in three:

            if (' ' + key3 + ' ') in (' ' + key4 + ' '):


                key_ratio = key3 + '/' + key4
                new_d[key_ratio] = '%.3f'%(four[key4] / float(three[key3]))

                if four[key4] > .8 * three[key3]:

                    new_d[key4] = four[key4]



    print
    print three
    print four
    print new_d












    with open('middle.csv', 'wb') as intermediate:
            writer = csv.writer(intermediate)
            for key, value in new_d.iteritems():
                #writer.writerow([key, value])

                a, b = key.split('/')
                writer.writerow([a, b, value])

    intermediate.close()



    with open('middle.csv', 'r') as sample, open('frequencies.csv', 'w') as out:

        reader = csv.reader(sample)
        writer = csv.writer(out)

        writer.writerows(sorted(reader, key = lambda x : float(x[2]), reverse = True))













