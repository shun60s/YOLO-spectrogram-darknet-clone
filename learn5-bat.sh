# prepare
cd darknet
make clean
make
python process.py -d task2/

# start to learn from task1 last weight
./darknet detector train task2/voice.data task2/yolov3-obj.cfg task1/backup/yolov3-obj_last.weights -dont_show -map



