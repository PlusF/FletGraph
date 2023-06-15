import flet as ft
import numpy as np
import pandas as pd
from constants import ENVIRONMENT, CONDITION


def create_table_from_df(df: pd.DataFrame, selected_indices: list[int], select_handler, sort_handler):
    table = ft.DataTable(
        data_row_color={ft.MaterialState.HOVERED: "0x300000FF"},
        show_checkbox_column=True,
        columns=[
            ft.DataColumn(
                ft.Text(column),
                on_sort=sort_handler,
            ) for column in df.columns.tolist()[:4]
        ],
        rows=[
            ft.DataRow(
                [ft.DataCell(ft.Text(val)) for val in row[:4]],
                selected=index in selected_indices,
                on_select_changed=select_handler,
            ) for index, row in df.iterrows()
        ],
    )

    return table


def create_table_view(page: ft.Page, navbar: ft.NavigationBar, df: pd.DataFrame,
                      selected_indices: list[int], sort_info: list[ft.DataColumnSortEvent], filter_info: list[dict]):
    def select_handler(e: ft.ControlEvent):
        # 行が選択されたらチェックをつける
        e.control.selected = True if e.data == 'true' else False
        page.update()
        # ページが切り替わった後も忘れないように，ミュータブルなリストに情報を入れておく
        filename = e.control.cells[3].content.value
        index = np.where(df['filename'] == filename)[0][0]
        if e.control.selected:  # 追加
            selected_indices.append(index)
        else:  # 削除
            selected_indices.remove(index)

    def sort_handler(e: ft.DataColumnSortEvent):
        # 列をクリックでソート（もう一度クリックで昇順/降順切り替え）
        df_sorted = df.sort_values(df.columns[e.column_index], ascending=e.ascending)
        table.sort_column_index = e.column_index
        table.sort_ascending = e.ascending
        table.rows = [
            ft.DataRow(
                [ft.DataCell(ft.Text(val)) for val in row[:4]],
                selected=index in selected_indices,
                on_select_changed=select_handler,
            ) for index, row in df_sorted.iterrows()
        ]
        page.update()
        # ページが切り替わった後も忘れないように，ミュータブルなリストに情報を入れておく
        sort_info[0] = e

    switch_env = ft.Ref[ft.Switch]()
    dropdown_env = ft.Ref[ft.Dropdown]()
    switch_nd = ft.Ref[ft.Switch]()
    dropdown_nd = ft.Ref[ft.Dropdown]()
    switch_cond = ft.Ref[ft.Switch]()
    dropdown_cond = ft.Ref[ft.Dropdown]()

    def apply_filter(e=None):
        if e is None:  # 画面が切り替わったとき，filter_infoの内容と合致させる
            for key, value in filter_info[0].items():
                if key == 'switch_env':
                    switch_env.current.value = value
                elif key == 'dropdown_env':
                    dropdown_env.current.value = value
                elif key == 'switch_nd':
                    switch_nd.current.value = value
                elif key == 'dropdown_nd':
                    dropdown_nd.current.value = value
                elif key == 'switch_cond':
                    switch_cond.current.value = value
                elif key == 'dropdown_cond':
                    dropdown_cond.current.value = value

        # フィルタをかける
        df_filtered = df.copy(deep=True)
        if switch_env.current.value:
            filter_info[0]['switch_env'] = True
            filter_info[0]['dropdown_env'] = dropdown_env.current.value
            df_filtered = df_filtered[df_filtered['environment'] == dropdown_env.current.value]
        else:
            filter_info[0]['switch_env'] = False
        if switch_nd.current.value:
            filter_info[0]['switch_nd'] = True
            filter_info[0]['dropdown_nd'] = dropdown_nd.current.value
            df_filtered = df_filtered[df_filtered['ND filter'] == int(dropdown_nd.current.value)]
        else:
            filter_info[0]['switch_nd'] = False
        if switch_cond.current.value:
            filter_info[0]['switch_cond'] = True
            filter_info[0]['dropdown_cond'] = dropdown_cond.current.value
            df_filtered = df_filtered[df_filtered['condition'] == dropdown_cond.current.value]
        else:
            filter_info[0]['switch_cond'] = False

        # テーブルをアップデート
        table.rows = [
            ft.DataRow(
                [ft.DataCell(ft.Text(val)) for val in row[:4]],
                selected=index in selected_indices,
                on_select_changed=select_handler,
            ) for index, row in df_filtered.iterrows()
        ]
        page.update()

    table = create_table_from_df(df, selected_indices, select_handler, sort_handler)
    if sort_info[0] is not None:
        sort_handler(sort_info[0])

    cv = ft.Column([table], scroll=ft.ScrollMode.AUTO)
    rv = ft.Row([cv], expand=1, vertical_alignment=ft.CrossAxisAlignment.START)

    filters = ft.Row([
        ft.Row([
            ft.Switch(ref=switch_env, on_change=apply_filter),
            ft.Dropdown(ref=dropdown_env, options=[ft.dropdown.Option(name) for name in ENVIRONMENT.values()],
                        label='Environment', value=ENVIRONMENT[0], on_change=apply_filter),
        ]),
        ft.Row([
            ft.Switch(ref=switch_nd, on_change=apply_filter),
            ft.Dropdown(ref=dropdown_nd, options=[ft.dropdown.Option(name) for name in [1, 5, 10, 25, 32, 50, 100]],
                        label='ND filter', value="10", on_change=apply_filter),
        ]),
        ft.Row([
            ft.Switch(ref=switch_cond, on_change=apply_filter),
            ft.Dropdown(ref=dropdown_cond, options=[ft.dropdown.Option(name) for name in CONDITION.values()],
                        label='Condition', value=CONDITION[0], on_change=apply_filter),
        ])
    ], alignment=ft.MainAxisAlignment.CENTER)
    if len(filter_info[0]) > 0:
        apply_filter()

    return ft.View('table', [rv, filters], navigation_bar=navbar)
