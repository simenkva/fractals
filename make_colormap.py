import colour
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt




def make_colormap(theme_colors, name=None, plot=False):
    n_theme = len(theme_colors)
    CAM16UCS = colour.convert(theme_colors, 'Hexadecimal', 'CAM16UCS')

    if name is None:
        name = 'colormap'

    for i in range(n_theme-1):
        gradient = colour.algebra.lerp(
            colour.algebra.smooth(np.linspace(0, 1, 256),0,1,clip=True)[..., np.newaxis],
            CAM16UCS[i][np.newaxis],
            CAM16UCS[i+1][np.newaxis],
        )

        RGB0 = colour.convert(gradient, 'CAM16UCS', 'Output-Referred RGB')
        if i == 0:
            RGB = RGB0
        else:
            RGB = np.vstack([RGB, RGB0])
        
    # make a colormap
    cmap = ListedColormap(np.clip(RGB, 0, 1), name=name)
    if plot:
        plot_colormap(cmap)
        
    return cmap
        



def plot_colormap(cmap, fig=None):
    # get name of cmap
    cmap_name = cmap.name
    if fig is None:
        fig = plt.figure()
    plt.figure(figsize=(8, 1))
    gradient = np.linspace(0, 1, 256)
    plt.imshow([gradient], aspect='auto', cmap=cmap)
    plt.subplots_adjust(top=0.95, bottom=0.05, left=0.2, right=0.99)
    plt.title(cmap_name, fontsize=20)
    

themes = {
    'terracottabeigeteal': ['#B85042', '#E7E8D1', '#A7BEAE'],
    'olivesalmon': ['#A1BE95', '#F98866'],
    'salmonpeach': ['#F98866', '#FFF2D7'],
    'charcoalrustblue': ['#2A3132','#763626', '#90AFC5'],
    }


cmaps = {}
for t in themes:
    cmaps[t] = make_colormap(themes[t], name=t)
    