import tkinter as tk
import customtkinter as ctk
from PresetConfig import ThemeManager, ButtonStyles, EntryStyles, LayoutSettings
from PIL import ImageColor


class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initialize theme manager
        self.theme_manager = ThemeManager(is_dark_mode=True)

        # Setup window
        window_settings = LayoutSettings.get_window_settings()
        self.title(window_settings["title"])
        self.geometry(window_settings["geometry"])
        self.resizable(*window_settings["resizable"])
        self.iconbitmap(window_settings["Logo"])

        # Set appearance mode
        ctk.set_appearance_mode(self.theme_manager.get_theme_mode())
        ctk.set_default_color_theme("blue")

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Configure main frame
        self.configure(fg_color=self.theme_manager.bg_color)

        # Theme Toggle Button
        theme_toggle_frame = ctk.CTkFrame(self, fg_color=self.theme_manager.bg_color)
        theme_toggle_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        theme_toggle_style = ButtonStyles.get_theme_toggle_style(self.theme_manager)
        self.theme_toggle = ctk.CTkButton(
            theme_toggle_frame, **theme_toggle_style, command=self.switch_theme
        )
        self.theme_toggle.pack(side=tk.LEFT, padx=(0, 0))

        # Entry frame
        entry_frame = ctk.CTkFrame(self, fg_color=self.theme_manager.bg_color)
        entry_frame.pack(fill=tk.X, padx=10, pady=(0, 0))

        # Entry field
        entry_style = EntryStyles.get_entry_style(self.theme_manager)
        self.entry = ctk.CTkEntry(entry_frame, **entry_style, state="readonly")
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Buttons frame
        buttons_frame = ctk.CTkFrame(self, fg_color=self.theme_manager.bg_color)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Button layout
        buttons = LayoutSettings.get_button_layout()
        grid_settings = LayoutSettings.get_grid_settings()

        # Configure grid with specific pixel dimensions
        for i in range(grid_settings["row_count"]):
            buttons_frame.grid_rowconfigure(i, minsize=grid_settings["row_minsize"])
        for i in range(grid_settings["col_count"]):
            buttons_frame.grid_columnconfigure(i, minsize=grid_settings["col_minsize"])

        # Create buttons with exact dimensions
        for text, btn_type, row, col in buttons:
            if btn_type == "number":
                button_style = ButtonStyles.get_number_button_style(
                    self.theme_manager, text
                )
            else:  # special
                button_style = ButtonStyles.get_special_button_style(
                    self.theme_manager, text
                )

            button = ctk.CTkButton(
                buttons_frame,
                **button_style,
                command=lambda t=text: self.on_button_click(t),
            )
            button.grid(
                row=row,
                column=col,
                padx=grid_settings["padx"],
                pady=grid_settings["pady"],
            )

        # Bind keyboard events to the main window
        self.bind("<Key>", self.handle_key_press)

    def handle_key_press(self, event):
        """Handle keyboard input, particularly numpad keys"""
        key = event.char
        keysym = event.keysym

        # Handle numeric keys (0-9)
        if key in "0123456789":
            self.on_button_click(key)

        # Handle operator keys
        elif key in "+-*/":
            # Map * to x for multiplication
            if key == "*":
                self.on_button_click("x")
            else:
                self.on_button_click(key)

        # Handle Enter/Return key as equals
        elif keysym in ("Return", "KP_Enter"):
            self.on_button_click("=")

        # Handle space as CE (clear)
        elif keysym == "space":
            self.on_button_click("CE")

        # Handle period as . (dot)
        elif keysym == "period":
            self.on_button_click(".")

        # Handle backspace to delete last character
        elif keysym == "BackSpace":
            current = self.entry.get()
            if current and current != "Erreur":
                self.entry.configure(state="normal")  # Temporarily enable to modify
                self.entry.delete(len(current) - 1, tk.END)
                self.entry.configure(state="readonly")  # Set back to readonly

        # Handle parentheses
        elif key in "()":
            self.on_button_click("( )")

        # Handle percentage key
        elif key == "%":
            self.on_button_click("%")

    def on_button_click(self, char):
        self.entry.configure(state="normal")  # Temporarily enable to modify

        if char == "CE":
            self.entry.delete(0, tk.END)  # Clear entry field
        elif char == "=":
            try:
                # Replace 'x' with '*' for proper evaluation
                expression = self.entry.get().replace("x", "*")
                result = eval(expression)  # Evaluate the expression
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))  # Display result
            except Exception:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Erreur")
        elif char == "+/-":
            try:
                current = self.entry.get()
                if current and current != "Erreur":
                    # Check if this is a simple number or an expression
                    operators = ["+", "-", "x", "/"]
                    has_operators = any(op in current for op in operators)

                    if not has_operators:
                        # Simple number - just toggle the sign
                        if current.startswith("-"):
                            self.entry.delete(0, tk.END)
                            self.entry.insert(0, current[1:])
                        else:
                            self.entry.delete(0, tk.END)
                            self.entry.insert(0, "-" + current)
                    else:
                        # This is an expression - toggle sign of the last number
                        # Find the last operator
                        last_op_index = max(
                            current.rfind(op) for op in operators if op in current
                        )

                        if last_op_index >= 0:
                            # Extract parts before and after the last operator
                            before = current[: last_op_index + 1]
                            after = current[last_op_index + 1 :]

                            # Check if there's already a negative sign after the operator
                            if after.startswith("-"):
                                new_expr = before + after[1:]
                            else:
                                new_expr = before + "-" + after

                            self.entry.delete(0, tk.END)
                            self.entry.insert(0, new_expr)
            except Exception:
                pass
        elif char == "( )":
            # Simple parentheses handling
            current = self.entry.get()
            open_count = current.count("(")
            close_count = current.count(")")
            if open_count > close_count:
                self.entry.insert(tk.END, ")")
            else:
                self.entry.insert(tk.END, "(")

        elif char == "%":
            try:
                current = self.entry.get()
                if current and current != "Erreur":
                    # Check if this is a simple number or an expression
                    operators = ["+", "-", "x", "/"]
                    has_operators = any(op in current for op in operators)

                    if not has_operators:
                        # Simple percentage of a number (converts to decimal)
                        value = float(current) / 100
                        self.entry.delete(0, tk.END)
                        self.entry.insert(0, str(value))
                    else:
                        # Handle percentage in an expression
                        # Find the last operator
                        last_op_index = max(
                            current.rfind(op) for op in operators if op in current
                        )

                        if last_op_index >= 0:
                            # Extract parts before and after the last operator
                            left_part = current[:last_op_index]
                            operator = current[last_op_index]
                            right_part = current[last_op_index + 1 :]

                            # If there's no left part (expression starts with operator), use 0
                            if not left_part and operator == "-":
                                left_part = "0"

                            # Calculate the percentage based on operator type
                            if operator in ["+", "-"]:
                                # For + and -, calculate percentage of left value
                                if left_part:
                                    left_value = eval(left_part.replace("x", "*"))
                                    percentage_value = (
                                        float(right_part) / 100
                                    ) * left_value
                                    new_expr = (
                                        left_part + operator + str(percentage_value)
                                    )
                                    self.entry.delete(0, tk.END)
                                    self.entry.insert(0, new_expr)
                            else:  # For * and /
                                # For * and /, simply convert to decimal
                                percentage_value = float(right_part) / 100
                                new_expr = left_part + operator + str(percentage_value)
                                self.entry.delete(0, tk.END)
                                self.entry.insert(0, new_expr)
            except Exception:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Erreur")

        else:
            self.entry.insert(tk.END, char)  # Append pressed button text

        # Set entry back to readonly after modifying
        self.entry.configure(state="readonly")

    def switch_theme(self):
        # Toggle theme and get new mode
        self.theme_manager.toggle_theme()

        # Update customtkinter appearance mode
        ctk.set_appearance_mode(self.theme_manager.get_theme_mode())

        # Update button icon
        self.theme_toggle.configure(
            text=self.theme_manager.get_theme_icon(),
            fg_color=self.theme_manager.special_bg,
            text_color=self.theme_manager.fg_color,
        )

        # Update main background
        self.configure(fg_color=self.theme_manager.bg_color)

        # Update entry field
        self.entry.configure(
            text_color=self.theme_manager.fg_color, fg_color=self.theme_manager.bg_color
        )

        # Update all buttons
        self.update_button_colors()

    def interpolate_color(self, old_color, new_color, factor):
        """Interpolates between two colors for smooth transitions."""
        # Convert hex to RGB
        old_rgb = ImageColor.getrgb(old_color)
        new_rgb = ImageColor.getrgb(new_color)

        # Blend colors
        blended_rgb = tuple(
            int(old_rgb[i] + (new_rgb[i] - old_rgb[i]) * factor) for i in range(3)
        )

        # Convert back to hex
        return f"#{blended_rgb[0]:02x}{blended_rgb[1]:02x}{blended_rgb[2]:02x}"

    def update_button_colors(self):
        for child in self.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                child.configure(fg_color=self.theme_manager.bg_color)

                for subchild in child.winfo_children():
                    if (
                        isinstance(subchild, ctk.CTkButton)
                        and subchild != self.theme_toggle
                    ):
                        # Check button type by color
                        is_special = any(
                            [
                                subchild.cget("fg_color")
                                == self.theme_manager.special_bg,
                                subchild.cget("fg_color")
                                == self.theme_manager.dark_special_bg,
                                subchild.cget("fg_color")
                                == self.theme_manager.light_special_bg,
                            ]
                        )

                        if is_special:
                            # Special button
                            subchild.configure(
                                fg_color=self.theme_manager.special_bg,
                                hover_color=self.theme_manager.active_bg,
                                text_color=self.theme_manager.fg_color,
                            )
                        else:
                            # Number button
                            subchild.configure(
                                fg_color=self.theme_manager.button_bg,
                                hover_color=self.theme_manager.hover_bg,
                                text_color=self.theme_manager.fg_color,
                            )


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
