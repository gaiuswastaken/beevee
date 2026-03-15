from kivy.utils import get_color_from_hex

colourScheme = {

    # The main colours (honey) 
    "primary": get_color_from_hex("#C89B00"),  
    "onPrimary": get_color_from_hex("#FFFFFF"),

    "primaryContainer": get_color_from_hex("#F2E3A3"),  
    "onPrimaryContainer": get_color_from_hex("#3A2F00"),

    # Supporting accent (wood / hive tone) 
    "secondary": get_color_from_hex("#7A5A2B"),
    "onSecondary": get_color_from_hex("#FFFFFF"),

    "secondaryContainer": get_color_from_hex("#E6D5B5"),
    "onSecondaryContainer": get_color_from_hex("#2A1E0C"),

    # Natural accent (plant / pollen hint) 
    "tertiary": get_color_from_hex("#556B2F"),
    "onTertiary": get_color_from_hex("#FFFFFF"),

    "tertiaryContainer": get_color_from_hex("#D5E2B3"),
    "onTertiaryContainer": get_color_from_hex("#1F2A0B"),

    # Background surfaces 
    "background": get_color_from_hex("#FAF7F0"),
    "onBackground": get_color_from_hex("#1C1B1F"),

    "surface": get_color_from_hex("#FAF7F0"),
    "onSurface": get_color_from_hex("#1C1B1F"),

    "surfaceVariant": get_color_from_hex("#E7E1D6"),
    "onSurfaceVariant": get_color_from_hex("#49454F"),

    # Utility 
    "outline": get_color_from_hex("#8F8A82"),

    "error": get_color_from_hex("#B3261E"),
    "onError": get_color_from_hex("#FFFFFF"),
    "errorContainer": get_color_from_hex("#F9DEDC"),
    "onErrorContainer": get_color_from_hex("#410E0B"),
}
