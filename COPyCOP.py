import sys
sys.path.append('/home/khkim/work/copycop_v1.0.0')

import csv
import json
import multiprocessing 
import os
import uuid
import shutil
from copycop_release.imageCOP.trainImage import imageTrain
from imageCOP.inferenceImage import imageCompare
from textCOP.textcop import TextLearning, TextSimilarity
import json

def readJsonType(jsonData):
    # Read for inference or train
    foramtTypes = []
    for data in jsonData:
        foramtTypes.append(data['type'])

    return foramtTypes

def readJsonForImage(jsonData, jsonTitle):
    # Read for inference or train
    uuids = []
    imageNames = []

    datas = jsonData[jsonTitle]
    print('length of inference : ', len(datas))
    for data in datas:
        if data['type'] == 'IMG':
            uuids.append(data['source'])
            imageNames.append(data['file'])

    print('Reading Json is done')
    return imageNames, uuids

def parseJsonForText(in_json_dict, in_dataset_root):
    ret_val = True

    # create dataset root directory
    dataset_root_dir = in_dataset_root
    os.makedirs(dataset_root_dir, exist_ok=True)
    print('========> parseJsonForText() dataset_root_dir = : ', dataset_root_dir)
    
    dataset_mode = -1  # 0=training 1=inference    
    first_key = list(in_json_dict.keys())[0]  #'learning-in' or 'similarity-in'
    info_file_name = ''
    if first_key == 'learning-in':
        dataset_mode = 0
        medi_dir = 'winners'
        filearray = in_json_dict.get('learning-in')
        info_file_name = 'filelist_info_training.csv'
    elif first_key == 'similarity-in':
        dataset_mode = 1
        medi_dir = 'applies'
        filearray = in_json_dict.get('similarity-in')
        info_file_name = 'filelist_info_inference.csv'
    else:
        print("ERROR : JSON first key is wrong. It must be 'learning-in' or 'similarity-in'")
        ret_val = False

    # make directories ('winner' or 'applies')
    dst_dir = os.path.join(dataset_root_dir, medi_dir)
    os.makedirs(dst_dir, exist_ok=True)
    
    # rename & copy files
    filelist_info = open(os.path.join(dataset_root_dir, info_file_name), 'w', newline='')
    wr = csv.writer(filelist_info)
    
    if len(filearray) > 0:
        for info in filearray:
            uuid = info.get('source')
            filename = info.get('file')
            print('uuid : ', uuid)
            print('type : ', info.get('type'))                
            print('filename : ', filename)

            if info.get('type') == 'TXT':
                dst_full_name = os.path.join(dst_dir, uuid+'.txt')
                print('dst_full_name : ', dst_full_name)
                shutil.copyfile(filename, dst_full_name)
                # uuid 와 파일명을 기록
                wr.writerow([uuid, dst_full_name])
    else: 
        print("ERROR : JSON array is empty")
        ret_val = False

    filelist_info.close()

    return ret_val

def loadConfig():
    json_dict = dict()
    with open('./copycop_release/config.json', 'r') as f:
        json_dict = json.load(f)
    return json_dict

def COPyCOP(jsonData):
    
    return_dict1 = multiprocessing.Queue()
    return_dict2 = multiprocessing.Queue()

    json_dict = jsonData
    config = loadConfig()
    jsonTitle = list(json_dict.keys())[0]

    if jsonTitle == 'learning-in':

        typeList = readJsonType(json_dict[jsonTitle])

        p1_detected = False
        p2_detected = False

        if 'IMG' in typeList:
            print('Train IMG is exist')

            imageNames, uuids = readJsonForImage(json_dict, jsonTitle)
            inputData = [imageNames, uuids]

            p1 = multiprocessing.Process(target=imageTrain, args=(inputData, config, return_dict1))
            p1.start()
            p1_detected = True
        if 'TXT' in typeList:
            print('Train TXT is exist')
            text_data_root = config.get('config')['text']['data_root']   #'./copycop/textCOP/dataset/dataset02'
            if parseJsonForText(json_dict, text_data_root) == True:
                #p2 = multiprocessing.Process(target=TextLearning, args=(json_dict, './copycop_release/textCOP/dataset/dataset02', 0, return_dict2))
                p2 = multiprocessing.Process(target=TextLearning, args=(json_dict, config, 0, return_dict2))
                p2.start()
                p2_detected = True

        result_json1 = None
        result_json2 = None

        if p1_detected == True:
            p1.join()
            result_json1 = return_dict1.get()

        if p2_detected == True:
            p2.join()
            result_json2 = return_dict2.get()

        print('end')
        return result_json1, result_json2
    elif jsonTitle == 'similarity-in':

        typeList = readJsonType(json_dict[jsonTitle])

        p1_detected = False
        p2_detected = False

        if 'IMG' in typeList:
            print('Inference IMG is exist')

            imageNames, uuids = readJsonForImage(json_dict, jsonTitle)
            inputData = [imageNames, uuids]

            p1 = multiprocessing.Process(target=imageCompare, args=(inputData, config, return_dict1))
            p1.start()
            p1_detected = True
        if 'TXT' in typeList:
            print('Inference TXT is exist')
            text_data_root = config.get('config')['text']['data_root']   #'./copycop/textCOP/dataset/dataset02'
            if parseJsonForText(json_dict, text_data_root) == True:
                #p2 = multiprocessing.Process(target=TextSimilarity, args=(json_dict, './copycop_release/textCOP/dataset/dataset02', return_dict2))
                p2 = multiprocessing.Process(target=TextSimilarity, args=(json_dict, config, return_dict2))
                p2.start()
                p2_detected = True

        result_json1 = None
        result_json2 = None

        if p1_detected == True:
            p1.join()
            result_json1 = return_dict1.get()

        if p2_detected == True:
            p2.join()
            result_json2 = return_dict2.get()

        print('end')
        return result_json1, result_json2
    else: 
        print('Unknown Title. Check your json')
        return None, None
