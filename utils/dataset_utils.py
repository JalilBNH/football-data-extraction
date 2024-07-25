import os 
import shutil
import yaml



def prepare_dataset(dataset_path):
    """Format a dataset path made with CVAT and exported in yolo format to work with YOLO of ultralytics. The formated dataset is in {dataset_path/00}
    CAUTION : this function moves all the file and do not copy them !!!
    Args:
        dataset_path (string): path/to/dataset
    """

    paths = [
        '00',
        '00/train',
        '00/train/images',
        '00/train/labels', 
        '00/test',
        '00/test/images',
        '00/test/labels',
        '00/val',
        '00/val/images',
        '00/val/labels'
    ]

    for path in paths: os.makedirs(os.path.join(dataset_path, path), exist_ok=True) # Create the directory we need


    data = {} # Contains all the yaml file info 

    # Move all images in the new folder
    if os.path.exists(os.path.join(dataset_path, 'obj_Train_data')):
        data['train'] = os.path.join(dataset_path, '00', 'train', 'images')
        for file in os.listdir(os.path.join(dataset_path, 'obj_Train_data')):
            print(file)
            if file.endswith('jpg'):
                shutil.move(os.path.join(dataset_path, 'obj_Train_data', file), os.path.join(dataset_path, '00/train/images', file))
            if file.endswith('txt'):
                shutil.move(os.path.join(dataset_path, 'obj_Train_data', file), os.path.join(dataset_path, '00/train/labels', file))


    if os.path.exists(os.path.join(dataset_path, 'obj_Test_data')):
        data['test'] = os.path.join(dataset_path, '00', 'test', 'images')
        for file in os.listdir(os.path.join(dataset_path, 'obj_Test_data')):
            print(file)
            if file.endswith('jpg'):
                shutil.move(os.path.join(dataset_path, 'obj_Test_data', file), os.path.join(dataset_path, '00/test/images', file))
            if file.endswith('txt'):
                shutil.move(os.path.join(dataset_path, 'obj_Test_data', file), os.path.join(dataset_path, '00/test/labels', file))


    if os.path.exists(os.path.join(dataset_path, 'obj_Validation_data')):
        data['val'] = os.path.join(dataset_path, '00', 'val', 'images')
        for file in os.listdir(os.path.join(dataset_path, 'obj_Validation_data')):
            print(file)
            if file.endswith('jpg'):
                shutil.move(os.path.join(dataset_path, 'obj_Validation_data', file), os.path.join(dataset_path, '00/val/images', file))
            if file.endswith('txt'):
                shutil.move(os.path.join(dataset_path, 'obj_Validation_data', file), os.path.join(dataset_path, '00/val/labels', file))



    names = []
    with open(os.path.join(dataset_path, 'obj.names'), 'r') as file:
        for f in file:
            names.append(f[:-1])

    data['nc'] = len(names)
    data['names'] = names


    # Create and write everything in the yaml file
    with open(os.path.join(dataset_path, '00', 'data.yaml'), 'w') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)