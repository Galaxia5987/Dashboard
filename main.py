import threading

import ntcore
from dash import Dash, ctx, html, Input, Output, callback

clicked_button_index = [1, 1]


def column_index_to_class_name(index, is_clicked):
    clicked = 'unclicked'
    if is_clicked:
        clicked = 'clicked'
    if index % 3 == 2:
        return clicked + '-cube-button'
    else:
        return clicked + '-cone-button'


def index_to_class_name(row_index, column_index, is_clicked):
    clicked = 'unclicked'
    if is_clicked:
        clicked = 'clicked'
    if row_index == 1:
        return column_index_to_class_name(column_index, is_clicked)
    elif row_index == 2:
        return column_index_to_class_name(column_index, is_clicked)
    else:
        return clicked + '-hybrid-button'


app = Dash(__name__)


@callback(
    *(Output('b' + str(i), 'className') for i in range(1, 10)),
    *(Output('m' + str(i), 'className') for i in range(1, 10)),
    *(Output('t' + str(i), 'className') for i in range(1, 10)),

    *(Input('t' + str(i), 'n_clicks') for i in range(1, 10)),
    *(Input('m' + str(i), 'n_clicks') for i in range(1, 10)),
    *(Input('b' + str(i), 'n_clicks') for i in range(1, 10)),

    prevent_initial_call=True
)
def update_output(n11, n12, n13, n14, n15, n16, n17, n18, n19,
                  n21, n22, n23, n24, n25, n26, n27, n28, n29,
                  n31, n32, n33, n34, n35, n36, n37, n38, n39):
    clicked_button = ctx.triggered_id

    if clicked_button[0] == 'b':
        clicked_button_index[0] = 1
    elif clicked_button[0] == 'm':
        clicked_button_index[0] = 2
    else:
        clicked_button_index[0] = 3

    clicked_button_index[1] = int(clicked_button[1])

    lst = []
    for i in range(1, 4):
        for j in range(1, 10):
            if (i != clicked_button_index[0]) | (j != clicked_button_index[1]):
                lst.append(index_to_class_name(i, j, False))
            else:
                lst.append(index_to_class_name(i, j, True))

    return tuple(lst)


app.layout = html.Div([
    *(html.Button('', id='b' + str(i), className=column_index_to_class_name(i, False), n_clicks=0,
                  style={'position': "absolute", 'left': 143 * (i - 1), 'bottom': 0}) for i in range(10)),
    *(html.Button('', id='m' + str(i), className=column_index_to_class_name(i, False), n_clicks=0,
                  style={'position': "absolute", 'left': 143 * (i - 1), 'bottom': 200}) for i in range(10)),
    *(html.Button('', id='t' + str(i), className='unclicked-hybrid-button', n_clicks=0,
                  style={'position': "absolute", 'left': 143 * (i - 1), 'bottom': 400}) for i in range(10)),
])


def switch_class_name(class_name, game_piece):
    if class_name == "unclicked-" + game_piece + "-button":
        return "clicked-" + game_piece + "-button"
    else:
        return "unclicked-" + game_piece + "-button"


inst = ntcore.NetworkTableInstance.getDefault()
inst.startServer()
pb_row_index = inst.getIntegerTopic("selected_row_index").publish()
pb_column_index = inst.getIntegerTopic("selected_column_index").publish()
pb_row_index.setDefault(0)
pb_column_index.setDefault(0)


def update_nt():
    while True:
        pb_row_index.set(clicked_button_index[0])
        pb_column_index.set(clicked_button_index[1])


if __name__ == '__main__':
    thread = threading.Thread(target=update_nt)
    thread.start()
    app.run(debug=False)
