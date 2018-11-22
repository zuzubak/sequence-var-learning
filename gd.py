def find_cost(training_list):
    cost_megalist=[] 
    ls2=[]
    for constant in training_list:
        ls1=[]
        for training_item in training_list[1:]:
            cost_list=[]
            label=training_item[0]
            i=1
            for parameter in training_item[1:]:
                parameter_cost=abs(training_item[i] - constant[i-1])
                cost_list.append(parameter_cost)
                i+=1
                cost=sum(cost_list)
            ls1.append(cost)
        ls2.append(ls1)  
    return ls2