import batchent
import entropy
import spectral_pca
from scipy.spatial import distance
import csv
import index
import numpy
import previous_ent
import dkl
import pandas as pd
import imp
import math
import spread
import pickle_commands as pc
imp.reload(spectral_pca)
imp.reload(dkl)
imp.reload(batchent)

meta_nest_dict = {
    'BrownBlue': ['br82bl42', 'br81bl41', 'tutor_bl5wh5'],
    'GreenBlack': ['gn56bk56', 'gn55bk55', 'tutor_or152br44'],
    'GreyCyan': ['gy6cy6', 'gy5cy5', 'gy4cy4', 'tutor_br34bl20'],
    'OrangeBrown': ['or189br53', 'or188br52', 'tutor_bk'],
    'PurpleGreen': ['pu12gn8', 'tutor_si933'],
    'PurpleYellow': ['pu17ye34', 'pu14ye31', 'tutor_ye20gy31'],
    'RedYellow': ['re38ye2', 're37ye1', 're10ye6', 'tutor_si935'],
    'WhiteOrange': ['wh96or142', 'wh100or80', 'tutor_si933(2)'],
    'YellowBlack': ['ye73bk73', 'ye84bk64', 'tutor_si936'],
    'YellowGrey' : ['ye44gy44', 'tutor_or172br12']
}


directory = './data/BFs_logan/data/'
prefix = 'fathers_and_sons_from_logan - '


prevalence_dict = {}
category_dict = {}
prevalence_data = pd.read_csv('./data/Data4Malcolm - main.csv')
for tutor_syllable,pupil_syllable,prevalence,category in zip(prevalence_data['TutorID_Syllable'],
        prevalence_data['PupilID_Syllable'],
        prevalence_data['perTut'],
        prevalence_data['Category']):
    prevalence_dict[tutor_syllable] = prevalence
    category_dict[pupil_syllable] = category


def branch_point_differences(n,mode):
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
            branchpoints_to_analyze = [value for value in bird1_branchpoints if value in bird2_branchpoints]
            branchpoints_dict = {}
            for branchpoint in branchpoints_to_analyze:
                differences_dict={}
                if branchpoint in distrib_1.values():
                    count1 = distrib_1[branchpoint]['count']
                else:
                    count1 = 0
                if branchpoint in distrib_2.values():
                    count2 = distrib_1[branchpoint]['count']
                else:
                    count2 = 0
                transitions_to_analyze = list(distrib_1[branchpoint]['transitions'].keys())+list(distrib_2[branchpoint]['transitions'].keys())
                for transition in transitions_to_analyze:
                        if transition not in distrib_1[branchpoint]['transitions'].keys():
                            bird1_value = 0.00000001
                        else:
                            bird1_value = distrib_1[branchpoint]['transitions'][transition]
                        if transition not in distrib_2[branchpoint]['transitions'].keys():
                            bird2_value = 0.00000001
                        else:
                            bird2_value = distrib_2[branchpoint]['transitions'][transition]
                        if mode == 'euclidean':
                            difference = abs(bird1_value-bird2_value)
                        if mode == 'dkl':
                            difference = bird1_value * math.log2(bird1_value/bird2_value)
                        if mode == 'log':
                            difference = abs(math.log2(bird1_value)-math.log2(bird2_value))
                        differences_dict[transition] = difference
                divergence = sum(differences_dict.values())
                branchpoints_dict[branchpoint] = {
                    'tutor_count': count1, 
                    'pupil_count': count2, 
                    'divergence': divergence}
            divergences = []
            counts = []
            for branchpoint, subdict in branchpoints_dict.items():
                divergences.append(subdict['divergence'])
            shared_branchpoints = len(branchpoints_dict.keys())
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


def compare(n_for_previous_ent=2, ent_data=None):
    pca_data = spectral_pca.get_pca_matrix()
    if ent_data is None:
        ent_data = batchent.batch_syl_info_and_feats()
    divergence_data = branch_point_differences(2,'euclidean')[1]
    previous_ent_data = previous_ent.batch_pe(n=n_for_previous_ent)
    out_dict = {}
    for nest, birds_list in meta_nest_dict.items():
        nest_dict = {}
        pupil_IDs = birds_list[:-1]
        tutor_ID = birds_list[-1]
        tutor_syllables = pca_data[tutor_ID].keys()
        for pupil_ID in pupil_IDs:
            pupil_dict = {}
            try:
                pupil_syllables = pca_data[pupil_ID].keys()
                retained_syllables = [
                    value for value in tutor_syllables if value in pupil_syllables]
                dropped_syllables = [
                    value for value in tutor_syllables if value not in pupil_syllables]
                for syllable in retained_syllables:
                    for row in ent_data:
                        if row[0] == pupil_ID and row[1] == syllable:
                            pupil_entropy = row[2]
                        if row[0] == tutor_ID and row[1] == syllable:
                            tutor_entropy = row[2]
                            tutor_spectral_data = row[-6:]
                    tutor_pca = pca_data[tutor_ID][syllable]
                    pupil_pca = pca_data[pupil_ID][syllable]
                    spectral_distance = distance.euclidean(
                        tuple(tutor_pca), tuple(pupil_pca))
                    divergence = divergence_data[nest][pupil_ID][tuple(
                        syllable)]['divergence']
                    tutor_previous_ent = previous_ent_data[tutor_ID][syllable]
                    pupil_previous_ent = previous_ent_data[pupil_ID][syllable]
                    pupil_dict[syllable] = [
                        tutor_entropy,
                        pupil_entropy,
                        spectral_distance,
                        divergence,
                        tutor_previous_ent,
                        pupil_previous_ent]
                    for feature in tutor_spectral_data:
                        pupil_dict[syllable].append(feature)
            except BaseException:
                pass
            nest_dict[pupil_ID] = pupil_dict
        out_dict[nest] = nest_dict
    matrix_version = []
    for nest, nestdict in out_dict.items():
        for bird, birddict in nestdict.items():
            for syl, syllist in birddict.items():
                matrix_version.append([nest, bird, syl] + syllist)
    with open("./output/nest_learning.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Nest',
                         'BirdID',
                         'Syllable',
                         'TutorEntropy',
                         'PupilEntropy',
                         'SpectralDistance',
                         'Divergence',
                         'TutorPreviousEnt',
                         'PupilPreviousEnt',
                         'MeanFreq',
                         'SpecDense',
                         'Duration',
                         'LoudEnt',
                         'SpecTempEnt',
                         'meanLoud'])
        for row in matrix_version:
            writer.writerow(row)
    return matrix_version

def tutor_compare(n_for_previous_ent=2):
    pca_data = spectral_pca.get_pca_matrix()
    token_pca_data = spectral_pca.tokens_by_type()
    forwards_ent_data = pc.depickle('forwards_ent_data')
    backwards_ent_data = pc.depickle('backwards_ent_data')
    fEP = pc.depickle('fEP')
    bEP = pc.depickle('bEP')
    divergence_data = branch_point_differences(2,'euclidean')[1]
    dkl_data = branch_point_differences(2,'dkl')[1]
    log_data = branch_point_differences(2,'log')[1]
    previous_ent_data = previous_ent.batch_pe(n=n_for_previous_ent)
    out_dict = {}
    for nest, birds_list in meta_nest_dict.items():
        nest_dict = {}
        pupil_IDs = birds_list[:-1]
        tutor_ID = birds_list[-1]
        tutor_syllables = pca_data[tutor_ID].keys()
        for pupil_ID in pupil_IDs:
            pupil_dict = {}
            tutor_syllables = pca_data[tutor_ID].keys()
            pupil_syllables = pca_data[pupil_ID].keys()
            retained_syllables = [
                value for value in tutor_syllables if value in pupil_syllables]
            dropped_syllables = [
                value for value in tutor_syllables if value not in pupil_syllables]
            for syllable in tutor_syllables:
                try:
                    prevalence = prevalence_dict[tutor_ID+'_'+syllable]
                    category = category_dict[pupil_ID+'_'+syllable]
                except:
                    prevalence = ''
                    category = ''
                pupil_entropy=''
                direction_dict={'forwards':{'tutor':'','pupil':''},'backwards':{'tutor':'','pupil':''},'fEP':{'tutor':'','pupil':''},'bEP':{'tutor':'','pupil':''}}
                for direction,direction_data in zip(['forwards','backwards','fEP','bEP'],[forwards_ent_data,backwards_ent_data,fEP,bEP]):
                    for row in direction_data:
                        if row[0] == pupil_ID and row[1] == syllable:
                            direction_dict[direction]['pupil'] = row[2]
                        if row[0] == tutor_ID and row[1] == syllable:
                            direction_dict[direction]['tutor'] = row[2]
                            tutor_spectral_data = row[-6:]
                spectral_distance = ''
                divergence=''
                dkl_value = ''
                log_value = ''
                try:
                    tutor_spread = spread.spread(token_pca_data[tutor_ID + '_' + syllable])
                except:
                    tutor_spread = ''
                try:
                    pupil_spread = spread.spread(token_pca_data[pupil_ID + '_' + syllable])
                except:
                    pupil_spread = ''
                try:
                    cloud_distance = spread.sim(token_pca_data[tutor_ID + '_' + syllable], 
                                                                token_pca_data[pupil_ID + '_' + syllable])
                except:
                    cloud_distance = ''
                try:
                    tutor_pca = pca_data[tutor_ID][syllable]
                    pupil_pca = pca_data[pupil_ID][syllable]
                    spectral_distance = distance.euclidean(
                        tuple(tutor_pca), tuple(pupil_pca))
                except:
                    pass
                if category == 'Retained':
                    try:
                        divergence = divergence_data[nest][pupil_ID][tuple(
                            syllable)]['divergence']
                        dkl_value = dkl_data[nest][pupil_ID][tuple(
                            syllable)]['divergence']
                        log_value = log_data[nest][pupil_ID][tuple(
                            syllable)]['divergence']
                    except:
                        pass
                try:
                    tutor_previous_ent = previous_ent_data[tutor_ID][syllable]
                    pupil_previous_ent = ''
                except:
                    pass
                try:
                    pupil_previous_ent = previous_ent_data[pupil_ID][syllable]
                except:
                    pass
                pupil_dict[syllable] = [
                    prevalence,
                    category,
                    direction_dict['forwards']['tutor'],
                    direction_dict['forwards']['pupil'],
                    direction_dict['backwards']['tutor'],
                    direction_dict['backwards']['pupil'],
                    direction_dict['fEP']['tutor'],
                    direction_dict['fEP']['pupil'],
                    direction_dict['bEP']['tutor'],
                    direction_dict['bEP']['pupil'],
                    spectral_distance,
                    tutor_spread,
                    pupil_spread,
                    cloud_distance,
                    divergence,
                    dkl_value,
                    log_value,
                    tutor_previous_ent,
                    pupil_previous_ent]
                for feature in tutor_spectral_data:
                    pupil_dict[syllable].append(feature)
            nest_dict[pupil_ID] = pupil_dict
        out_dict[nest] = nest_dict
    matrix_version = []
    for nest, nestdict in out_dict.items():
        for bird, birddict in nestdict.items():
            for syl, syllist in birddict.items():
                matrix_version.append([nest, bird, syl] + syllist)
    with open("./output/nest_learning.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Nest',
                         'BirdID',
                         'Syllable',
                         'Prevalence',
                         'Category',
                         'TutorForwardsEntropy',
                         'PupilForwardsEntropy',
                         'TutorBackwardsEntropy',
                         'PupilBackwardsEntropy',
                         'TutorfEP',
                         'PupilfEP',
                         'TutorbEP',
                         'PupilbEP',
                         'SpectralDistance',
                         'TutorSpread',
                         'PupilSpread',
                         'CloudDistance',
                         'EuclideanDistance',
                         'DKL',
                         'LogDistance',
                         'TutorPreviousEnt',
                         'PupilPreviousEnt',
                         'MeanFreq',
                         'SpecDense',
                         'Duration',
                         'LoudEnt',
                         'SpecTempEnt',
                         'meanLoud'])
        for row in matrix_version:
            writer.writerow(row)
    return matrix_version


def average(previous_result):
    out_dict = {}
    bird_dict = {}
    for row in previous_result:
        if row[1] not in bird_dict.keys():
            bird_dict[row[1]] = []
        bird_dict[row[1]].append(row[-1])
    for key, value in bird_dict.items():
        out_dict[key] = sum(value) / len(value)
    matrix_version = []
    for bird, birdresult in out_dict.items():
        matrix_version.append(birdresult)
    with open("./output/average_spectral_distances.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for row in matrix_version:
            writer.writerow([row])
    return matrix_version
