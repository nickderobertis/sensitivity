
def _get_color_map(reverse_colors: bool = False) -> str:
    color_map = 'RdYlGn'
    if reverse_colors:
        color_map += '_r'
    return color_map
