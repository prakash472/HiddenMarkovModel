import sys
with open("hmmmodel.txt","r",encoding="UTF-8") as fp:
    fp.readline()
    emission_probability=eval(fp.readline())
    fp.readline()
    transmission_probability=eval(fp.readline())
    fp.readline()
    vocabulary=eval(fp.readline())
    fp.readline()
    available_tags=eval(fp.readline())
fp.close()
available_tags=[tags for tags in available_tags if tags not in ["Start","End"]]
open_tag_list=[]
tags_dictionary={}
for tags,words in emission_probability.items():
    tags_dictionary[tags]=len(words)
print("The length of tag dictionary is",len(tags_dictionary))
for tag in available_tags:
    if tag!="Start" or tag!="End":
        if tags_dictionary[tag]>(3/100)*len(vocabulary):
            open_tag_list.append(tag)
print("The open class tag_list is",open_tag_list)

test_path=sys.argv[1]
with open(test_path,encoding = 'UTF-8') as fp:
    test_input=[line.rstrip('\n') for line in fp]


def getInitialStateProbability(current_state,state_prob):
    position=""
    max_prob=float("-inf")
    for item_prob in state_prob:
        if max_prob<state_prob[item_prob]+transmission_probability[item_prob][current_state]:
            position=item_prob
            max_prob=transmission_probability[item_prob][current_state]+state_prob[item_prob]
    return position,max_prob

def calculateEndTag(max_prob,words):
    end_prob = float("-inf")
    end_tag  = "" 
    for state in max_prob[len(words) -1]:
        if end_prob<max_prob[len(words)-1][state] + transmission_probability[state]["End"]:
            end_prob = transmission_probability[state]["End"] + max_prob[len(words)-1][state]
            end_tag = state
    return end_tag

def handlingForStartTag(first_word):
    position={}
    max_prob={}
    for tag in available_tags:
        if first_word in emission_probability[tag] and first_word in vocabulary  : 
            position[tag] = "Start"
            max_prob[tag] = emission_probability[tag][first_word] + transmission_probability["Start"][tag]
        elif first_word not in vocabulary:
            position[tag] = "Start"
            max_prob[tag] = transmission_probability["Start"][tag]
    return max_prob,position
    

def taggedSentence(sentence):
        words = sentence.split(" ")
        max_prob={}
        position={}
        first_prob,first_position=handlingForStartTag(words[0])
        max_prob[0]=first_prob
        position[0]=first_position
        for i in range(1,len(words)):
            position[i],max_prob[i] = {},{}
            for tag in available_tags:
                if words[i] in vocabulary and words[i] in emission_probability[tag]: 
                    position[i][tag],max_prob[i][tag] = getInitialStateProbability(tag, max_prob[i-1])
                    max_prob[i][tag] += emission_probability[tag][words[i]] 
                elif words[i] not in vocabulary:
                    if tag in open_tag_list:
                        position[i][tag],max_prob[i][tag] = getInitialStateProbability(tag, max_prob[i-1])
        end_tag=calculateEndTag(max_prob,words)
        output = []
        prediction_tag = end_tag
        for i in range(len(words) - 1, -1, -1):
            output.append(f"{words[i]}/{prediction_tag}")
            prediction_tag = position[i][prediction_tag]
        return output[::-1]


result=[]
for sentence in test_input:
    tagged_sentece=taggedSentence(sentence)
    new_sentence=" ".join(tagged_sentece)
    result.append(new_sentence)

file_pointer=open("hmmoutput.txt","w",encoding="UTF-8")
for sentence in result:
    file_pointer.write(sentence+"\n")
file_pointer.close()



