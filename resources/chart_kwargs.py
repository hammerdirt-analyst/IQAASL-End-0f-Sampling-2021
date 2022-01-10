from matplotlib.colors import LinearSegmentedColormap
# chart kwargs
title_k = {'loc':'left', 'pad':14, 'linespacing':1.5, 'fontsize':12}
title_kr = {'loc':'right', 'pad':14, 'linespacing':1.5, 'fontsize':12}
title_k14 = {'loc':'left', 'pad':14, 'linespacing':1.5, 'fontsize':14}
title_k14r = {'loc':'right', 'pad':14, 'linespacing':1.5, 'fontsize':14}
xlab_k = {'labelpad':10, 'fontsize':12}
xlab_k14 = {'labelpad':10, 'fontsize':14}
xlabels_top = dict(labeltop=True, labelbottom=False, pad=12, labelsize=12)
no_xticks = dict(axis='x', which='both', width=0, length=0 )
label_r14 = dict(labelpad=14, loc='right', fontsize=14)

rotate_45 = dict(axis='x', which='both', labelrotation=45)
rotate_0 = dict(axis='x', which='both', labelrotation=0)

rotate_90 = dict(axis='x', which='both', labelrotation=90)

colors_palette = {
    "G156": "dimgray", 
    "G178": "teal",
    "G177": "darkslategray",
    "G200": "lightseagreen",
    "G27": "darkorange",
    "G30": "darkkhaki",
    "G67": "rosybrown",
    "G89": "salmon",
    "G95": "magenta",
    "G82": "maroon",
    "G79": "brown",
    "G208": "turquoise",
    "G124": "indigo",
    "G25": "chocolate",
    "G31": "goldenrod",
    "G21": "tan",
    "Gfrags": "brown",
    "Gfoam": "maroon",
    "G117": "cornsilk",
    "G941": "plum",
    "G74": "coral",
    "G112": "yellow",
    "G24": "navajowhite",
    "G23": "peru",
    "G100": "pink",
    "G32": "khaki",
    "G33": "lemonchiffon",
    "G35": "blue",
    "G211": "thistle",
    "G904": "lightgray",
    "G940": "tomato",
    "G106": "peru",
    "G10": "darkslateblue",
    "G70": "gold",
    "G98": "hotpink",
}

# colors for gradients
colors = ["beige", "navajowhite", "sandybrown", "salmon", "sienna"]
nodes = [0.0, 0.2, 0.6, 0.8, 1.0]
cmap2 = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))