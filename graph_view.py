import os
from datetime import datetime
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from utils import check_and_create_dir, smooth_1d, remove_cosmic_ray_1d, calc_tick_from_range
from constants import CMAPS


matplotlib.use("svg")

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 15

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0

plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['axes.linewidth'] = 1.0  # グラフ囲う線の太さ

plt.rcParams['legend.frameon'] = False  # 凡例を囲うかどうか、Trueで囲う、Falseで囲わない
plt.rcParams['legend.framealpha'] = 1.0  # 透過度、0.0から1.0の値を入れる
plt.rcParams['legend.facecolor'] = 'white'  # 背景色
plt.rcParams['legend.edgecolor'] = 'black'  # 囲いの色
plt.rcParams['legend.fancybox'] = False  # Trueにすると囲いの四隅が丸くなる

plt.rcParams['lines.linewidth'] = 1.0
plt.rcParams['figure.subplot.top'] = 0.95
plt.rcParams['figure.subplot.bottom'] = 0.2
plt.rcParams['figure.subplot.left'] = 0.05
plt.rcParams['figure.subplot.right'] = 0.65


def create_graph_view(
        page: ft.Page, navbar: ft.NavigationBar,
        fig: plt.Figure, ax: plt.Axes, graph_settings: dict,
        df: pd.DataFrame, selected_indices: list[int]):

    # 関数内で参照するための宣言
    normalization = ft.Ref[ft.Switch]()
    cosmic_ray_removal = ft.Ref[ft.Switch]()
    smoothing = ft.Ref[ft.Switch]()

    label_size = ft.Ref[ft.TextField]()
    tick_size = ft.Ref[ft.TextField]()
    cmap = ft.Ref[ft.Dropdown]()

    def draw(e=None):
        if e is not None:  # スイッチの変更があったとき
            graph_settings['normalization'] = normalization.current.value
            graph_settings['cosmic_ray_removal'] = cosmic_ray_removal.current.value
            graph_settings['smoothing'] = smoothing.current.value
            graph_settings['label_size'] = int(label_size.current.value)
            graph_settings['tick_size'] = int(tick_size.current.value)
            graph_settings['cmap'] = plt.get_cmap(cmap.current.value)
        # プロット
        ax.clear()
        for i, index in enumerate(selected_indices):
            env, nd, cond, filename, x, y = df.loc[index]
            if graph_settings['normalization']:
                y = y - y.min()
                y /= y.max()
            if graph_settings['cosmic_ray_removal']:
                y = remove_cosmic_ray_1d(y, 3, 7)
            if graph_settings['smoothing']:
                y = smooth_1d(y, 100)
                # normalize again
                if graph_settings['normalization']:
                    y = y - y.min()
                    y /= y.max()
            ax.plot(1240 / x, y,
                    label=f'{env}/{nd}%/{cond}',
                    color=graph_settings['cmap'](i / len(selected_indices)))
        ax.set_xlabel('Energy [eV]', fontsize=graph_settings['label_size'])
        ax.set_ylabel('Intensity [arb. units]', fontsize=graph_settings['label_size'])
        ticks, labels = calc_tick_from_range(*ax.get_xlim())
        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=labels, fontsize=graph_settings['tick_size'])
        ax.set_yticks([])
        if len(selected_indices) > 0:
            ax.legend(loc='center left', bbox_to_anchor=(1., .5))
        if e is not None:
            page.update()

    def save_fig(e):
        dirname = os.path.join(os.path.abspath(os.curdir), 'fig')
        check_and_create_dir(dirname)
        filename_to_save = datetime.now().isoformat().replace(':', '-') + '.png'
        full_path = os.path.join(dirname, filename_to_save)
        fig.savefig(full_path, transparent=True)
        # セーブしたことを知らせるダイアログを表示
        page.snack_bar = ft.SnackBar(
            ft.Text(f'Successfully saved: {full_path}'),
            duration=1500)
        page.snack_bar.open = True
        page.update()

    chart = MatplotlibChart(fig, expand=True)
    button_save = ft.ElevatedButton('Save', icon=ft.icons.SAVE_OUTLINED, on_click=save_fig, scale=1.5)

    draw()
    return ft.View('graph', [
        chart,
        ft.Row(
            [
                ft.Column([
                    ft.Switch(ref=normalization, label='Normalize', on_change=draw),
                    ft.Switch(ref=cosmic_ray_removal, label='Remove Cosmic Ray', on_change=draw),
                    ft.Switch(ref=smoothing, label='Smooth', on_change=draw)
                ]),
                ft.Column([
                    ft.TextField(ref=label_size, label='Label Size', value=str(graph_settings['label_size']), on_change=draw),
                    ft.TextField(ref=tick_size, label='Tick Size', value=str(graph_settings['tick_size']), on_change=draw)
                ]),
                ft.Dropdown(ref=cmap,
                            options=[ft.dropdown.Option(name) for name in CMAPS]
                            , label='Color Map', value=CMAPS[0], on_change=draw),
                button_save
            ],
            spacing=50,
            alignment=ft.MainAxisAlignment.CENTER),
    ], navigation_bar=navbar)
