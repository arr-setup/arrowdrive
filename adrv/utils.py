class Size:
    def __init__(self, value: int | float):
        self.raw = value
        
    def literal(self):
        sz_unit = 0
        while self.raw >= 1000 ** (sz_unit + 1):
            sz_unit += 1

        return f"{round(self.raw / (1000 ** sz_unit))}{'T' if sz_unit == 4 else 'G' if sz_unit == 3 else 'M' if sz_unit == 2 else 'k' if sz_unit == 1 else ''}B"

units = 1000 ** 0
kilo = 1000 ** 1
mega = 1000 ** 2
giga = 1000 ** 3
tera = 1000 ** 4

def convert(val: float, _from: str, _to: str) -> float:
    _from = _from.upper()
    _to = _to.upper()

    if _from not in ["B", "KB", "MB", "GB", "TB"] or _to not in ["B", "KB", "MB", "GB", "TB"]:
        raise ValueError("Units must be B, kB, MB, GB or TB")
        
    _from = units if _from == "B" else kilo if _from == "KB" else mega if _from == "MB" else giga if _from == "GB" else tera
    _to = units if _to == "B" else kilo if _to == "KB" else mega if _to == "MB" else giga if _to == "GB" else tera

    _diff = _from / _to
    return val * _diff