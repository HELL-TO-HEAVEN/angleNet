"""
     need a console ?

     Chen Y. Liang
     Apr 29, 2017
"""
import matplotlib
matplotlib.use('Qt4Agg')
import numpy as np
from easydict import EasyDict as edict
import logging, time, os
import mxnet as mx


#logger= logging.getLogger('angleNet Logger')



config = edict()

config.it=edict()
config.it.debug=edict()
config.it.debug.debug =   True
config.it.debug.feat_shape=None#[5,4]#None # #  [1,3,6,6]

"""
   Referenced by angleIter.py

labelName: used for anchor-wise regression
stride: pixels(in raw img) between to neighbor anchors' centrs
sideLength: \sqrt{Aera} ,Aera is fixed for one sideLength wrt. angleD
"""
config.ANCHOR_angleD=(0,60,-60) #(-60,)#  # degree
config.ANCHOR_HoW=(1.5,3)   #(3,)#     #   rh over rw
config.ANCHOR_sideLength=(60,80)
config.ANCHOR_stride =None#  deprecated, calculated in angleIter.py automatically  240#16# (250,250)#

config.class_num=2   # only building and background

config.debug=edict()
config.debug.debug= True
config.debug.it = edict()
config.debug.it.anchor_num = 60  # randomly show some of anchors on the figure in angleIter.next()

config.it.scale=400

config.it.imgPath='../data/%d'%config.it.scale#img'   #  angleNet/lab/it/angleIter.py
config.it.labelFile='../data/angleList-%d.txt'%config.it.scale
config.it.epoch=3
config.it.iteration=40#00#*1000
config.it.dataNames=['data','rpn_inside_weight','rpn_outside_weight']    #  gdt: label, x, y, alphaR, rh, rw     will be used after proposal operation
config.it.labelNames=['target_label','target_bbox']         #  target_label ONLY indicats wheather it is object
config.it.shuffle=True
config.it.ioudir = '../data/iou/%d/'%config.it.scale  #  pre-calculate iou to a file for each image, it contains all .npz 
config.it.mean=[123.68, 116.28, 103.53]


config.train=edict()
config.train.ctx = mx.gpu()#mx.cpu()
config.train.iou_x_num=10     # referenced by angleIter.py
config.train.THRESHOLD_OBJECT=.6  # ref by  angleIter.py
config.train.THRESHOLD_BACKGD =.2
config.train.rpn_batch_size=128
config.train.rpn_fg_frac   =.5
config.train.rpn_bbx_weight=[10., 10., 10., 20., 20.]  # x,y,alphaR,rh,rw rpn_inside_weight
#config.train.rpn_bbox_outside_weight = 
#config.train.rpn_bbox_inside_weight
config.train.rpn_postive_weight=.6
config.train.lr=0.01
config.train.wd=1E-5
config.train.momentum=.9
config.train.timeStamp=time.asctime()
config.train.outputPath='../output/'
config.train.save_prefix=os.path.join(config.train.outputPath, config.train.timeStamp+'_angleD='+str(config.ANCHOR_angleD)+\
                         ';HoW='+str(config.ANCHOR_HoW)+';sideLength='+str(config.ANCHOR_sideLength) )
config.train.batch_size = 1  # do i forget this mean?
config.train.callbackBatch = 4
config.train.is_save = True


config.net=edict()
config.net.rpn_conv_name='relu5_3'
config.net.rpn_conv_names={'1x1':('relu5_3',),'2x2':('relu4_3', )}   #   used in the construction of the nets
config.net.symbol_path = '../model/vgg16'
config.net.params_epoch=0  # by default

config.type_num = len(config.ANCHOR_HoW)*len(config.ANCHOR_angleD)*len(config.ANCHOR_sideLength)


config.predict=edict()
config.predict.ctx=mx.gpu()

LOGFMT = '%(levelname)s: %(asctime)s %(filename)s [line: %(lineno)d]  %(message)s'

#logging.basicConfig(level=logging.DEBUG,format=LOGFMT)

filePathAndNname = config.train.outputPath+config.train.timeStamp+'-training.log'
if config.debug.debug:
	logging.basicConfig(level=logging.DEBUG,format=LOGFMT)
#        logger.setLevel(logging.DEBUG)
elif os.path.isdir(config.train.outputPath) :

	logging.basicConfig(level=logging.INFO,
            filename=filePathAndNname,
                    format=LOGFMT
            )

	console = logging.StreamHandler()
	logging.getLogger('').addHandler(console)
	formatter = logging.Formatter(LOGFMT)
	console.setFormatter(formatter)
        logging.info(filePathAndNname)

#assert 0


def nofile():
	if os.path.isfile(filePathAndNname):
		os.remove(filePathAndNname)
	logging.basicConfig(level=logging.INFO,format=LOGFMT)
