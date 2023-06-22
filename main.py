import matplotlib.pyplot as plt
import flet as ft
from graph_view import create_graph_view
from table_view import create_table_view
from database import get_df
from constants import CMAPS


def main(page: ft.Page):
    page.title = 'Graph'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 1300
    page.window_height = 900

    def nav_bar_clicked(e):
        page_number = int(e.data)
        if page_number == 0:
            page.go('/graph')
        elif page_number == 1:
            page.go('/table')

    navbar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.AUTO_GRAPH_OUTLINED, selected_icon=ft.icons.AUTO_GRAPH, label='Graph'),
            ft.NavigationDestination(icon=ft.icons.TABLE_CHART_OUTLINED, selected_icon=ft.icons.TABLE_CHART, label='Table'),
        ],
        on_change=nav_bar_clicked,
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    graph_settings = {
        'normalization': False,
        'cosmic_ray_removal': False,
        'smoothing': False,
        'min_x': 2.0,
        'max_x': 2.5,
        'label_size': 30,
        'tick_size': 20,
        'cmap': CMAPS[0]
    }
    df = get_df()
    selected_indices = [0]
    sort_info = [None]
    filter_info = [{}]

    def route_change(handler):
        troute = ft.TemplateRoute(handler.route)
        page.views.clear()
        if troute.match('/graph'):
            page.views.append(create_graph_view(page, navbar, fig, ax, graph_settings, df, selected_indices))
        elif troute.match('/table'):
            page.views.append(create_table_view(page, navbar, df, selected_indices, sort_info, filter_info))
        page.update()

    page.on_route_change = route_change
    page.go('/graph')


if __name__ == '__main__':
    ft.app(target=main)
