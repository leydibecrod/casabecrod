import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import contextily as ctx
from shapely.geometry import Polygon, LineString, Point
import math

# All solares data (UTM Zone 18S)
solares = [
    {'name': 'Mz32 - Valerio Santa Cruz', 'color': '#4CAF50',
     'verts': [(215590.311,9367198.3636),(215579.725,9367172.3284),(215563.0456,9367179.3414),(215573.037,9367205.374)],
     'sides': [28.11,18.09,27.88,18.64]},
    {'name': 'Mz32 - Guillermo Leon', 'color': '#66BB6A',
     'verts': [(215604.01,9367193.0352),(215593.647,9367167.0011),(215579.724,9367172.5498),(215590.0874,9367198.5102)],
     'sides': [28.02,14.99,27.95,14.96]},
    {'name': 'Mz32 - Sr. Onorato Becerra', 'color': '#2196F3',
     'verts': [(215647.7892,9367175.5857),(215637.2033,9367149.5505),(215615.1635,9367158.6069),(215625.4522,9367184.6407)],
     'sides': [28.11,23.83,27.99,24.10]},
    {'name': 'Mz33 - Alsides Briones', 'color': '#9C27B0',
     'verts': [(215682.1595,9367267.8781),(215692.151,9367293.9106),(215707.0415,9367288.0708),(215697.05,9367262.0383)],
     'sides': [27.88,15.99,27.88,15.99]},
    {'name': 'Mz33 - Pablo Hinostroza', 'color': '#FF9800',
     'verts': [(215665.0622,9367218.7053),(215675.1277,9367244.812),(215688.2308,9367239.7763),(215678.1653,9367213.6696)],
     'sides': [27.98,14.04,27.98,14.04]},
    {'name': 'Mz35 - Brijido Ramirez', 'color': '#00BCD4',
     'verts': [(215691.9285,9367210.6303),(215701.9199,9367236.6628),(215715.6186,9367231.4083),(215705.6271,9367205.3758)],
     'sides': [27.88,14.67,27.88,14.67]},
    {'name': 'Mz35 - Casa Comunal', 'color': '#80CBC4',
     'verts': [(215705.7758,9367205.3764),(215715.6173,9367231.7036),(215729.7619,9367226.4511),(215719.9204,9367200.1239)],
     'sides': [28.11,15.09,28.11,15.09]},
    {'name': 'Mz32 - Hildebran Becerra', 'color': '#1565C0',
     'verts': [(215628.6798,9367127.659),(215618.0938,9367101.6239),(215603.7979,9367107.4663),(215613.1948,9367133.4962)],
     'sides': [28.11,15.44,27.67,16.55]},
    {'name': 'Mz36 - Yovani Cayao, Jorge Lopez', 'color': '#F44336',
     'verts': [(215680.2483,9367163.3274),(215670.2569,9367137.295),(215655.9636,9367142.5468),(215665.9551,9367168.5793)],
     'sides': [27.88,15.23,27.88,15.23]},
    {'name': 'Mz36 - Sara Togas', 'color': '#D84315',
     'verts': [(215655.9636,9367142.5468),(215683.9582,9367131.4498),(215679.8464,9367120.2095),(215651.8518,9367131.3064)],
     'sides': [30.11,11.97,30.11,11.97]},
    {'name': 'Mz30 - Jesus Becerra', 'color': '#388E3C',
     'verts': [(215532.0887,9367188.0625),(215542.0775,9367214.6857),(215556.968,9367208.8459),(215546.9766,9367182.8134)],
     'sides': [28.44,15.99,27.88,15.79]},
    {'name': 'Mz29 - Abulio Arce', 'color': '#7B1FA2',
     'verts': [(215574.5831,9367258.5379),(215559.6927,9367264.3777),(215570.2787,9367290.413),(215585.1718,9367283.9825)],
     'sides': [15.99,28.11,16.22,27.56]},
    {'name': 'Mz33 - Opuesta Alcides', 'color': '#AB47BC',
     'verts': [(215622.0031,9367291.2347),(215631.9946,9367317.2673),(215646.885,9367311.4275),(215636.8936,9367285.3949)],
     'sides': [27.88,15.99,27.88,15.99]},
    {'name': 'Mz33 - Frente Abilio', 'color': '#5C6BC0',
     'verts': [(215603.4921,9367242.4247),(215613.4828,9367268.6049),(215625.6925,9367263.9344),(215615.5531,9367237.7535)],
     'sides': [28.02,13.07,28.08,12.93]},
    {'name': 'Mz30 - Sra. Yola (Karen)', 'color': '#26A69A',
     'verts': [(215513.2792,9367139.5465),(215523.268,9367166.1697),(215538.1584,9367160.3299),(215528.1671,9367134.2974)],
     'sides': [28.44,15.99,27.88,15.79]},
    {'name': 'Mz32 - Moises Marin', 'color': '#795548',
     'verts': [(215554.2275,9367156.8579),(215569.1179,9367151.0181),(215558.532,9367124.983),(215543.6415,9367130.8227)],
     'sides': [15.99,28.11,15.99,28.11]},
    {'name': 'Mz30 - Rupa Rustic', 'color': '#00897B',
     'verts': [(215472.5268,9367211.4216),(215482.5182,9367237.4542),(215497.4087,9367231.6144),(215487.4173,9367205.5819)],
     'sides': [27.88,15.99,27.88,15.99]},
    {'name': 'Mz30 - Esquina Sur Oeste Mz30', 'color': '#00695C',
     'verts': [(215453.7173,9367162.9055),(215463.7087,9367188.9381),(215478.5992,9367183.0983),(215468.6078,9367157.0658)],
     'sides': [27.88,15.99,27.88,15.99]},
    {'name': 'Mz29 - Pintado Huaman', 'color': '#6A1B9A',
     'verts': [(215515.0185,9367282.4877),(215500.72,9367288.9208),(215511.306,9367314.9561),(215526.1991,9367308.5256)],
     'sides': [15.68,28.11,16.22,28.34]},
    {'name': 'Mz29 - Esquina Nor Oeste Mz29', 'color': '#4A148C',
     'verts': [(215543.9663,9367357.4801),(215536.3194,9367338.9886),(215523.3632,9367344.394),(215531.0101,9367362.8856)],
     'sides': [20.01,14.04,20.01,14.04]},
    {'name': 'Mz29 - Op. Abilio Arce', 'color': '#9C27B0',
     'verts': [(215605.0226,9367332.3556),(215594.2872,9367306.4674),(215579.5441,9367312.6032),(215590.1308,9367338.4907)],
     'sides': [28.03,15.97,27.97,16.11]},
    {'name': 'Mz33 - Esquina SW', 'color': '#F44336',
     'verts': [(215588.0044,9367248.8524),(215597.6979,9367275.0313),(215609.9062,9367270.6561),(215600.2134,9367244.3296)],
     'sides': [27.92,12.97,28.05,13.02]},
    {'name': 'Wilder Coronel', 'color': '#FFB300',
     'verts': [(215467.6224,9367244.4752),(215457.631,9367218.4427),(215442.7405,9367224.2824),(215452.7319,9367250.315)],
     'sides': [27.88,15.99,27.88,15.99]},
    {'name': 'Esquina Sur Este Mz24', 'color': '#FF8F00',
     'verts': [(215448.5156,9367195.9578),(215438.2257,9367170.2192),(215423.3352,9367176.0589),(215433.9211,9367202.0942)],
     'sides': [27.72,15.99,28.11,15.83]},
]

# Manzana perimeters
mz_perimeters = {
    'Mz32': {
        'corners': [(215573.037,9367205.374),(215661.2083,9367170.2383),(215632.2513,9367096.0716),(215543.6415,9367130.8227)],
        'color': '#FFFFFF', 'labels': ['N:94.91m','E:79.62m','S:95.18m','W:80.14m']},
    'Mz33': {
        'corners': [(215678.1653,9367213.6696),(215707.0415,9367288.0708),(215619.1299,9367322.2722),(215589.9031,9367248.1490)],
        'color': '#FFEB3B', 'labels': ['SE:79.81m','NE:94.33m','NW:79.68m','SW:94.76m']},
    'Mz30': {
        'corners': [(215482.5182,9367237.4542),(215556.968,9367208.8459),(215528.1671,9367134.2974),(215453.7173,9367162.9055)],
        'color': '#00E676', 'labels': ['N:79.76m','E:79.92m','S:79.76m','W:79.92m']},
    'Mz29': {
        'corners': [(215531.0101,9367362.8856),(215605.0226,9367332.3556),(215574.5831,9367258.5379),(215500.72,9367288.9208)],
        'color': '#CE93D8', 'labels': ['N:80.06m','E:79.85m','S:79.87m','W:79.93m']},
}

# Alignment analysis data
pabloRef = (215678.1653, 9367213.6696)
alcidesRef = (215697.05, 9367262.0383)
onoV1 = (215647.7892, 9367175.5857)
onoV2 = (215637.2033, 9367149.5505)
brijidoV1 = (215691.9285, 9367210.6303)
brijidoV2 = (215701.9199, 9367236.6628)
yovaniV4 = (215665.9551, 9367168.5793)

# Line equation
refA = alcidesRef[1] - pabloRef[1]
refB = -(alcidesRef[0] - pabloRef[0])
refC = (alcidesRef[0] - pabloRef[0]) * pabloRef[1] - (alcidesRef[1] - pabloRef[1]) * pabloRef[0]
refNorm = math.sqrt(refA**2 + refB**2)

distOV1 = (refA * onoV1[0] + refB * onoV1[1] + refC) / refNorm
distOV2 = (refA * onoV2[0] + refB * onoV2[1] + refC) / refNorm

t1 = -(refA * onoV1[0] + refB * onoV1[1] + refC) / (refA**2 + refB**2)
projV1 = (onoV1[0] + refA * t1, onoV1[1] + refB * t1)
t2 = -(refA * onoV2[0] + refB * onoV2[1] + refC) / (refA**2 + refB**2)
projV2 = (onoV2[0] + refA * t2, onoV2[1] + refB * t2)

streetW = abs((refA * brijidoV1[0] + refB * brijidoV1[1] + refC) / refNorm)
distProjYov = math.sqrt((yovaniV4[0]-projV1[0])**2 + (yovaniV4[1]-projV1[1])**2)

# Create figure - 6000x6000px
fig, ax = plt.subplots(1, 1, figsize=(50, 50), dpi=100)

# Compute bounds
all_x = []
all_y = []
for s in solares:
    for v in s['verts']:
        all_x.append(v[0])
        all_y.append(v[1])
for mz in mz_perimeters.values():
    for c in mz['corners']:
        all_x.append(c[0])
        all_y.append(c[1])

pad = 40
xmin, xmax = min(all_x) - pad, max(all_x) + pad
ymin, ymax = min(all_y) - pad, max(all_y) + pad

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# Add satellite basemap (EPSG:32718 = UTM Zone 18S)
try:
    google_sat = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
    ctx.add_basemap(ax, crs='EPSG:32718',
                    source=google_sat,
                    zoom=18, attribution='')
    print("Satellite basemap added")
except Exception as e:
    print(f"Basemap error: {e}")
    ax.set_facecolor('#1a1a2e')

# Draw manzana perimeters
for mz_name, mz in mz_perimeters.items():
    corners = mz['corners'] + [mz['corners'][0]]
    xs = [c[0] for c in corners]
    ys = [c[1] for c in corners]
    ax.plot(xs, ys, color=mz['color'], linewidth=2, linestyle='--', alpha=0.85, zorder=5)

    # Center label
    cx = np.mean([c[0] for c in mz['corners']])
    cy = np.mean([c[1] for c in mz['corners']])
    ax.text(cx, cy, mz_name, fontsize=14, fontweight='bold', color=mz['color'],
            ha='center', va='center', zorder=10,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7, edgecolor=mz['color']))

    # Side labels
    for i in range(4):
        j = (i+1)%4
        mx = (mz['corners'][i][0] + mz['corners'][j][0]) / 2
        my = (mz['corners'][i][1] + mz['corners'][j][1]) / 2
        ax.text(mx, my, mz['labels'][i], fontsize=8, color=mz['color'],
                ha='center', va='center', zorder=10,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.6))

# Draw solares
for solar in solares:
    verts = solar['verts'] + [solar['verts'][0]]
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]

    # Fill
    from matplotlib.patches import Polygon as MPoly
    poly = MPoly(solar['verts'], closed=True, facecolor=solar['color'], alpha=0.35,
                 edgecolor=solar['color'], linewidth=2, zorder=6)
    ax.add_patch(poly)

    # Center label
    cx = np.mean([v[0] for v in solar['verts']])
    cy = np.mean([v[1] for v in solar['verts']])
    short_name = solar['name'].split(' - ')[1] if ' - ' in solar['name'] else solar['name']
    ax.text(cx, cy, short_name, fontsize=8, fontweight='bold', color='white',
            ha='center', va='center', zorder=12,
            path_effects=[matplotlib.patheffects.withStroke(linewidth=3, foreground='black')])

    # Vertex markers + labels
    for i, v in enumerate(solar['verts']):
        ax.plot(v[0], v[1], 'o', color='white', markersize=4, markeredgecolor=solar['color'],
                markeredgewidth=1.5, zorder=11)
        ax.text(v[0]+1.5, v[1]+1, f'V{i+1}', fontsize=6, color='white', zorder=11,
                path_effects=[matplotlib.patheffects.withStroke(linewidth=2, foreground='black')])

    # Side distances
    for i in range(len(solar['verts'])):
        j = (i+1) % len(solar['verts'])
        mx = (solar['verts'][i][0] + solar['verts'][j][0]) / 2
        my = (solar['verts'][i][1] + solar['verts'][j][1]) / 2
        ax.text(mx, my, f'{solar["sides"][i]}m', fontsize=6, color='white',
                ha='center', va='center', zorder=12,
                bbox=dict(boxstyle='round,pad=0.15', facecolor='#2196F3', alpha=0.85, edgecolor='none'))

# Lado Mz24: Wilder Coronel V1 -> Esquina SE Mz24 V2
wilderV1 = (215467.6224, 9367244.4752)
esqSEMz24V2 = (215438.2257, 9367170.2192)
ladoMz24Dist = math.sqrt((wilderV1[0]-esqSEMz24V2[0])**2 + (wilderV1[1]-esqSEMz24V2[1])**2)
ax.plot([wilderV1[0], esqSEMz24V2[0]], [wilderV1[1], esqSEMz24V2[1]],
        color='#FFFFFF', linewidth=2, linestyle='--', alpha=0.8, zorder=5)
ax.text((wilderV1[0]+esqSEMz24V2[0])/2 - 3, (wilderV1[1]+esqSEMz24V2[1])/2,
        f'Mz24: {ladoMz24Dist:.2f}m', fontsize=8, color='white', ha='right', va='center', zorder=12,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.6))

# Alignment lines (yellow dashed) - extended to full street projection
lineDx = alcidesRef[0] - pabloRef[0]
lineDy = alcidesRef[1] - pabloRef[1]
lineLen = math.sqrt(lineDx**2 + lineDy**2)
lineUx, lineUy = lineDx / lineLen, lineDy / lineLen

# West alignment line: Pablo V4 -> Alcides V4, extended south to Hildebran V2, north to Opuesta Alcides V2
opAlcidesV2_ref = (215631.9946, 9367317.2673)
hildebranV2 = (215618.0938, 9367101.6239)
tHildW = (hildebranV2[0] - pabloRef[0]) * lineUx + (hildebranV2[1] - pabloRef[1]) * lineUy
tOpAlcW = (opAlcidesV2_ref[0] - pabloRef[0]) * lineUx + (opAlcidesV2_ref[1] - pabloRef[1]) * lineUy
extA = (pabloRef[0] + lineUx * tHildW, pabloRef[1] + lineUy * tHildW)
extB = (pabloRef[0] + lineUx * tOpAlcW, pabloRef[1] + lineUy * tOpAlcW)
ax.plot([extA[0], extB[0]], [extA[1], extB[1]], color='#FFD600', linewidth=2.5,
        linestyle='--', alpha=0.9, zorder=7, label='Alineacion Jr. Moyobamba')

# East alignment line: Brijido V1 -> V2, extended south to Hildebran V2, north to Alcides V3
alcidesV3_ref = (215707.0415, 9367288.0708)
tHildE = (hildebranV2[0] - brijidoV1[0]) * lineUx + (hildebranV2[1] - brijidoV1[1]) * lineUy
tAlcV3E = (alcidesV3_ref[0] - brijidoV1[0]) * lineUx + (alcidesV3_ref[1] - brijidoV1[1]) * lineUy
ext2A = (brijidoV1[0] + lineUx * tHildE, brijidoV1[1] + lineUy * tHildE)
ext2B = (brijidoV1[0] + lineUx * tAlcV3E, brijidoV1[1] + lineUy * tAlcV3E)
ax.plot([ext2A[0], ext2B[0]], [ext2A[1], ext2B[1]], color='#FFD600', linewidth=2.5,
        linestyle='--', alpha=0.9, zorder=7)

# Street width line (green)
ax.plot([pabloRef[0], brijidoV1[0]], [pabloRef[1], brijidoV1[1]], color='#4CAF50',
        linewidth=2.5, zorder=8)
mx = (pabloRef[0] + brijidoV1[0]) / 2
my = (pabloRef[1] + brijidoV1[1]) / 2
ax.text(mx, my + 2, f'Jr. Moyobamba: {streetW:.1f}m', fontsize=9, fontweight='bold',
        color='white', ha='center', va='bottom', zorder=12,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FF5722', alpha=0.9, edgecolor='none'))


# Cross street line (Punto ideal -> Yovani)
ax.plot([projV1[0], yovaniV4[0]], [projV1[1], yovaniV4[1]], color='#4CAF50',
        linewidth=2.5, zorder=8)
midpy = ((projV1[0]+yovaniV4[0])/2, (projV1[1]+yovaniV4[1])/2)
ax.text(midpy[0], midpy[1]+2, f'{distProjYov:.2f}m', fontsize=8, fontweight='bold',
        color='white', ha='center', va='bottom', zorder=12,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#FF5722', alpha=0.9, edgecolor='none'))

# --- Alignment analysis 2: Calle transversal (Mz30/Mz32 → Mz33) ---
valerioV4 = (215573.037, 9367205.374)
moisesV4 = (215543.6415, 9367130.8227)
conflV1 = (215588.0044, 9367248.8524)
conflV4 = (215600.2134, 9367244.3296)
jesusV3 = (215556.968, 9367208.8459)
karenV4Pt = (215528.1671, 9367134.2974)

ref2A_t = moisesV4[1] - valerioV4[1]
ref2B_t = -(moisesV4[0] - valerioV4[0])
ref2C_t = (moisesV4[0] - valerioV4[0]) * valerioV4[1] - (moisesV4[1] - valerioV4[1]) * valerioV4[0]
ref2Norm_t = math.sqrt(ref2A_t**2 + ref2B_t**2)

distCV1 = (ref2A_t * conflV1[0] + ref2B_t * conflV1[1] + ref2C_t) / ref2Norm_t
distCV4 = (ref2A_t * conflV4[0] + ref2B_t * conflV4[1] + ref2C_t) / ref2Norm_t
streetW2N = abs((ref2A_t * jesusV3[0] + ref2B_t * jesusV3[1] + ref2C_t) / ref2Norm_t)
streetW2S = abs((ref2A_t * karenV4Pt[0] + ref2B_t * karenV4Pt[1] + ref2C_t) / ref2Norm_t)

tc1 = -(ref2A_t * conflV1[0] + ref2B_t * conflV1[1] + ref2C_t) / (ref2A_t**2 + ref2B_t**2)
projCV1 = (conflV1[0] + ref2A_t * tc1, conflV1[1] + ref2B_t * tc1)
tc4 = -(ref2A_t * conflV4[0] + ref2B_t * conflV4[1] + ref2C_t) / (ref2A_t**2 + ref2B_t**2)
projCV4 = (conflV4[0] + ref2A_t * tc4, conflV4[1] + ref2B_t * tc4)

# Direction vector (Moises V4 -> Valerio V4, south to north)
line2Dx = valerioV4[0] - moisesV4[0]
line2Dy = valerioV4[1] - moisesV4[1]
line2Len = math.sqrt(line2Dx**2 + line2Dy**2)
line2Ux = line2Dx / line2Len
line2Uy = line2Dy / line2Len

# Orange line 1: Moises V4 -> Valerio V4 extended north to Opuesta Alcides V2 height
opAlcidesV2 = (215631.9946, 9367317.2673)
tOpAlc = (opAlcidesV2[0] - moisesV4[0]) * line2Ux + (opAlcidesV2[1] - moisesV4[1]) * line2Uy
e2LA = (moisesV4[0] - line2Ux * 20, moisesV4[1] - line2Uy * 20)
e2LB = (moisesV4[0] + line2Ux * tOpAlc, moisesV4[1] + line2Uy * tOpAlc)
ax.plot([e2LA[0], e2LB[0]], [e2LA[1], e2LB[1]], color='#FF9800', linewidth=2.5,
        linestyle='--', alpha=0.9, zorder=7)

# Orange line 2: Karen V4 -> Jesus V3 extended north to Op. Abilio Arce V1 height
opAbilioV1 = (215605.0226, 9367332.3556)
tOpAbilio = (opAbilioV1[0] - karenV4Pt[0]) * line2Ux + (opAbilioV1[1] - karenV4Pt[1]) * line2Uy
e2RA = (karenV4Pt[0] - line2Ux * 20, karenV4Pt[1] - line2Uy * 20)
e2RB = (karenV4Pt[0] + line2Ux * tOpAbilio, karenV4Pt[1] + line2Uy * tOpAbilio)
ax.plot([e2RA[0], e2RB[0]], [e2RA[1], e2RB[1]], color='#FF9800', linewidth=2.5,
        linestyle='--', alpha=0.9, zorder=7)

# Green street width line
ax.plot([valerioV4[0], jesusV3[0]], [valerioV4[1], jesusV3[1]], color='#4CAF50', linewidth=2.5, zorder=8)
smx2 = (valerioV4[0]+jesusV3[0])/2
smy2 = (valerioV4[1]+jesusV3[1])/2
ax.text(smx2-3, smy2, f'Calle: {(streetW2N+streetW2S)/2:.1f}m', fontsize=9, fontweight='bold',
        color='white', ha='right', va='center', zorder=12,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FF5722', alpha=0.9, edgecolor='none'))

# Red perpendicular lines from Conflictiva
ax.plot([conflV1[0], projCV1[0]], [conflV1[1], projCV1[1]], color='#F44336', linewidth=2.5, zorder=8)
mcv1 = ((conflV1[0]+projCV1[0])/2, (conflV1[1]+projCV1[1])/2)
ax.text(mcv1[0]+2, mcv1[1], f'{abs(distCV1):.2f}m', fontsize=8, fontweight='bold',
        color='white', ha='left', zorder=12,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#F44336', alpha=0.9, edgecolor='none'))

ax.plot([conflV4[0], projCV4[0]], [conflV4[1], projCV4[1]], color='#F44336', linewidth=2.5, zorder=8)
mcv4 = ((conflV4[0]+projCV4[0])/2, (conflV4[1]+projCV4[1])/2)
ax.text(mcv4[0]+2, mcv4[1], f'{abs(distCV4):.2f}m', fontsize=8, fontweight='bold',
        color='white', ha='left', zorder=12,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#F44336', alpha=0.9, edgecolor='none'))

ax.plot(projCV1[0], projCV1[1], 'o', color='#4CAF50', markersize=8, zorder=11)
ax.plot(projCV4[0], projCV4[1], 'o', color='#4CAF50', markersize=8, zorder=11)

# Mark NW projected corner of Mz33
ax.plot(215619.1299, 9367322.2722, 'o', color='#FFEB3B', markersize=10, zorder=11)

# Street name labels (centered between parallel street lines)
# Jr. Moyobamba: center between yellow west (Pablo→Alcides) and yellow east (Brijido V1→V2)
jrMoyoX = (215678.1653 + 215691.9285 + 215697.05 + 215701.9199) / 4
jrMoyoY = (9367213.6696 + 9367210.6303 + 9367262.0383 + 9367236.6628) / 4
ax.text(jrMoyoX, jrMoyoY, 'Jr. Moyobamba', fontsize=12, fontstyle='italic', fontweight='bold',
        color='#FFD600', ha='center', va='center', zorder=14, rotation=69,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='black', alpha=0.7, edgecolor='#FFD600', linewidth=1))

# Jr. Rioja: center between orange east (Valerio→Moises) and orange west (Karen→Jesus)
jrRiojaX = (valerioV4[0] + jesusV3[0] + moisesV4[0] + karenV4Pt[0]) / 4
jrRiojaY = (valerioV4[1] + jesusV3[1] + moisesV4[1] + karenV4Pt[1]) / 4
ax.text(jrRiojaX, jrRiojaY, 'Jr. Rioja', fontsize=12, fontstyle='italic', fontweight='bold',
        color='#FFD600', ha='center', va='center', zorder=14, rotation=69,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='black', alpha=0.7, edgecolor='#FFD600', linewidth=1))

# Av. Marginal - Fernando Belaunde Terry: E-W along south edge of Mz32
avMarX = (215543.6415 + 215632.2513) / 2
avMarY = (9367130.8227 + 9367096.0716) / 2 - 12
ax.text(avMarX, avMarY, 'Av. Marginal - Fernando Belaunde Terry', fontsize=11, fontstyle='italic', fontweight='bold',
        color='#FF9800', ha='center', va='center', zorder=14, rotation=-22,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='black', alpha=0.7, edgecolor='#FF9800', linewidth=1))

# Title
ax.text(xmax - 5, ymax - 5,
        'ZONIFICACION AGUAS CLARAS\nBarrio Dinamarca - Datos SUNARP\nDatum: WGS84 UTM 18S',
        fontsize=16, fontweight='bold', color='white', ha='right', va='top', zorder=15,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.8, edgecolor='#FFD600', linewidth=2))

# Legend
legend_items = []
for s in solares:
    legend_items.append(mpatches.Patch(color=s['color'], alpha=0.5, label=s['name']))
legend_items.append(plt.Line2D([0],[0], color='#FFD600', linestyle='--', linewidth=2, label='Alineacion Jr. Moyobamba'))
legend_items.append(plt.Line2D([0],[0], color='#4CAF50', linewidth=2, label='Ancho de calle'))
legend_items.append(plt.Line2D([0],[0], color='#FF9800', linestyle='--', linewidth=2, label='Alineacion calle transversal'))

for mz_name, mz in mz_perimeters.items():
    legend_items.append(plt.Line2D([0],[0], color=mz['color'], linestyle='--', linewidth=2, label=f'{mz_name} perimetro'))

leg = ax.legend(handles=legend_items, loc='lower left', fontsize=8, ncol=2,
                facecolor='black', edgecolor='#FFD600', labelcolor='white',
                framealpha=0.85)
leg.set_zorder(15)

ax.set_aspect('equal')
ax.set_xlabel('Este (m)', fontsize=10, color='white')
ax.set_ylabel('Norte (m)', fontsize=10, color='white')
ax.tick_params(colors='white', labelsize=8)
for spine in ax.spines.values():
    spine.set_edgecolor('white')

plt.tight_layout()
output = 'C:/Users/lucas/proyectos/casabecrod/barrio-dinamarca/exports/barrio_dinamarca_4K.png'
plt.savefig(output, dpi=100, bbox_inches='tight', facecolor='#111111')
print(f"Saved: {output}")

print("Done!")
