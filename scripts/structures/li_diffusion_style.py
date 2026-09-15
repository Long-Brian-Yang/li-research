"""Presentation style only; never modify artist x/y data or axis limits."""
import textwrap

def apply_style(fig):
    axes=fig.axes
    grid=axes[0].get_subplotspec().get_gridspec()
    rows,cols=grid.nrows,grid.ncols
    fig.set_size_inches(7.2*cols,5.8*rows)
    fig.set_facecolor('white')
    for ax in axes:
        ax.set_facecolor('white')
        ax.title.set_text('\n'.join(textwrap.wrap(ax.get_title(),34)))
        ax.title.set_fontsize(22)
        ax.xaxis.label.set_fontsize(19)
        ax.yaxis.label.set_fontsize(19)
        ax.tick_params(labelsize=15,width=1.8)
        for spine in ax.spines.values():
            spine.set_linewidth(1.8)
            spine.set_color('black')
        for line in ax.lines:
            # Preserve dense raw traces as thinner lines, while matching the
            # approved 3 pt weight for summary curves. No data transformations.
            old=line.get_linewidth()
            line.set_linewidth(1.2 if old<=1 else 3)
            palette={'#32688e':'#31688e','#34ad86':'#35b779','#b73b46':'#d73027'}
            color=line.get_color()
            if isinstance(color,str):line.set_color(palette.get(color,color))
        ax.grid(True,alpha=.25)
        leg=ax.get_legend()
        if leg:
            leg.set_frame_on(False)
            for handle in leg.legend_handles:
                if hasattr(handle,'get_color'):
                    color=handle.get_color()
                    if isinstance(color,str):handle.set_color(palette.get(color,color))
                if hasattr(handle,'get_linewidth'):
                    handle.set_linewidth(1.2 if handle.get_linewidth()<=1 else 3)
            for t in leg.get_texts():
                t.set_text('\n'.join(textwrap.wrap(t.get_text(),27)))
                t.set_fontsize(15)
        for t in ax.texts:t.set_fontsize(15)
