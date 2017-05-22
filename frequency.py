import sys
from konlpy.tag import Twitter
from collections import Counter
 
 
def get_tags(text, ntags=50):
    spliter = Twitter()
    nouns = spliter.nouns(text)
    count = Counter(nouns)
    return_list = []
    for n, c in count.most_common(ntags):
        temp = {'tag': n, 'count': c}
        return_list.append(temp)
    return return_list
 
 
def get_freq():
    text_file_name = "words_log.txt"
    noun_count = 100
    output_file_name = "words_data.txt"
    open_text_file = open(text_file_name, 'r')
    text = open_text_file.read()
    tags = get_tags(text, noun_count)
    open_text_file.close()
    open_output_file = open(output_file_name, 'w')
    for tag in tags:
        noun = tag['tag']
        count = tag['count']
        open_output_file.write('{} {}\n'.format(noun, count))
    open_output_file.close()
 
 
#if __name__ == '__main__':
#    main()
