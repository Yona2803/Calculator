import os


class ThemeManager:
    def __init__(self, is_dark_mode=True):
        self.is_dark_mode = is_dark_mode
        self.update_theme_colors()

    def define_colors(self):
        # Dark mode colors
        self.dark_bg = "#000000"
        self.dark_fg = "#ffffff"
        self.dark_button_bg = "#1A1A1A"
        self.dark_special_bg = "#DF8A6B"
        self.dark_hover_bg = "#DE754F"
        self.dark_active_bg = "#F98B63"

        # Light mode colors
        self.light_bg = "#ffffff"
        self.light_fg = "#000000"
        self.light_button_bg = "#E0E0E0"
        self.light_special_bg = "#DF8A6B"
        self.light_hover_bg = "#FFBBA2"
        self.light_active_bg = "#F98B63"

    def update_theme_colors(self):
        self.define_colors()

        if self.is_dark_mode:
            self.bg_color = self.dark_bg
            self.fg_color = self.dark_fg
            self.button_bg = self.dark_button_bg
            self.special_bg = self.dark_special_bg
            self.hover_bg = self.dark_hover_bg
            self.active_bg = self.dark_active_bg
        else:
            self.bg_color = self.light_bg
            self.fg_color = self.light_fg
            self.button_bg = self.light_button_bg
            self.special_bg = self.light_special_bg
            self.hover_bg = self.light_hover_bg
            self.active_bg = self.light_active_bg

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_theme_colors()
        return self.is_dark_mode

    def get_theme_mode(self):
        return "dark" if self.is_dark_mode else "light"

    def get_theme_icon(self):
        return "☀" if self.is_dark_mode else "🌙"


class ButtonStyles:
    @staticmethod
    def get_number_button_style(theme_manager, text):
        return {
            "text": text,
            "font": ("Jura", 32),
            "text_color": theme_manager.fg_color,
            "fg_color": theme_manager.button_bg,
            "hover_color": theme_manager.hover_bg,
            "width": 91,
            "height": 89,
            "corner_radius": 11,
        }

    @staticmethod
    def get_special_button_style(theme_manager, text):
        return {
            "text": text,
            "font": ("Jura", 32),
            "text_color": theme_manager.fg_color,
            "fg_color": theme_manager.special_bg,
            "hover_color": theme_manager.hover_bg,
            "width": 91,
            "height": 89,
            "corner_radius": 11,
        }

    @staticmethod
    def get_theme_toggle_style(theme_manager):
        return {
            "text": theme_manager.get_theme_icon(),
            "font": ("Jura", 16),
            "text_color": theme_manager.fg_color,
            "fg_color": theme_manager.special_bg,
            "hover_color": theme_manager.active_bg,
            "width": 40,
            "height": 40,
            "corner_radius": 8,
        }


class EntryStyles:
    @staticmethod
    def get_entry_style(theme_manager):
        return {
            "font": ("Jura", 90),
            "text_color": theme_manager.fg_color,
            "fg_color": theme_manager.bg_color,
            "border_width": 0,
            "height": 100,
            "justify": "right",
        }


class LayoutSettings:
    @staticmethod
    def get_button_layout():
        return [
            ("CE", "special", 1, 0),
            ("+/-", "special", 1, 1),
            ("%", "special", 1, 2),
            ("/", "special", 1, 3),
            ("7", "number", 2, 0),
            ("8", "number", 2, 1),
            ("9", "number", 2, 2),
            ("x", "special", 2, 3),
            ("4", "number", 3, 0),
            ("5", "number", 3, 1),
            ("6", "number", 3, 2),
            ("-", "special", 3, 3),
            ("1", "number", 4, 0),
            ("2", "number", 4, 1),
            ("3", "number", 4, 2),
            ("+", "special", 4, 3),
            ("( )", "number", 5, 0),
            ("0", "number", 5, 1),
            (".", "number", 5, 2),
            ("=", "special", 5, 3),
        ]

    @staticmethod
    def get_grid_settings():
        return {
            "row_minsize": 30,
            "col_minsize": 91,
            "row_count": 5,
            "col_count": 4,
            "padx": 2,
            "pady": 2,
        }

    @staticmethod
    def get_window_settings():
        return {
            "title": "Calculatror",
            "geometry": "400x685",
            "resizable": (False, False),
            "Logo": os.path.abspath("assets/Logo.ico"),
        }
