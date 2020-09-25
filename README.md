# YOLO spectrogram darknet clone   

This is a try of spectrogram detector by yolo cloned from AlexeyAB/darknet.git.   


## condition    

This time, train and test size is very small, 84 and 20.   
There are only two classes, voice and instrument, that means bent lines and flat lines,  
although they don't mean true voice and true instrument.   

## result  

train data  
![figure1](predictions-img78.jpg)  
![figure2](predictions-img0.jpg)  



valid(test) data  
![figure3](predictions-img35.jpg)  
![figure4](predictions-img35-thresh0_1.jpg)  


## loss and mAP(mean Average Precision)    
mAP is still not good.  

![figure5](chart_yolov3-obj.png)   


## train and test  

Please refer to learn4-bat.sh and test4-bat.sh.   











