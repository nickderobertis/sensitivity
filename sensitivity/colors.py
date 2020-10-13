
def _get_color_map(reverse_colors: bool = False, color_map: str = 'RdYlGn') -> str:
    if reverse_colors:
        color_map += '_r'
    return color_map
