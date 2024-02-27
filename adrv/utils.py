class Size:
    def __init__(self, value: int | float):
        self.raw = value
        
    def literal(self):
        sz_unit = 0
        while self.raw >= 1000 ** (sz_unit + 1):
            sz_unit += 1

        return f"{round(self.raw / (1000 ** sz_unit))}{'T' if sz_unit == 4 else 'G' if sz_unit == 3 else 'M' if sz_unit == 2 else 'k' if sz_unit == 1 else ''}B"
    
class Converter:
    def __init__(self) -> None:
        self.bytes = 1000 ** 0
        self.kilo = 1000 ** 1
        self.mega = 1000 ** 2
        self.giga = 1000 ** 3
        self.tera = 1000 ** 4

    def convert(self, val: float, _from: str, _to: str) -> float:
        _from = _from.upper()
        _to = _to.upper()

        if _from not in ["B", "KB", "MB", "GB", "TB"] or _to not in ["B", "KB", "MB", "GB", "TB"]:
            raise ValueError("Units must be B, kB, MB, GB or TB")
        
        _from = self.bytes if _from == "B" else self.kilo if _from == "KB" else self.mega if _from == "MB" else self.giga if _from == "GB" else self.tera
        _to = self.bytes if _to == "B" else self.kilo if _to == "KB" else self.mega if _to == "MB" else self.giga if _to == "GB" else self.tera

        _diff = _from / _to
        return val * _diff