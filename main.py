import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import re


def get_words(text):
    return re.compile('\w+').findall(text)


def read_song(file):
    lyrics = []
    with open(file) as song:
        lines = song.readlines()
        for l in lines:
            words = get_words(l)
            lyrics += [w.lower() for w in words]

    return lyrics


def add_color(word, colors, opt='seq'):
    if word in colors.keys():
        return colors[word], colors

    else:
        if opt=='seq':
            n = np.max(list(colors.values())) + 1
        elif opt=='rdn':
            n = np.random.randint(1, 100)

        colors[word] = n
        return n, colors


def get_cmap(colors, original_cmap):
    # define the colormap
    cmap = original_cmap
    # extract all colors from the .jet map
    cmaplist = [cmap(i) for i in range(cmap.N)]
    # force the first color entry to be black
    cmaplist[0] = (0, 0, 0, 1.0)
    # create the new map
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    # define the bins and normalize
    bounds = np.linspace(0, len(np.unique(list(colors.values()))), len(np.unique(list(colors.values())))+1)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    return cmap, norm

def repeat_matrix(words, opt='seq'):
    colors = {'':0}
    df = pd.DataFrame(np.zeros((len(words), len(words))))
    for ix1, row in df.iterrows():
        for ix2 in row.index:
            w1 = words[ix1]
            w2 = words[ix2]
            if w1==w2:
                n, colors = add_color(w1, colors, opt=opt)
                df.at[ix1, ix2] = n

    return df, colors



if __name__ == '__main__':

    opt= 'seq'
    song='holloback_girl'
    lyrics = read_song('songs/%s.txt' %song)

    matrix, colors = repeat_matrix(lyrics, opt=opt)
    cmap, norm = get_cmap(colors, mpl.cm.rainbow)

    plt.figure()
    plt.imshow(matrix, cmap=cmap, norm=norm)
    plt.axis('off')
    plt.title(song)
    plt.savefig('pictures/%s.png' %song)
    plt.show()