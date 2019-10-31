import batchent
import entropy
import spectral_pca
from scipy.spatial import distance
import csv
import index
import numpy
import previous_ent

meta_nest_dict = {
    'BrownBlue':['br82bl42','br81bl41','tutor_bl5wh5'],
    'GreenBlack':['gn56bk56','gn55bk55','tutor_or152br44'],
    'GreyCyan':['gy6cy6','gy5cy5','gy4cy4','tutor_br34bl20'],
    'OrangeBrown':['or189br53','or188br52','tutor_bk'],
    'PurpleGreen':['pu12gn8','tutor_si933'],
    'PurpleYellow':['pu17ye34','pu14ye31','tutor_ye20gy31'],
    'RedYellow':['re38ye2','re37ye1','re10ye9','tutor_si935'],
    'WhiteOrange':['wh96or142','wh100or80','tutor_si933(2)'],
    'YellowBlack':['ye84bk64','tutor_si936']
    }

directory='./data/BFs_logan/data/'
prefix='fathers_and_sons_from_logan - '

def branch_point_differences(n):
    out_dict={}
    syllables_dict={}
    for nest,birds_list in meta_nest_dict.items():
        nest_dict={}
        nest_syllable_dict={}
        pupil_IDs=birds_list[:-1]
        tutor_ID=birds_list[-1]
        for pupil_ID in pupil_IDs:
            fp1=directory+prefix+tutor_ID+'.csv'
            fp2=directory+prefix+pupil_ID+'.csv'
            distrib_1=entropy.branchpoints(fp1,[2,n+1])[n]
            distrib_2=entropy.branchpoints(fp2,[2,n+1])[n]
            bird1_branchpoints=[]
            bird2_branchpoints=[]
            for branchpoint_1 in distrib_1.keys():
                bird1_branchpoints.append(branchpoint_1)
            for branchpoint_2 in distrib_2.keys():
                bird2_branchpoints.append(branchpoint_2)
            branchpoints_to_analyze=[value for value in bird1_branchpoints if value in bird2_branchpoints]
            branchpoints_dict={}
            for branchpoint in branchpoints_to_analyze:
                count1=distrib_1[branchpoint]['count']
                count2=distrib_2[branchpoint]['count']
                mean_count=sum([count1,count2])/2
                differences_dict={}
                for transition in distrib_1[branchpoint]['transitions'].keys():
                    if transition in distrib_2[branchpoint]['transitions'].keys():
                        difference=abs(distrib_1[branchpoint]['transitions'][transition]-distrib_2[branchpoint]['transitions'][transition])
                    else:
                        difference=abs(distrib_1[branchpoint]['transitions'][transition])
                    differences_dict[transition]=difference
                for transition in distrib_2[branchpoint]['transitions'].keys():
                    if transition not in distrib_1[branchpoint]['transitions'].keys():
                        difference=abs(distrib_2[branchpoint]['transitions'][transition])
                    differences_dict[transition]=difference
                divergence=sum(differences_dict.values())/len(differences_dict.values())
                branchpoints_dict[branchpoint]={'mean_count':mean_count,'divergence':divergence}
            divergences=[]
            counts=[]
            for branchpoint,subdict in branchpoints_dict.items():
                divergences.append(subdict['divergence'])
                counts.append(subdict['mean_count'])
            shared_branchpoints=len(branchpoints_dict.keys())
            average_divergence=numpy.average(divergences,weights=counts)
            pupil_result=average_divergence
            nest_syllable_dict[pupil_ID]=branchpoints_dict
            nest_dict[pupil_ID]=pupil_result
        out_dict[nest]=nest_dict
        syllables_dict[nest]=nest_syllable_dict
    matrix_version=[]
    syllables_matrix_version=[]
    for nest,nestdict in out_dict.items():
        for bird,birdresult in nestdict.items():
            matrix_version.append(birdresult)
    for nest,nestdict in syllables_dict.items():
        for bird,birddict in nestdict.items():
            for syl,syldict in birddict.items():
                syllables_matrix_version.append([nest,bird,syl,syldict['divergence']])
    with open("./output/bird_divergence.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for row in matrix_version:
            writer.writerow([row])
    with open("./output/syllable_divergence.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Nest','BirdID','Syllable','Divergence'])
        for row in syllables_matrix_version:
            writer.writerow(row)
    return (matrix_version,syllables_dict)

def compare(n_for_previous_ent=2,ent_data=None):
    pca_data=spectral_pca.get_pca_matrix()
    if ent_data==None:
        ent_data=batchent.batch_syl_info_and_feats()
    divergence_data=branch_point_differences(2)[1]
    previous_ent_data=previous_ent.batch_pe(n=n_for_previous_ent)
    out_dict={}
    for nest,birds_list in meta_nest_dict.items():
        nest_dict={}
        pupil_IDs=birds_list[:-1]
        tutor_ID=birds_list[-1]
        tutor_syllables=pca_data[tutor_ID].keys()
        for pupil_ID in pupil_IDs:
            pupil_dict={}
            try:
                pupil_syllables=pca_data[pupil_ID].keys()
                retained_syllables = [value for value in tutor_syllables if value in pupil_syllables]
                for syllable in retained_syllables:
                    for row in ent_data:
                        if row[0]==pupil_ID and row[1]==syllable:
                            pupil_entropy=row[2]
                        if row[0]==tutor_ID and row[1]==syllable:
                            tutor_entropy=row[2]
                            tutor_spectral_data=row[-6:]
                    tutor_pca=pca_data[tutor_ID][syllable]
                    pupil_pca=pca_data[pupil_ID][syllable]
                    spectral_distance= distance.euclidean(tuple(tutor_pca),tuple(pupil_pca))
                    divergence=divergence_data[nest][pupil_ID][tuple(syllable)]['divergence']
                    tutor_previous_ent=previous_ent_data[tutor_ID][syllable]
                    pupil_previous_ent=previous_ent_data[pupil_ID][syllable]
                    pupil_dict[syllable] = [tutor_entropy,pupil_entropy,spectral_distance,divergence,tutor_previous_ent,pupil_previous_ent]
                    for feature in tutor_spectral_data:
                        pupil_dict[syllable].append(feature)
            except:
                pass
            print(pupil_dict)
            nest_dict[pupil_ID]=pupil_dict
        out_dict[nest]=nest_dict
    print(out_dict)
    matrix_version=[]
    for nest,nestdict in out_dict.items():
        for bird,birddict in nestdict.items():
            for syl,syllist in birddict.items():
                matrix_version.append([nest,bird,syl]+syllist)
    with open("./output/nest_learning.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Nest','BirdID','Syllable','TutorEntropy','PupilEntropy','SpectralDistance','Divergence','TutorPreviousEnt','PupilPreviousEnt','MeanFreq','SpecDense','Duration','LoudEnt','SpecTempEnt','meanLoud'])
        for row in matrix_version:
            writer.writerow(row)
    return matrix_version

def average(previous_result):
    out_dict={}
    bird_dict={}
    for row in previous_result:
        if row[1] not in bird_dict.keys():
            bird_dict[row[1]]=[]
        bird_dict[row[1]].append(row[-1])
    for key,value in bird_dict.items():
        out_dict[key]=sum(value)/len(value)
    matrix_version=[]
    for bird,birdresult in out_dict.items():
        matrix_version.append(birdresult)
    with open("./output/average_spectral_distances.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for row in matrix_version:
            writer.writerow([row])
    return matrix_version