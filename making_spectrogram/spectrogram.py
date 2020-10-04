#coding:utf-8

#  Read a wav file and write out spectrogram as jpg files
#
#  BPF bank analysis Spectrogram of which feature are
#   a) BPF's target response is 2nd harmonic level less than -70dB
#   b) Mel-frequency division
#   c) Half-wave rectification until a few KHz signal or DC with ripple signal
#   d) Down sampling to decrease temporal resolution
#   e) N-th root compression 
#   f) normalized Gray scale image

import sys
import argparse
import pathlib
from scipy import signal
from scipy.io.wavfile import read as wavread
from matplotlib import pyplot as plt


from mel  import *
from BPF4 import *
from Compressor1 import *


# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy 1.18.4
#  matplotlib  3.3.1
#  scipy 1.4.1


class Class_Analysis1(object):
    def __init__(self, num_band=1024, fmin=40, fmax=8000, sr=44100, Q=40.0, \
        moving_average_factor=50, down_sample_factor=10, \
        power_index=1/3.5, \
        save_file_path="test"):
        # instance
        # (1) mel frequency list
        self.num_band=num_band
        self.fmin=fmin
        self.fmax=fmax
        self.mel=Class_mel(self.num_band, self.fmin, self.fmax)
        # (2) BPF bank
        self.sr= sr
        self.Q= Q
        self.maf= int(moving_average_factor)
        self.dsf= int(down_sample_factor)
        self.BPF_list=[]
        for flist0 in self.mel.flist:
            bpf=Class_BPFtwice(fc=flist0, Q=self.Q, sampling_rate=self.sr, moving_average_factor=self.maf, down_sample_factor=self.dsf)
            self.BPF_list.append(bpf)
        # (3) compress via power function
        self.power_index= power_index
        self.comp1= Class_Compressor1(power_index= self.power_index)
        
        # (4)
        self.init0(save_file_path)
        
        #
    def init0(self, save_file_path="test"):
        #
        self.boxes_previous = None
        self.boxes_previous_score = None
        #
        self.savefile=save_file_path
        self.savefile_append= False
        self.class_number=0
        
    def compute(self, yg):
        # yg should be mono
        self.dwn_len= int(len(yg)/self.dsf)
        self.out1= np.empty( ( self.num_band, self.dwn_len), dtype=np.float32  )
        
        for i, bpf in enumerate( self.BPF_list ):
            print ('\r fc', bpf.fc, end='')
            self.out1[i]=self.comp1(bpf.filtering2( yg, self.dwn_len))
        
        print ('self.out1.shape', self.out1.shape)
        print ('max', np.amax(self.out1), ' min', np.amin(self.out1))
        
        return self.out1
    
    
    def trans_gray(self, indata0 ):
        # in_data0 dimension should be 2 zi-gen
        # convert to single Gray scale
        f= np.clip( indata0, 0.0, None)  # clip to >= 0
        # Normalize to [0, 255]
        f=  f / np.amax(f)  # normalize as max is 1.0
        fig_unit = np.uint8(np.around( f * 255))
        return fig_unit
    
    def conv_gray2RGBgray(self, in_fig ):
        # convert single Gray scale to RGB gray
        rgb_fig= np.zeros( (in_fig.shape[0],in_fig.shape[1], 3) )
        
        for i in range(3):
            rgb_fig[:,:,i] = 255 - in_fig
        
        return rgb_fig
    
    def conv_int255(self, in_fig):
        # matplotllib imshow x format was changed from version 2.x to version 3.x
        if 1:  # matplotlib > 3.x
            return np.array(np.abs(in_fig - 255), np.int)
        else:  # matplotlib = 2.x
            return in_fig
    
    def plot_image(self, LabelOn= True, rt_without_plotshow=False ):
        #
        self.fig_image= self.conv_gray2RGBgray( self.trans_gray(self.out1))
        
        # 
        fig, ax = plt.subplots()
        
        if LabelOn:
            ax.set_title('BPF bank analysis Spectrogram')
            ax.set_xlabel('time step [sec]')
            ax.set_ylabel('frequecny [Hz]')
        
        # draw time value
        self.xlen=self.fig_image.shape[1]
        
        if LabelOn:
            slen=self.xlen / ( self.sr/ self.dsf)
            char_slen=str( int(slen*1000) / 1000) # ms
            char_slen2=str( int((slen/2)*1000) / 1000) # ms
            ax.set_xticks([0,int(self.xlen/2)-1, self.xlen-1])
            ax.set_xticklabels(['0', char_slen2, char_slen])
        
        # draw frequecny value
        self.ylen=self.fig_image.shape[0]
        
        
        if LabelOn:
            flens=[self.fmin, 300, 1000, 3000,  self.fmax]
            # flens=[self.fmin, 300, 600, 1000, 1400, 2000, 3000,  self.fmax] # forMix_400Hz1KHz-10dB_44100Hz_400msec_TwoTube_mono.wav
            yflens,char_flens= self.mel.get_postion( flens)
            ax.set_yticks( yflens )
            ax.set_yticklabels( char_flens)
        else:
            ax.set_axis_off()
        
        self.img0= ax.imshow( self.conv_int255(self.fig_image), aspect='auto', origin='lower')
        
        plt.tight_layout()
        plt.savefig( self.savefile + '.jpg' , bbox_inches='tight', pad_inches = 0)
        if not rt_without_plotshow:
            plt.show()
    
def load_wav( path0):
    # return 
    #        yg: wav data (mono) 
    #        sr: sampling rate
    try:
        sr, y = wavread(path0)
    except:
        print ('error: wavread ', path0)
        sys.exit()
    else:
        yg= y / (2 ** 15)
        if yg.ndim == 2:  # if stereo
            yg= np.average(yg, axis=1)
    
    print ('file ', path0)
    print ('sampling rate ', sr)
    print ('length ', len(yg))
    return yg,sr



if __name__ == '__main__':
    #
    parser = argparse.ArgumentParser(description='Spectrogram output')
    parser.add_argument('--wav_file', '-w', default='./wav/test.wav', help='wav file name(16bit)')
    #parser.add_argument('--wav_file', '-w', default='./mp4audio/wav/Music_Video.wav', help='wav file name(16bit)')
    #parser.add_argument('--wav_file', '-w', default='./mp4audio/wav/Movies_soundtrack.wav', help='wav file name(16bit)')
    #parser.add_argument('--wav_file', '-w', default='./wav/Audio.wav', help='wav file name(16bit)')
    parser.add_argument('--out_dir', '-o', default='./result', help='specify output directory')
    args = parser.parse_args()
    
    path0= args.wav_file
    path_dir= args.out_dir + '/'
    
    # load compared two wav files
    yg0,sr0=load_wav( path0)
    
    # frame length  and shift length
    frame0= sr0 * 3
    shift0= int(frame0 * 0.75)
    all_frame = int((len(yg0) - frame0)/shift0)
    print ('total length [sec]', len(yg0)/sr0, ' frame size', frame0, ' shift size', shift0, ' frame number', all_frame)
    
    # get file name without ext
    path1= pathlib.PurePath(path0).stem
    save_file_path= path_dir + path1
    print ('save path', save_file_path)
    
    # instance
    Ana0= Class_Analysis1(num_band=1024, fmin=40, fmax=8000, sr=sr0)
    
    # process one frame. shift and process next frame
    for loop in range(all_frame):
        #
        Ana0.init0(save_file_path=save_file_path+'_' + str(loop))
        # process
        yo0= Ana0.compute(yg0[shift0*loop : shift0*loop + frame0] )
        
        # draw image,  if LabelOn is set to True, it will show time step and frequecny
        Ana0.plot_image(LabelOn=False, rt_without_plotshow=True) 
        

