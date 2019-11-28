import batchent
import entropy
import spectral_pca
from scipy.spatial import distance
import csv
import index
import numpy as np
import previous_ent

meta_nest_dict = {
    'BrownBlue': ['br82bl42', 'br81bl41', 'tutor_bl5wh5'],
    'GreenBlack': ['gn56bk56', 'gn55bk55', 'tutor_or152br44'],
    'GreyCyan': ['gy6cy6', 'gy5cy5', 'gy4cy4', 'tutor_br34bl20'],
    'OrangeBrown': ['or189br53', 'or188br52', 'tutor_bk'],
    'PurpleGreen': ['pu12gn8', 'tutor_si933'],
    'PurpleYellow': ['pu17ye34', 'pu14ye31', 'tutor_ye20gy31'],
    'RedYellow': ['re38ye2', 're37ye1', 're10ye6', 'tutor_si935'],
    'WhiteOrange': ['wh96or142', 'wh100or80', 'tutor_si933(2)'],
    'YellowBlack': ['ye84bk64', 'tutor_si936']
}

directory = './data/BFs_logan/data/'
prefix = 'fathers_and_sons_from_logan - '

def dkl(n):
    out_dict = {}
    syllables_dict = {}
    for nest, birds_list in meta_nest_dict.items():
        nest_dict = {}
        nest_syllable_dict = {}
        pupil_IDs = birds_list[:-1]
        tutor_ID = birds_list[-1]
        for pupil_ID in pupil_IDs:
            fp1 = directory + prefix + tutor_ID + '.csv'
            fp2 = directory + prefix + pupil_ID + '.csv'
            distrib_1 = entropy.branchpoints(fp1, [2, n + 1])[n]
            distrib_2 = entropy.branchpoints(fp2, [2, n + 1])[n]
            bird1_branchpoints = []
            bird2_branchpoints = []
            for branchpoint_1 in distrib_1.keys():
                bird1_branchpoints.append(branchpoint_1)
            for branchpoint_2 in distrib_2.keys():
                bird2_branchpoints.append(branchpoint_2)
            branchpoints_to_analyze = [
                value for value in bird1_branchpoints if value in bird2_branchpoints]
            branchpoints_dict = {}
            for branchpoint in branchpoints_to_analyze:
                count1 = distrib_1[branchpoint]['count']
                count2 = distrib_2[branchpoint]['count']
                mean_count = sum([count1,count2])/2
                differences_dict = {}
                for transition in distrib_1[branchpoint]['transitions'].keys():
                    bird1_value = distrib_1[branchpoint]['transitions'][transition]
                    if transition not in distrib_2[branchpoint]['transitions'].keys():
                        bird2_value = 0.00000001
                    else:
                        bird2_value = distrib_2[branchpoint]['transitions'][transition]
                    difference = bird1_value * np.log(bird1_value/bird2_value)
                    differences_dict[transition] = difference
                for transition in distrib_2[branchpoint]['transitions'].keys():
                    bird2_value = distrib_2[branchpoint]['transitions'][transition] 
                    if transition not in distrib_1[branchpoint]['transitions'].keys(
                    ):
                        bird1_value = 0.00000001
                        difference = bird1_value * np.log(bird1_value/bird2_value)
                        differences_dict[transition] = difference
                divergence = sum(differences_dict.values()) / \
                    len(differences_dict.values())
                branchpoints_dict[branchpoint] = {
                    'tutor_count': count1, 
                    'pupil_count': count2, 
                    'mean_count' : mean_count, 
                    'divergence': divergence}
            divergences = []
            counts = []
            for branchpoint, subdict in branchpoints_dict.items():
                divergences.append(subdict['divergence'])
                counts.append(subdict['mean_count'])
            shared_branchpoints = len(branchpoints_dict.keys())
            average_divergence = np.average(divergences, weights=counts)
            pupil_result = average_divergence
            nest_syllable_dict[pupil_ID] = branchpoints_dict
            nest_dict[pupil_ID] = pupil_result
        out_dict[nest] = nest_dict
        syllables_dict[nest] = nest_syllable_dict
    matrix_version = []
    syllables_matrix_version = []
    for nest, nestdict in out_dict.items():
        for bird, birdresult in nestdict.items():
            matrix_version.append(birdresult)
    for nest, nestdict in syllables_dict.items():
        for bird, birddict in nestdict.items():
            for syl, syldict in birddict.items():
                syllables_matrix_version.append(
                    [nest, bird, syl, syldict['divergence']])
    with open("./output/bird_divergence.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for row in matrix_version:
            writer.writerow([row])
    with open("./output/syllable_divergence.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Nest', 'BirdID', 'Syllable', 'Divergence'])
        for row in syllables_matrix_version:
            writer.writerow(row)
    return [matrix_version,syllables_dict]