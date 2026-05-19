from dataclasses import dataclass
from math import ceil


@dataclass(frozen=True)
class PrintTarget:
    width_cm: float
    height_cm: float
    dpi: int

    @property
    def width_px(self) -> int:
        return ceil((self.width_cm / 2.54) * self.dpi)

    @property
    def height_px(self) -> int:
        return ceil((self.height_cm / 2.54) * self.dpi)


def required_scale(source_width: int, source_height: int, target: PrintTarget) -> int:
    width_scale = target.width_px / source_width
    height_scale = target.height_px / source_height
    scale = max(width_scale, height_scale)

    if scale <= 1:
        return 1
    if scale <= 2:
        return 2
    if scale <= 3:
        return 3
    return 4


def dpi_for_print(source_width: int, source_height: int, width_cm: float, height_cm: float) -> dict[str, int]:
    width_dpi = int(source_width / (width_cm / 2.54))
    height_dpi = int(source_height / (height_cm / 2.54))
    return {
        "width_dpi": width_dpi,
        "height_dpi": height_dpi,
        "effective_dpi": min(width_dpi, height_dpi),
    }

