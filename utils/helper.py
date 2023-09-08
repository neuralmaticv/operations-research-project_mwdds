import os
import glob
import json

def listdir_nohidden(path):
    return glob.glob(os.path.join(path, 'V*'))

def instances_to_json(pt_path: str, json_name: str) -> None:
    def _listdir_problem_types(path):
        return glob.glob(os.path.join(path, 'V*')) # match only folders starting with V (V50E50, V50E100, etc.)

    def _construct_dict(problem_types):
        d = {}
        for problem_type in problem_types:
            d[problem_type.split('/')[-1]] = []
        return d
    
    
    pt_folders = _listdir_problem_types(pt_path)
    pt_folders = sorted(pt_folders, key=lambda x: (int(x.split('/')[-1].split('E')[0][1:]), int(x.split('/')[-1].split('E')[1][0:]))) # V50E50, V50E100, etc.
    pt_folder_n = sorted(os.listdir(pt_folders[0]), key=lambda x: int(x)) # folders 0, 1, 2..

    rakaj_dict = _construct_dict(pt_folders)

    for folder in pt_folders:
        key = folder.split('/')[-1]
        
        for instance in pt_folder_n:
            pt_instances = os.path.join(folder, instance, 'Test')
            for file in os.listdir(pt_instances):
                if file.startswith('Problem.dat'):
                    rakaj_dict[key].append(os.path.join(instance, 'Test', file))
            
                
    
    with open(json_name + ".json", 'w') as json_file:
        json.dump(rakaj_dict, json_file, indent=4)

def read_json(json_file_path: str) -> dict:
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    return data
