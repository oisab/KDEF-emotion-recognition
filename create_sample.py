import shutil
import os

# write here path to your sorted data directory
data_dir = r'/home/oisab/mai/vkr/DATASETS/KDEF_and_AKDEF/KDEF_sorted'
train_dir = 'train'
val_dir = 'val'
test_dir = 'test'
test_data_portion = 0.1
val_data_portion = 0.1
nb_images = 700


def create_directory(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)
    os.makedirs(os.path.join(dir_name, "afraid"))
    os.makedirs(os.path.join(dir_name, "angry"))
    os.makedirs(os.path.join(dir_name, "disgusted"))
    os.makedirs(os.path.join(dir_name, "happy"))
    os.makedirs(os.path.join(dir_name, "neutral"))
    os.makedirs(os.path.join(dir_name, "sad"))
    os.makedirs(os.path.join(dir_name, "surprised"))


create_directory(train_dir)
create_directory(val_dir)
create_directory(test_dir)


def copy_images(start_index, end_index, source_dir, destination_dir):
    for i in range(start_index, end_index):
        shutil.copy2(os.path.join(source_dir, "afraid/afraid_" + str(i) + ".jpg"),
                     os.path.join(destination_dir, "afraid"))
        shutil.copy2(os.path.join(source_dir, "angry/angry_" + str(i) + ".jpg"),
                     os.path.join(destination_dir, "angry"))
        shutil.copy2(os.path.join(source_dir, "disgusted/disgusted_" + str(i) + ".jpg"),
                     os.path.join(destination_dir, "disgusted"))
        shutil.copy2(os.path.join(source_dir, "happy/happy_" + str(i) + ".jpg"),
                     os.path.join(destination_dir, "happy"))
        shutil.copy2(os.path.join(source_dir, "neutral/neutral_" + str(i) + ".jpg"),
                     os.path.join(destination_dir, "neutral"))
        shutil.copy2(os.path.join(source_dir, "sad/sad_" + str(i) + ".jpg"),
                     os.path.join(destination_dir, "sad"))
        shutil.copy2(os.path.join(source_dir, "surprised/surprised_" + str(i) + ".jpg"),
                     os.path.join(destination_dir, "surprised"))


start_val_data_idx = int(nb_images * (1 - val_data_portion - test_data_portion))
start_test_data_idx = int(nb_images * (1 - test_data_portion))
print(start_val_data_idx)
print(start_test_data_idx)
copy_images(0, start_val_data_idx, data_dir, train_dir)
copy_images(start_val_data_idx, start_test_data_idx, data_dir, val_dir)
copy_images(start_test_data_idx, nb_images, data_dir, test_dir)
