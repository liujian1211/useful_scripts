import torch

class MyUnet(torch.nn.Module):
    def __init__(self):
        super(MyUnet,self).__init__()
        self.conv1_1 = torch.nn.Conv2d(in_channels=1,out_channels=64,kernel_size=3,stride=1,padding=0)
        self.relu1_1 = torch.nn.ReLU(inplace=True)
        self.conv1_2 = torch.nn.Conv2d(in_channels=64,out_channels=64,kernel_size=3,stride=1,padding=0)
        self.relu1_2 = torch.nn.ReLU(inplace=True)

        self.max_pool1 = torch.nn.MaxPool2d(kernel_size=2,stride=2)

        self.conv2_1 = torch.nn.Conv2d(in_channels=64,out_channels=128,kernel_size=3,stride=1,padding=0)
        self.relu2_1 = torch.nn.ReLU(inplace=True)
        self.conv2_2 = torch.nn.Conv2d(in_channels=128,out_channels=128,kernel_size=3,stride=1,padding=0)
        self.relu2_2 = torch.nn.ReLU(inplace=True)

        self.max_pool2 = torch.nn.MaxPool2d(kernel_size=2,stride=2)

        self.conv3_1 = torch.nn.Conv2d(in_channels=128,out_channels=256,kernel_size=3,stride=1,padding=0)
        self.relu3_1 = torch.nn.ReLU(inplace=True)
        self.conv3_2 = torch.nn.Conv2d(in_channels=256,out_channels=256,kernel_size=3,stride=1,padding=0)
        self.relu3_2 = torch.nn.ReLU(inplace=True)

        self.max_pool3 = torch.nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv4_1 = torch.nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, stride=1, padding=0)
        self.relu4_1 = torch.nn.ReLU(inplace=True)
        self.conv4_2 = torch.nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=0)
        self.relu4_2 = torch.nn.ReLU(inplace=True)

        self.max_pool4 = torch.nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv5_1 = torch.nn.Conv2d(in_channels=512,out_channels=1024,kernel_size=3,stride=1,padding=0)
        self.relu5_1 = torch.nn.ReLU(inplace=True)
        self.conv5_2 = torch.nn.Conv2d(in_channels=1024, out_channels=1024, kernel_size=3, stride=1, padding=0)
        self.relu5_2 = torch.nn.ReLU(inplace=True)

        self.up_conv1 = torch.nn.ConvTranspose2d(in_channels=1024,out_channels=512,kernel_size=2,stride=2)

        self.conv6_1 = torch.nn.Conv2d(in_channels=1024,out_channels=512,kernel_size=3,stride=1,padding=0)
        self.relu6_1 = torch.nn.ReLU(inplace=True)
        self.conv6_2 = torch.nn.Conv2d(in_channels=512,out_channels=512,kernel_size=3,stride=1,padding=0)
        self.relu6_2 = torch.nn.ReLU(inplace=True)

        self.up_conv2 = torch.nn.ConvTranspose2d(in_channels=512,out_channels=256,kernel_size=2,stride=2)

        self.conv7_1 = torch.nn.Conv2d(in_channels=512,out_channels=256,kernel_size=3,stride=1,padding=0)
        self.relu7_1 = torch.nn.ReLU(inplace=True)
        self.conv7_2 = torch.nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=0)
        self.relu7_2 = torch.nn.ReLU(inplace=True)

        self.up_conv3 = torch.nn.ConvTranspose2d(in_channels=256,out_channels=128,kernel_size=2,stride=2)

        self.conv8_1 = torch.nn.Conv2d(in_channels=256, out_channels=128, kernel_size=3, stride=1, padding=0)
        self.relu8_1 = torch.nn.ReLU(inplace=True)
        self.conv8_2 = torch.nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=0)
        self.relu8_2 = torch.nn.ReLU(inplace=True)

        self.up_conv4 = torch.nn.ConvTranspose2d(in_channels=128,out_channels=64,kernel_size=2,stride=2)

        self.conv9_1 = torch.nn.Conv2d(in_channels=128, out_channels=64, kernel_size=3, stride=1, padding=0)
        self.relu9_1 = torch.nn.ReLU(inplace=True)
        self.conv9_2 = torch.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=0)
        self.relu9_2 = torch.nn.ReLU(inplace=True)

        self.conv10 = torch.nn.Conv2d(in_channels=64,out_channels=2,kernel_size=1,stride=1,padding=0)  #卷积前后尺寸不变

    def crop(self,tensor,target_tensor):
        tensor_size = tensor.size()[2]
        target_tensor_size = target_tensor.size()[2]
        delta = (tensor_size - target_tensor_size) // 2
        ret_tensor = tensor[:,:,delta:tensor_size-delta,delta:tensor_size-delta]

        return ret_tensor

    def forward(self,x):
        x1 = self.conv1_1(x)
        x1 = self.relu1_1(x1)
        x2 = self.conv1_2(x1)
        x2 = self.relu1_2(x2)
        down1 = self.max_pool1(x2)

        x3 = self.conv2_1(down1)
        x3 = self.relu2_1(x3)
        x4 = self.conv2_2(x3)
        x4 = self.relu2_2(x4)
        down2 = self.max_pool2(x4)

        x5 = self.conv3_1(down2)
        x5 = self.relu3_1(x5)
        x6 = self.conv3_2(x5)
        x6 = self.relu3_2(x6)
        down3 = self.max_pool3(x6)

        x7 = self.conv4_1(down3)
        x7 = self.relu4_1(x7)
        x8 = self.conv4_2(x7)
        x8 = self.relu4_2(x8)
        down4 = self.max_pool4(x8)

        x9 = self.conv5_1(down4)
        x9 = self.relu5_1(x9)
        x10 = self.conv5_2(x9)
        x10 = self.relu5_2(x10)

        up_1 = self.up_conv1(x10)
        up1 = self.crop(x8,up_1)
        up1 = torch.cat((up_1,up1),dim=1)
        x11 = self.conv6_1(up1)
        x11 = self.relu6_1(x11)
        x12 = self.conv6_2(x11)
        x12 = self.relu6_2(x12)

        up_2 = self.up_conv2(x12)
        up2 = self.crop(x6,up_2)
        up2 = torch.cat((up_2,up2),dim=1)
        x13 = self.conv7_1(up2)
        x13 = self.relu7_1(x13)
        x14 = self.conv7_2(x13)
        x14 = self.relu7_2(x14)

        up_3 = self.up_conv3(x14)
        up3 = self.crop(x4,up_3)
        up3 = torch.cat((up_3,up3),dim=1)
        x15 = self.conv8_1(up3)
        x15 = self.relu8_1(x15)
        x16 = self.conv8_2(x15)
        x16 = self.relu8_2(x16)

        up_4 = self.up_conv4(x16)
        up4 = self.crop(x2,up_4)
        up4 = torch.cat((up_4,up4),dim=1)
        x17 = self.conv9_1(up4)
        x17 = self.relu9_1(x17)
        x18 = self.conv9_2(x17)
        x18 = self.relu9_2(x18)
        x19 = self.conv10(x18)

        return x19

if __name__ == '__main__':
    mytensor = torch.randn([1,1,572,572])
    mynet = MyUnet()

    ret = mynet(mytensor)
    print(ret.shape)
