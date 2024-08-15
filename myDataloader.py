import os
import torch
import torchvision.transforms
from torch.utils.data import Dataset,DataLoader
from PIL import Image
from torchvision import transforms
import torchvision

class MyDataset(Dataset):
    def __init__(self,image_folder,label_folder,transform):
        super(MyDataset,self).__init__()
        self.image_folder = image_folder
        self.label_folder = label_folder
        self.transform = transform
        self.data = self.load_data()

    def load_data(self):
        image_data=[]
        label_data =[]
        data = []
        for image_name in os.listdir(self.image_folder):
            image_path = os.path.join(self.image_folder,image_name)
            image = Image.open(image_path)
            image = self.transform(image)
            image_data.append(image)

        for label_name in os.listdir(self.label_folder):
            label_path = os.path.join(self.label_folder,label_name)
            with open(label_path,'r') as f:
                label = f.read().strip()
            label_data.append(label)

        for image_,label_ in zip(image_data,label_data):
            data.append({'image':image_,'label':label_})
        return data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        data = self.data[index]
        return data['image'],data['label']

if __name__ == '__main__':
    image_folder = 'D:/damagedataset_v8/asphalt/images/val'
    label_folder = 'D:/damagedataset_v8/asphalt/labels/val'
    transform = torchvision.transforms.Compose([transforms.Resize((640,640)),
                                                transforms.ToTensor()])
    

    mydataset = MyDataset(image_folder,label_folder,transform)
    dataloader = DataLoader(mydataset,batch_size=100,shuffle=True)
    for i ,data in enumerate(dataloader):
        print(data[0].shape)
        print(len(data[1]))
        break