import glob
import os

classes = {0:[], 1:[], 2:[], 3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[],15:[],16:[],17:[],18:[],19:[]}
cls_txt = {0:'横向裂缝',1:'竖直裂缝',2:'坑槽',3:'龟裂',4:'路面标志',5:'轮胎印',6:'灌缝',7:'下水道井盖',
           8:'切割缝',9:'抛洒物',10:'路面积水',11:'修补块',12:'动物',13:'鞋',14:'破损的减速带',15:'影子',16:'缺失路面标志线',17:'破碎板',18:'错台',19:'www'}

train_folder_files = 'D:/samples_luzhou/326/labels'
# val_folder_files = '/home/ps/honghesong/ultralytics-main/damage_dataset_v8/labels/val/'

file_extension = '*.txt'

train_txt_files = glob.glob(os.path.join(train_folder_files,file_extension))
# val_txt_files = glob.glob(os.path.join(val_folder_files,file_extension))

for file in train_txt_files:
    with open(file, 'r') as file:
        for line in file:
            words = line.split()
            cls = words[0]
            # if(int(cls)==19):
            #     print('filename is ',file)
            for i in range(len(classes)):
                classes[i].append(i) if i==int(cls) else None

all =0
for j in range(len(classes)):
    print(f'{cls_txt[j]}的个数为：{len(classes[j])}')
    # print('classes[19]的个数为',len(classes[19]))
    #
    all += len(classes[j])
print('-----------------------')
print(f'总的类别数为：{all}')
