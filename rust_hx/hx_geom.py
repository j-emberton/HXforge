from dataclasses import dataclass


@dataclass
class tube_geometry:
    length: float = 1
    tube_od: float = 0.01
    tube_id: float = 0.009
