import customtkinter as ctk
from CTkTable import *
import json

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