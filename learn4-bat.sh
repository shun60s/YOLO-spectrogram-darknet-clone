# prepare
cd darknet
make clean
make
python process.py

# start to learn
wget https://pjreddie.com/media/files/darknet53.conv.74
./darknet detector train task1/voice.data task1/yolov3-obj.cfg darknet53.conv.74 -dont_show -map

# reload
./darknet detector train task1/voice.data task1/yolov3-obj.cfg task1/backup/yolov3-obj_last.weights -dont_show -map


