import customtkinter as ctk
from CTkTable import *
import json

import basketList
import graphMath

def getData():
    try:
        with open("options_data.json", "r") as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print("Error: Could not find options_data.json")
        return

    options_chain = json_data.get("options_chain", [])

    data = [["Call LTP", "STRIKE", "Put LTP"]]
    for option in options_chain:
        strike = option.get("strike_price", 0)
        ce = option.get("CE", {})
        pe = option.get("PE", {})

        row_data = [
            f"{ce.get('ltp', 0):.2f}",
            f"{strike:.2f}",
            f"{pe.get('ltp', 0):.2f}"
        ]
        data.append(row_data)

    return data

def create_table(master, data):
    table = CTkTable(
        master=master,
        row=len(data),
        column=len(data[0]),
        values=data,
        header_color="#1f538d",
        hover_color="gray30"
    )

    table.edit_row(
        0, 
        font=("Helvetica", 14, "bold"), 
        text_color="white"
    )

    return table

def addButtons(master, row):
    btn_buy_call = ctk.CTkButton(master, text="B", width=20, height=24, fg_color="#28a745", hover_color="#218838")
    btn_sell_call = ctk.CTkButton(master, text="S", width=20, height=24, fg_color="#dc3545", hover_color="#c82333")
    btn_buy_put = ctk.CTkButton(master, text="B", width=20, height=24, fg_color="#28a745", hover_color="#218838")
    btn_sell_put = ctk.CTkButton(master, text="S", width=20, height=24, fg_color="#dc3545", hover_color="#c82333")

    return btn_buy_call, btn_sell_call, btn_buy_put, btn_sell_put

basket = basketList.basket

def buy_call_clicked(row, data, ax, canvas):
    basket.append(data[row] + ["BUY", "CALL"])
    graphMath.drawGraph(ax, canvas)
    print(f"Added to basket: {data[row]} + ['BUY', 'CALL']")

def sell_call_clicked(row, data, ax, canvas):
    basket.append(data[row] + ["SELL", "CALL"])
    print(f"Added to basket: {data[row]} + ['SELL', 'CALL']")

def buy_put_clicked(row, data, ax, canvas):
    basket.append(data[row] + ["BUY", "PUT"])
    print(f"Added to basket: {data[row]} + ['BUY', 'PUT']")

def sell_put_clicked(row, data):
    basket.append(data[row] + ["SELL", "PUT"])
    print(f"Added to basket: {data[row]} + ['SELL', 'PUT']")

def on_row_enter(e, row, data, btn_buy_call, btn_sell_call, btn_buy_put, btn_sell_put, table, ax, canvas):
    if getattr(on_row_enter, "last_row", None) == row:
        return
    
    btn_buy_call.configure(command=lambda r=row: buy_call_clicked(r, data, ax, canvas))
    btn_sell_call.configure(command=lambda r=row: sell_call_clicked(r, data, ax, canvas))
    btn_buy_put.configure(command=lambda r=row: buy_put_clicked(r, data, ax, canvas))
    btn_sell_put.configure(command=lambda r=row: sell_put_clicked(r, data, ax, canvas))

    btn_buy_call.place(in_=table.frame[row, 1], relx=0.0, rely=0.5, anchor="w")
    btn_buy_put.place(in_=table.frame[row, 2], relx=0.0, rely=0.5, anchor="e")
    btn_sell_call.place(in_=table.frame[row, 1], relx=0.0, rely=0.5, anchor="e")
    btn_sell_put.place(in_=table.frame[row, 1], relx=1.0, rely=0.5, anchor="w")

def drawButtons(btn_buy_call, btn_sell_call, btn_buy_put, btn_sell_put, table, data, ax, canvas):
    for r in range(1, table.rows):
        for c in range(table.columns):
            cell_frame = table.frame[r, c]

            cell_frame.bind("<Enter>", lambda e, row=r: on_row_enter(e, row, data, btn_buy_call, btn_sell_call, btn_buy_put, btn_sell_put, table, ax, canvas))
            for widget in cell_frame.winfo_children():
                widget.bind("<Enter>", lambda e, row=r: on_row_enter(e, row, data, btn_buy_call, btn_sell_call, btn_buy_put, btn_sell_put, table, ax, canvas))

def on_button_enter(e, row, data, table):
    if hasattr(on_button_enter, "last_row"):
        on_row_enter(e, on_button_enter.last_row, data, e.widget.master.children['!ctkbutton'], e.widget.master.children['!ctkbutton2'], e.widget.master, table)

def hideButtons(e, btn_buy_call, btn_sell_call, btn_buy_put, btn_sell_put, table):
    mouse_x, mouse_y = table.winfo_pointerxy()
    
    table_x = table.winfo_rootx()
    table_y = table.winfo_rooty()
    table_width = table.winfo_width()
    table_height = table.winfo_height()
    
    is_outside_x = mouse_x < table_x or mouse_x > (table_x + table_width)
    is_outside_y = mouse_y < table_y or mouse_y > (table_y + table_height)
    
    if is_outside_x or is_outside_y:
        btn_buy_call.place_forget()
        btn_sell_call.place_forget()
        btn_buy_put.place_forget()
        btn_sell_put.place_forget()

        if hasattr(on_row_enter, "last_row"):
            delattr(on_row_enter, "last_row")