import json
import os

datasets_folder = '/home/xaxi/PycharmProjects/experience-recorder/datasets-copy/2048/'
datasets = [os.path.join(datasets_folder,dataset_dir) for dataset_dir in os.listdir(datasets_folder)]

# print(datasets)
rolling = 5

datasets.sort()


def calculate_reward(scores):
    if len(scores) == 1:
        return -1
    reward = []
    for i,score in enumerate(scores[:-1]):
        if scores[i+1] == score:
            reward.append(-1)
        else:
            reward.append(1)
    print('r',reward)
    print('s',sum(reward))
    return sum(reward)/(rolling-1)




for dataset in datasets:
    files = os.listdir(dataset)
    files = [file for file in files if file.split('.')[1] == 'json']
    files.sort()
    for i,file in enumerate(files):
        filename = os.path.join(dataset, file)
        rolling_score = []

        current_file = open(filename)
        json_file = json.load(current_file)
        current_file.close()

        score = json_file['score']
        index_rolling =  rolling if i + rolling <= len(files) else len(files) - i
        for next_file in files[i:i+index_rolling]:
            score_i = json.load(open(os.path.join(dataset, next_file)))['score']
            rolling_score.append(score_i)

        rolling_score = calculate_reward(rolling_score)
        json_file['reward'] = rolling_score

        with open(os.path.join(dataset, file), "w") as outfile:
            print('jsonfile',json_file)
            json.dump(json_file, outfile)



