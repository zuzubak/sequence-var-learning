from numpy import random

def bootstrap(baseline_prob,test_prob,test_sample_size,n_iterations=10000):
    c=0
    probs_list=[]
    while c<n_iterations:
        trials=[]
        trial_number=0
        while trial_number<test_sample_size:
            if random.random()<baseline_prob:
                trials.append(1)
            else:
                trials.append(0)
            trial_number+=1
        trial_prob=sum(trials)/len(trials)
        probs_list.append(trial_prob)
        c+=1
    d=0
    for prob in probs_list:
        if baseline_prob<test_prob:
            if prob>=test_prob:
                d+=1
        if baseline_prob>test_prob:
            if prob<=test_prob:
                d+=1
    return 1-(d/n_iterations)
            