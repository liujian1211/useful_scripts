import torch
import torch.nn as nn

input_dim=5
hidden_dim=10
n_layer=1

lstm_layer = nn.LSTM(input_dim,hidden_dim,n_layer,batch_first=True)


batch_size = 1
seq_len = 1

inp = torch.randn(batch_size,seq_len,input_dim)  #(1,1,5)

hidden_state = torch.randn(n_layer,batch_size,hidden_dim)
cell_state = torch.randn(n_layer,batch_size,hidden_dim)
hidden = (hidden_state,cell_state)

out,hidden_ = lstm_layer(inp,hidden)
print(out.shape) #(1,1,10)