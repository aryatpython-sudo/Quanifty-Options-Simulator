import matplotlib.pyplot as plt
import customtkinter as ctk
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

plt.style.use('dark_background')

root = ctk.CTk()
root.title("Quanifty Options Basket Simulator")
root.geometry("1200x600")
root.resizable(False, False)

main_container = ctk.CTkFrame(root, fg_color="transparent")
main_container.pack(fill="both", expand=True, padx=10, pady=10)
left_frame = ctk.CTkScrollableFrame(main_container, label_text="P/L Graph", width=450)
left_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))
right_frame = ctk.CTkFrame(main_container, fg_color="transparent", width=700)
right_frame.pack(side="right", fill="y") 

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#242424')
ax.set_facecolor('#242424')
# ax.set_title("Options Payoff Simulation", color='white', pad=15, fontsize=14)
ax.set_xlabel("Index Price", color='white', fontsize=12)
ax.set_ylabel("Profit / Loss", color='white', fontsize=12)

# UI design
# ax.spines['top'].set_color("#464646")
# ax.spines['right'].set_color("#464646")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('gray')
ax.spines['left'].set_color('gray')

ax.set_xlim(24000, 25000)
ax.set_ylim(-10000, 10000)

v_line = ax.axvline(x=0, color='gray', linestyle='--', alpha=0.7, visible=False)

coordinates_label = ctk.CTkLabel(right_frame, text="Hover over graph to see coordinates", font=("Arial", 12))
coordinates_label.pack(pady=10, padx=120, anchor="w")

fig.subplots_adjust(top=0.95)

canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

# def plot_point():
#     error_label.configure(text="")

#     try:
#         x_coord = float(entry_x.get())
#         y_coord = float(entry_y.get())
def onMouseMove(event):
    if event.inaxes == ax:
        x = event.xdata
        y = event.ydata

        coordinates_label.configure(text=f"X: {x:.0f} | Y: {y:.0f}")

        v_line.set_xdata([x, x])
        v_line.set_visible(True)

        canvas.draw_idle()

    else:
        coordinates_label.configure(text="Hover over graph to see coordinates")
        v_line.set_visible(False)
        canvas.draw_idle()

def on_closing():
    plt.close('all')
    root.quit()
    root.destroy()
    sys.exit(0)

canvas.mpl_connect('motion_notify_event', onMouseMove)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
