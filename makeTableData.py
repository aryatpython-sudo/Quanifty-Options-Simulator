import customtkinter as ctk
from CTkTable import *
import json
import basketList

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
    btn_buy = ctk.CTkButton(master, text="B", width=20, height=24, fg_color="#28a745", hover_color="#218838")
    
    btn_sell = ctk.CTkButton(master, text="S", width=20, height=24, fg_color="#dc3545", hover_color="#c82333")

    return btn_buy, btn_sell

basket = basketList.basket

def buy_clicked(row, data):
    basket.append(data[row] + ["BUY"])

def sell_clicked(row, data):
    basket.append(data[row] + ["SELL"])

def on_row_enter(e, row, data, btn_buy, btn_sell, table):
    if getattr(on_row_enter, "last_row", None) == row:
        return
    
    btn_buy.configure(command=lambda r=row: buy_clicked(r, data))
    btn_sell.configure(command=lambda r=row: sell_clicked(r, data))

    btn_buy.place(in_=table.frame[row, 1], relx=0.0, rely=0.5, anchor="w")
    btn_sell.place(in_=table.frame[row, 1], relx=1.0, rely=0.5, anchor="e")

def drawButtons(btn_buy, btn_sell, table, data):
    for r in range(1, table.rows):
        for c in range(table.columns):
            cell_frame = table.frame[r, c]

            cell_frame.bind("<Enter>", lambda e, row=r: on_row_enter(e, row, data, btn_buy, btn_sell, table))
            for widget in cell_frame.winfo_children():
                widget.bind("<Enter>", lambda e, row=r: on_row_enter(e, row, data, btn_buy, btn_sell, table))

def on_button_enter(e, row, data, table):
    if hasattr(on_button_enter, "last_row"):
        on_row_enter(e, on_button_enter.last_row, data, e.widget.master.children['!ctkbutton'], e.widget.master.children['!ctkbutton2'], e.widget.master, table)

def hideButtons(e, btn_buy, btn_sell, table):
    mouse_x, mouse_y = table.winfo_pointerxy()
    
    table_x = table.winfo_rootx()
    table_y = table.winfo_rooty()
    table_width = table.winfo_width()
    table_height = table.winfo_height()
    
    is_outside_x = mouse_x < table_x or mouse_x > (table_x + table_width)
    is_outside_y = mouse_y < table_y or mouse_y > (table_y + table_height)
    
    if is_outside_x or is_outside_y:
        btn_buy.place_forget()
        btn_sell.place_forget()
        
        if hasattr(on_row_enter, "last_row"):
            delattr(on_row_enter, "last_row")