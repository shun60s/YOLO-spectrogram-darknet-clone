import glob, os

#
# This is a porting from https://timebutt.github.io/static/how-to-train-yolov2-to-detect-custom-objects/
# of which author is Nils Tijtgat.


# Current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
task_name = os.path.join(current_dir, 'task1/')

# Directory where the data will reside, relative to 'darknet.exe'
path_data = task_name + 'datasets/'

# Percentage of images to be used for the test set
percentage_test = 20;

# Create and/or truncate train.txt and test.txt
file_train = open(task_name + 'train.txt', 'w')  
file_test = open(task_name + 'test.txt', 'w')

# Populate train.txt and test.txt
counter = 1  
index_test = round(100 / percentage_test)  
for pathAndFilename in glob.iglob(os.path.join(path_data, "*.jpg")):  
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test:
        counter = 1
        file_test.write(path_data + title + '.jpg' + "\n")
    else:
        file_train.write(path_data + title + '.jpg' + "\n")
        counter = counter + 1


