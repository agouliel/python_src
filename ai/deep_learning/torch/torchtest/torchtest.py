# https://twitter.com/marlene_zw/status/1509882018968047618

import torch
from PIL import Image # pillow
import matplotlib.pyplot as plt
import matplotlib as mpl

model = torch.hub.load("bryandlee/animegan2-pytorch", "generator").eval()
face2paint = torch.hub.load("bryandlee/animegan2-pytorch:main", "face2paint", size=512)
img = Image.open('/Users/agou/Pictures/alex/alex-ionia.jpg').convert("RGB")
out = face2paint(model, img)
mpl.rcParams['figure.figsize'] = 11,8
fig,ax = plt.subplots(1,2)
ax[0].imshow(img)
ax[1].imshow(out)
plt.show()