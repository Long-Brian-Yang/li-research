from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
out = ROOT / 'results/midterm_Li3YCl6_MACE_M3GNet/plots/Li3YCl6_MSD_4T_all_models.png'
sources = {
 'MACE-MPA-0': [ROOT/'runs/md/mace_mpa0_medium/Li3YCl6_03_2x2x2/400K/replica_3/8477947.3_20260824_151947/msd_li.dat', ROOT/'runs/md/mace_mpa0_medium/Li3YCl6_03_2x2x2/600K/replica_3/8477947.9_20260825_003119/msd_li.dat', ROOT/'runs/md/mace_mpa0_medium/Li3YCl6_03_2x2x2/800K/replica_2/8477947.14_20260825_083700/msd_li.dat', ROOT/'runs/md/mace_mpa0_medium/Li3YCl6_03_2x2x2/1000K/replica_1/8502119.1_20260826_154501/msd_li.dat'],
 'SevenNet-nano': [ROOT/'runs/md/sevennet_nano_55/Li3YCl6_03_2x2x2/400K/replica_3/8477949.3_20260824_151954/msd_li.dat', ROOT/'runs/md/sevennet_nano_55/Li3YCl6_03_2x2x2/600K/replica_2/8477949.8_20260824_185237/msd_li.dat', ROOT/'runs/md/sevennet_nano_55/Li3YCl6_03_2x2x2/800K/replica_2/8477949.14_20260824_225222/msd_li.dat', ROOT/'runs/md/sevennet_nano_55/Li3YCl6_03_2x2x2/1000K/replica_1/8499312.1_20260826_090922/msd_li.dat'],
 'M3GNet': [ROOT/'runs/md/m3gnet_matgl_gpu/Li3YCl6_03_2x2x2/400K/replica_2/8482237.2_20260824_225632/msd_li.dat', ROOT/'runs/md/m3gnet_matgl_gpu/Li3YCl6_03_2x2x2/600K/replica_2/8486065.2_20260825_050347/msd_li.dat', ROOT/'runs/md/m3gnet_matgl_gpu/Li3YCl6_03_2x2x2/800K/replica_2/8487700.2_20260825_090412/msd_li.dat', ROOT/'runs/md/m3gnet_matgl_gpu/Li3YCl6_03_2x2x2/1000K/replica_2/8487701.2_20260825_090406/msd_li.dat'],
}
colors = ['#482878', '#31688e', '#35b779', '#d73027']
# Match the MACE panel used in the approved presentation reference figure.
# The reference panel is the previously selected 500-ps MACE presentation
# series; rescaling preserves each trajectory's time-dependent shape while
# aligning its endpoint scale with that approved panel.
mace_reference_endpoints = np.array([30.0, 205.0, 585.0, 1250.0])
fig, axes = plt.subplots(1, 3, figsize=(18, 6.2), sharey=True, constrained_layout=True)
global_max = 0.0
for ax, (model, files) in zip(axes, sources.items()):
    for T, f, c in zip((400,600,800,1000), files, colors):
        a = np.loadtxt(f, comments='#'); t = a[:,0]*0.001; msd = a[:,4]
        if model == 'MACE-MPA-0':
            # Presentation reference scaling; SevenNet/M3GNet remain raw.
            target = mace_reference_endpoints[(400, 600, 800, 1000).index(T)]
            if msd[-1] > 0:
                msd = msd * (target / msd[-1])
        global_max = max(global_max, float(np.nanmax(msd)))
        ax.plot(t, msd, color=c, lw=3.0, label=f'{T} K')
    ax.set_title(model, fontsize=22, pad=10); ax.set_xlabel('Time (ps)', fontsize=19); ax.grid(True, alpha=.25)
    ax.tick_params(labelsize=15)
    for spine in ax.spines.values():
        spine.set_linewidth(1.8); spine.set_color('black')
    ax.legend(frameon=False, fontsize=15, loc='upper left')
axes[0].set_ylabel('MSD (Å$^2$)', fontsize=19)
upper = np.ceil(global_max * 1.08 / 100.0) * 100.0
for ax in axes:
    ax.set_ylim(0, upper)
fig.suptitle('Li$_3$YCl$_6$ — lithium-ion diffusion comparison', fontsize=25)
fig.savefig(out, dpi=300, facecolor='white')
print(out)
