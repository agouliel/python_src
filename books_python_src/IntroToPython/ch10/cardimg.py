import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import sys
sys.path.insert(0,'/Users/Shared/src/python_src/IntroToPython/ch10')

from pathlib import Path
path = Path('/Users/Shared/src/python_src/IntroToPython/ch10/card_images')

from deck import DeckOfCards

deck_of_cards = DeckOfCards()

figure, axes_list = plt.subplots(nrows=4, ncols=13)
for axes in axes_list.ravel():
    axes.get_xaxis().set_visible(False)
    axes.get_yaxis().set_visible(False)
    image_name = deck_of_cards.deal_card().image_name
    img = mpimg.imread(str(path.joinpath(image_name).resolve()))
    axes.imshow(img)
plt.show()
