from pathlib import Path
import math
R=Path(__file__).resolve().parents[1]; A=R/'assets/projects'; A.mkdir(parents=True,exist_ok=True)
projects=[('animatter','Animatter.js','PHYSICS / INTERACTION SYSTEMS'),('aov-uabe','AOV UABE','UNITY / ASSET ENGINEERING'),('hok-betastudio','HOK BetaStudio','DESKTOP / INTERACTIVE WORLDS')]
for i,(slug,name,category) in enumerate(projects):
    lines=[]
    for j in range(24):
        x=650+j*22; h=45+(j*37+i*43)%125
        lines.append(f'<path d="M{x} 210V{210-h}l14 -9 9 9V210" fill="#093465" stroke="#218ed5"/>')
        for y in range(220-h,200,13): lines.append(f'<path d="M{x+4} {y}h12" stroke="#4edcff" opacity=".65"/>')
    motif=''
    if i==0:
        for j in range(5): motif+=f'<ellipse cx="900" cy="112" rx="{55+j*19}" ry="{22+j*9}" transform="rotate({j*32} 900 112)" fill="none" stroke="#70eaff" opacity=".7"/>'
    else:
        for j in range(3):
            x=820+j*55;y=60+j*14
            motif+=f'<path d="M{x} {y}l45 -24 45 24v65l-45 24 -45 -24Z M{x} {y}l45 24 45 -24 M{x+45} {y+24}v65" fill="#07548a" fill-opacity=".65" stroke="#70eaff" stroke-width="2"/>'
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="250" viewBox="0 0 1200 250"><defs><linearGradient id="bg"><stop stop-color="#08244a"/><stop offset=".65" stop-color="#075598"/><stop offset="1" stop-color="#082952"/></linearGradient><radialGradient id="halo"><stop stop-color="#168bff" stop-opacity=".7"/><stop offset="1" stop-color="#168bff" stop-opacity="0"/></radialGradient></defs><rect width="1200" height="250" fill="url(#bg)"/><ellipse cx="900" cy="110" rx="300" ry="180" fill="url(#halo)"/>{''.join(lines)}<path d="M550 250Q850 120 1200 175 M520 250Q850 110 1200 160" fill="none" stroke="#42bfff" opacity=".65"/>{motif}<g font-family="monospace"><text x="40" y="45" font-size="15" fill="#63e9ff">0{i+1} / {category}</text><text x="38" y="127" font-size="52" font-weight="bold" fill="#e5faff">{name}</text><text x="40" y="207" font-size="17" fill="#8ddfff">EXPLORE THE REPOSITORY ↗</text></g><path d="M0 249H1200" stroke="#42bfff"/></svg>'''
    (A/(slug+'.svg')).write_text(s,encoding='utf-8')
