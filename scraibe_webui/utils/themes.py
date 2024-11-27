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
        self.name = "forest_ocean_radial_gradient"

        # Set parameters for a radial gradient in light mode and fancy blocks
        super().set(
            # Radial gradient background for light mode
            background_fill_primary="radial-gradient(circle at center, #DADADA 20%, #E0E0E0 50%, #CFEFCF 100%)",

            # Component box styles
            block_background_fill="linear-gradient(120deg, #FFFFFF 0%, #F4F4F4 100%)",  # Light gradient for component boxes
            block_border_color="#CCCCCC",  # Light gray for box border
            block_border_width="1px",
            block_radius="15px",  # Rounded corners for a softer look
            block_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",  # Subtle shadow for depth

            # High contrast for main text and labels
            body_text_color="#1A1A1A",  # Very dark gray for primary text
            body_text_color_subdued="#333333",  # Darker gray for subdued text

            # Label (title) text for components
            block_title_text_color="#000000",  # Black for labels to improve contrast
            block_title_text_color_dark="#FFFFFF",  # White for labels in dark mode

            # Input fields
            input_background_fill="#FFFFFF",  # Pure white for inputs
            input_border_color="#666666",  # Darker gray border around input fields
            input_border_width="1px",

            # Primary button styling for light mode
            button_primary_background_fill="linear-gradient(120deg, *primary_300 0%, *primary_400 50%, *primary_500 100%)",
            button_primary_text_color="*neutral_50",
            button_primary_background_fill_hover="linear-gradient(120deg, *primary_400 0%, *primary_500 60%, *primary_600 100%)",

            # Dark mode settings with a subtle glow effect
            background_fill_primary_dark="radial-gradient(circle at center, #020924 10%, #01071A 50%, #000615 100%)",
            background_fill_secondary_dark="#01030D",
            button_primary_background_fill_dark="linear-gradient(120deg, *secondary_600 0%, *primary_500 60%, *primary_600 100%)",
            button_primary_background_fill_hover_dark="linear-gradient(120deg, *secondary_500 0%, *primary_500 60%, *primary_500 100%)",
            button_primary_text_color_dark="*neutral_50",
            block_shadow_dark="0 1px 3px rgba(255, 255, 255, 0.1)",
            button_secondary_shadow_hover="*shadow_drop_lg",
            button_primary_shadow_hover="0 1px 3px 0 *primary_200, 0 1px 2px -1px *primary_200",
            button_secondary_shadow_dark="none",
            button_primary_shadow_dark="none",
        )
