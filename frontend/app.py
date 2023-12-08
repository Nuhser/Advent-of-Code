import customtkinter as ctk
import tkinter


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Advent of Code - Solution Tool")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (5x2)
        self.grid_columnconfigure((1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=300)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, padx=(10, 0), pady=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.year_label = ctk.CTkLabel(self.sidebar_frame, text="Year:", anchor="w")
        self.year_label.grid(row=0, column=0, padx=20, pady=(10, 0))

        self.year_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["2021", "2022", "2023"], command=self.change_year_event)
        self.year_optionmenu.grid(row=1, column=0, padx=20, pady=(0, 10))
        
        self.day_label = ctk.CTkLabel(self.sidebar_frame, text="Day:", anchor="w")
        self.day_label.grid(row=2, column=0, padx=20, pady=(10, 0))

        self.day_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["1", "2", "3"], command=self.change_day_event)
        self.day_optionmenu.grid(row=3, column=0, padx=20, pady=(0, 10))

        self.run_options_frame = ctk.CTkFrame(self.sidebar_frame)
        self.run_options_frame.grid(row=5, column=0, rowspan=1, padx=20, pady=(0, 10))

        self.run_mode = tkinter.IntVar(value=3)
        
        self.radio_button_1 = ctk.CTkRadioButton(master=self.run_options_frame, variable=self.run_mode, value=0, text="Only Parser")
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = ctk.CTkRadioButton(master=self.run_options_frame, variable=self.run_mode, value=1, text="Part 1")
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = ctk.CTkRadioButton(master=self.run_options_frame, variable=self.run_mode, value=2, text="Part 2")
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = ctk.CTkRadioButton(master=self.run_options_frame, variable=self.run_mode, value=3, text="Both Parts")
        self.radio_button_3.grid(row=4, column=2, pady=10, padx=20, sticky="n")


    def change_year_event(self, selected_option: str):
        pass


    def change_day_event(self, selected_option: str):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()