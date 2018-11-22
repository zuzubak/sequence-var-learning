import csv


def classify(test_list,training_list): # takes each person's attendance, goes through each dinner, and calculates the matching with every other person at that dinner (difference between their values for that dinner)
    result=[]
    for test_item in test_list:
        current_choice=[['place_holder',1000000000000000]] #here's where you write a comprehensive comment
        for training_item in training_list:
            cost_list=[] # the lowest cost => they went to the maximum of the same dinners
            label=training_item[0]
            i=1
            for parameter in training_item[1:]: # calculating costs for individual dinners (per person / per "friend")
                parameter_cost=abs(training_item[i] - test_item[i-1])
                cost_list.append(parameter_cost)
                i+=1
            cost=sum(cost_list) # sum of all dinner costs (per person / per "friend")
            j=0
            for ch_item in current_choice: # ranking people's summed costs from least to largest
                if cost<=ch_item[1] or len(current_choice)==1:
                    if [label,cost] not in current_choice:
                        current_choice.insert(j,[label,cost])
                j+=1 
    result.append(current_choice)
    return result

def classify_from_csv(filepath): # creating a list for classify (from a csv file)
    training_list = []
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            new_row=[row[0]]
            training_list.append(new_row)
            for column in row[1:]:
                new_row.append(int(column))
            training_list.append(new_row)
            line_count += 1
    return training_list

def find_sim(test_label_list,filepath,n): 
    training_list=classify_from_csv(filepath)
    test_vector=[[]]
    i=0
    for label in test_label_list:
        for training_item in training_list:
            if training_item[0]==label:
                test_vector[i]=training_item[1:]
        i+=1
    result=classify(test_vector,training_list)
    result_trunc=[]
    for item in result:
        result_trunc.append(item[1:n+1])
    return result_trunc