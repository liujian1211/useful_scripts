import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
from tensorflow import keras
from tensorflow.keras.datasets import imdb

MAX_WORDS = 10000  # imdb’s vocab_size 即词汇表大小
MAX_LEN = 200      # 处理后，每个句子的最大长度

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
(x_train0, y_train), (x_test0, y_test) = imdb.load_data(num_words=MAX_WORDS)
x_train =  keras.preprocessing.sequence.pad_sequences(
                      x_train0, maxlen=MAX_LEN,  padding="post",
                      truncating="post")
x_test =  keras.preprocessing.sequence.pad_sequences(
                  x_test0, maxlen=MAX_LEN,    padding="post",
                      truncating="post")

word_index = imdb.get_word_index()
# print(list(word_index.items())[0:5])

index_word = {val:key for key,val in word_index.items()}
# print(list(index_word.items())[0:5])

sentence_num = x_train[0]  #第0句
sentence_word = [index_word[word_num] for word_num in sentence_num]


BATCH_SIZE = 256
train_data = TensorDataset(torch.LongTensor(x_train),torch.LongTensor(y_train))
test_data = TensorDataset(torch.LongTensor(x_test),torch.LongTensor(y_test))

train_loader = DataLoader(train_data,batch_size=BATCH_SIZE,shuffle=True)
test_loader = DataLoader(test_data,batch_size=BATCH_SIZE,shuffle=False)

#每一个train_loader都是batch_size为256的影评及其极性的词条对

EMB_SIZE = 128
HID_SIZE = 128
DROPOUT = 0.2

class Model(nn.Module):
    def __init__(self,max_words,emb_size,hid_size,dropout):
        super().__init__(Model,self).__init__()
        self.max_words = max_words
        self.emb_size = emb_size
        self.hid_size = hid_size
        self.dropout = dropout
        self.Embedding = nn.Embedding(self.max_words,self.emb_size)  #最大词汇量，词向量维度（即每个词的表示维度）

        self.LSTM = nn.LSTM(self.emb_size,self.hid_size,num_layers=2,batch_first=True,bidirectional=True)
        self.dp = nn.Dropout(self.dropout)
        self.fc1 = nn.Linear(in_features=self.hid_size*2, out_features=self.hid_size)
        self.fc2 = nn.Linear(in_features=self.hid_size,out_features=2)
    def forward(self,x):
        x = self.Embedding(x)
        x = self.dp(x)
        x,_ = self.LSTM(x)
        x = self.dp(x)
        x = F.relu(self.fc1(x))
        x = F.avg_pool2d(x,(x.shape[1],1)).squeeze()

        out = self.fc2(x)
        return out

def train(model,train_loader,optimizer,epoch):
    model.train()
    criterion = nn.CrossEntropyLoss()
    for batch_idx,(x,y) in enumerate(train_loader):
        x,y = x.to(DEVICE),y.to(DEVICE)
        optimizer.zero_grad()
        y_ = model(x)
        loss = criterion(y_,y)
        loss.backward()
        optimizer.step()

        if(batch_idx+1)%10==0:
            done_len = batch_idx * len(x)
            total_len = len(train_loader.dataset)
            percent = 100.*batch_idx / len(train_loader)
            print(f'Train Epoch:{epoch} [{done_len} / {total_len} ({percent:.0f} %)]\t Loss:{loss.item():.6f}')

def test(model,test_loader):
    model.eval()
    criterion = nn.CrossEntropyLoss(reduction='sum')
    test_loss = 0
    acc =0
    for batch_idx, (x, y) in enumerate(test_loader):
        x, y = x.to(DEVICE), y.to(DEVICE)
        with torch.no_grad():
            y_ = model(x)
        test_loss += criterion(y_, y)
        # 下句的 .max() 输出分别为最大值和最大值的index
        pred = y_.max(-1, keepdim=True)[1]
        acc += pred.eq(y.view_as(pred)).sum().item()
    test_loss /= len(test_loader.dataset)
    test_total_len = len(test_loader.dataset)
    percent = 100. * acc / test_total_len
    print(f'Test set: Average loss: {test_loss:.4f},Accuracy: {acc} / {test_total_len}({percent: .0f} %)\n')

    return acc / len(test_loader.dataset)

model = Model(MAX_WORDS, EMB_SIZE, HID_SIZE,DROPOUT).to(DEVICE)
print(model)
optimizer = torch.optim.Adam(model.parameters())
best_acc = 0.0 # 最佳模型的正确率
PATH = 'model.pth'# 定义模型保存路径（最佳模型）

for epoch in range(1, 11): # 10个epoch
    train(model, train_loader, optimizer, epoch)
    acc = test(model, test_loader)
    if best_acc < acc:
        best_acc = acc
        torch.save(model.state_dict(), PATH)
    print(f"acc is: {acc :.4f}, best acc is {best_acc:.4f}")

