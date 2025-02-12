import importlib  # noqa: F401


class ThemeManager:
    def __init__(self):
        self.current_theme = "dark"  # default theme
        self.load_theme_resources()

    def load_theme_resources(self):
        if self.current_theme == "dark":
            import components.assets.dark_theme_rc as dark_theme_rc

            self.theme_rc = dark_theme_rc
        else:
            import components.assets.light_theme_rc as light_theme_rc

            self.theme_rc = light_theme_rc

    def switch_theme(self, theme):
        if theme not in ["dark", "light"]:
            raise ValueError("Theme must be 'dark' or 'light'")
        self.current_theme = theme
        self.load_theme_resources()


# Create a single instance of the ThemeManager
theme_manager = ThemeManager()
