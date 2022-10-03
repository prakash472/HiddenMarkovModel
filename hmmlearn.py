import math
import time
import sys
from collections import Counter, defaultdict

start_time=time.time()
training_path=sys.argv[1]
with open(training_path,encoding = 'UTF-8') as fp:
    text=[line.rstrip('\n') for line in fp]

# Tags realated Stuff
def calculatingTagDictionary():
    tags=[]
    for sentence in text:
        words=sentence.split(" ")
        for word in words:
            word_tags=(word.split("/")[-1])
            if word_tags!="":
                tags.append(word_tags)
    tags_dictionary=dict(Counter(tags))
    tags_dictionary["Start"]=len(text)
    tags_dictionary["End"]=len(text)
    return tags_dictionary

tags_dictionary=calculatingTagDictionary()
available_tags=list(tags_dictionary.keys())
def calculateWordTags():
    total_words_tags={}
    for sentence in text:
        words=sentence.split(" ")
        for word in words:
            word_check=word.split("/")
            word_without_tags,tags=word[:-(len(word_check[-1])+1)],word_check[-1]
            if tags !="" and word_without_tags not in total_words_tags:
                total_words_tags[word_without_tags]=set()
            total_words_tags[word_without_tags].add(tags)
    return total_words_tags

word_tag_dictionary=calculateWordTags()
vocabulary=set(word_tag_dictionary.keys())

def calculateTransmissionCount():
    transition_count={}
    for sentence in text:
        words=sentence.split(" ")
        current_state="Start"
        end_state="End"
        for word in words:
            word_check=word.split("/")
            tags=word_check[-1]
            if current_state not in transition_count:
                transition_count[current_state]={}
            if tags not in transition_count[current_state]:
                transition_count[current_state][tags]=1
            else:
                transition_count[current_state][tags]+=1
            current_state=tags
        if current_state not in transition_count:
            transition_count[current_state]={}
        if end_state not in transition_count[current_state]:
            transition_count[current_state][end_state]=1
        else:
            transition_count[current_state][end_state]+=1
    return transition_count

def transmissionProbabilities():
    transmission_count=calculateTransmissionCount()
    transmission_probability=defaultdict(dict)
    for tagKey in transmission_count:
        for tag in available_tags:
            if tag not in transmission_count[tagKey]:
                transmission_count[tagKey][tag]=1
            else:
                transmission_count[tagKey][tag]+=1
        for tag in transmission_count[tagKey]:
            transmission_probability[tagKey][tag]=math.log(float(transmission_count[tagKey][tag]/tags_dictionary[tagKey]))
    return transmission_probability

def calculateEmissionCount():
    emission_count={}
    for sentence in text:
        words=sentence.split(" ")
        for word in words:
            word_check=word.split("/")
            word_without_tags,tags=word[:-(len(word_check[-1])+1)],word_check[-1]
            if tags not in emission_count:
                emission_count[tags]={}
            if word_without_tags not in emission_count[tags]:
                emission_count[tags][word_without_tags]=1
            else:
                emission_count[tags][word_without_tags]+=1
    return emission_count

def emissionProbabilites():
    emission_counts=calculateEmissionCount()
    emission_probability=defaultdict(dict)
    for tagKey in emission_counts:
        total_tags_for_tagKey=0
        for each_word in emission_counts[tagKey]:
            total_tags_for_tagKey=total_tags_for_tagKey+emission_counts[tagKey][each_word]
        for each_word in emission_counts[tagKey]:
            emission_probability[tagKey][each_word]=math.log(float(emission_counts[tagKey][each_word]/total_tags_for_tagKey))
    return emission_probability
transmission_probability=transmissionProbabilities()
emission_probabilites=emissionProbabilites()

with open("hmmmodel.txt","w",encoding="UTF-8") as fp:
    fp.write("Emission Probabilities=\n")
    fp.write(str(dict(emission_probabilites)))
    fp.write("\n")
    fp.write("Transmission Probabilites=\n")
    fp.write(str(dict(transmission_probability)))
    fp.write("\n")
    fp.write("Vocabulary=\n")
    fp.write(str(vocabulary))
    fp.write("\n")
    fp.write("Possible tags=\n")
    fp.write(str(available_tags))
    fp.write("\n")
fp.close()



        


