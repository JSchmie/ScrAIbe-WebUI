import gradio as gr

from gradio.themes import colors, sizes, Font, GoogleFont

class ForestOceanTheme(gr.themes.Ocean):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.Color(
            c50="#E6F7E6", c100="#CFF0CF", c200="#A8E0A8", c300="#82D182",
            c400="#5BC25B", c500="#34B134", c600="#299229", c700="#1E731E",
            c800="#145514", c900="#0A370A", c950="#042704"
        ),
        secondary_hue: colors.Color | str = colors.Color(
            c50="#E6F7E6", c100="#A8E0A8", c200="#82D182", c300="#5BC25B",
            c400="#34B134", c500="#299229", c600="#1E731E", c700="#145514",
            c800="#0A370A", c900="#042704", c950="#001800"
        ),
        neutral_hue: colors.Color | str = colors.zinc,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_xxl,
        text_size: sizes.Size | str = sizes.text_md,
        font: Font | str | list[Font | str] = (
            GoogleFont("IBM Plex Sans"),
            "ui-sans-serif",
            "system-ui",
            "sans-serif",
        ),
        font_mono: Font | str | list[Font | str] = (
            GoogleFont("Inter"),
            "ui-monospace",
            "Consolas",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )

        # Name the theme for identification
        self.name = "forest_ocean"

        # Set primary button to a vibrant green gradient in light mode
        super().set(
            button_primary_background_fill="linear-gradient(120deg, *primary_300 0%, *primary_400 50%, *primary_500 100%)",  # Green gradient
            button_primary_text_color="*neutral_50",  # White text for contrast
            button_border_width="0px",
            checkbox_label_border_width="1px",
            button_transform_hover="scale(1.02)",
            button_transition="all 0.1s ease-in-out",
            slider_color="*primary_400",
            button_primary_background_fill_hover="linear-gradient(120deg, *primary_400 0%, *primary_500 60%, *primary_600 100%)",  # Darker gradient on hover
            button_secondary_background_fill="linear-gradient(120deg, *neutral_300 0%, *neutral_100 60%, *neutral_200 100%)",
            button_secondary_background_fill_hover="linear-gradient(120deg, *neutral_200 0%, *neutral_100 60%, *neutral_100 100%)",
            checkbox_label_background_fill_selected="linear-gradient(120deg, *primary_400 0%, *primary_300 60%, *primary_400 100%)",
            checkbox_label_border_color_selected="*primary_400",
            checkbox_background_color_selected="*primary_400",
            checkbox_label_text_color_selected="*button_secondary_text_color",
            slider_color_dark="*primary_500",
            button_secondary_background_fill_dark="linear-gradient(120deg, *neutral_700 0%, *neutral_600 60%, *neutral_700 100%)",
            button_secondary_background_fill_hover_dark="linear-gradient(120deg, *neutral_600 0%, *neutral_600 60%, *neutral_700 100%)",
            checkbox_label_background_fill_selected_dark="linear-gradient(120deg, *primary_600 0%, *primary_500 60%, *primary_600 100%)",
            checkbox_label_border_color_selected_dark="*primary_600",
            checkbox_background_color_selected_dark="*primary_600",
            checkbox_label_text_color_selected_dark="*button_secondary_text_color",
            block_shadow="*shadow_drop_lg",
            button_secondary_shadow_hover="*shadow_drop_lg",
            button_primary_shadow_hover="0 1px 3px 0 *primary_200, 0 1px 2px -1px *primary_200",
            button_secondary_shadow_dark="none",
            button_primary_shadow_dark="none",
        )