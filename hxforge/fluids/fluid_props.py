from abc import ABC, abstractmethod
from numpy import ndarray
from pathlib import Path
import pandas as pd


class FluidProps(ABC):
    def __init__(self, fluid_name: str):
        self.fluid_name = fluid_name
        self._h: float  # stored enthalpy
        self._props: ndarray | None = None

    # ── public enthalpy attribute ────────────────────
    @property
    def h(self) -> float:
        return self._h

    @h.setter
    def h(self, value: float):
        self._h = value
        self._props = self._calc_props(value)

    # ── read‑only properties vector ──────────────────
    @property
    def props(self) -> ndarray:
        if self._props is None:
            raise AttributeError("Set .h first (e.g. obj.h = 150e3)")
        return self._props

    # ── subclass must supply the actual physics/math ─
    @abstractmethod
    def _calc_props(self, enthalpy: float) -> ndarray:
        pass


class FluidPropsFromFile(FluidProps):
    def __init__(self, fluid_name: str):
        super().__init__(fluid_name)
        self._load_properties_from_file()

    def _load_properties_from_file(self) -> None:
        cwd: Path = Path.cwd()
        file_path = cwd / f"{self.fluid_name}.txt"
        if not file_path.exists():
            raise FileNotFoundError(f"Fluid properties file not found: {file_path}")
        else:
            self.props_df = pd.read_csv(file_path, sep="\t", index_col="enthalpy")
            self.props_df.index = self.props_df.index.astype(float)
            self.props_df.sort_index(inplace=True)

    def _interpolate_row(xq, xcol="enthalpy"):
        # make sure the key column is the (sorted) index
        dfi = self.props_df.set_index(xcol)

        # add the query point to the index, interpolate, pluck the new row
        out = (
            dfi.reindex(dfi.index.union([xq]))  # step ①
            .interpolate(method="index")  # step ②  (linear w.r.t. index)
            .loc[xq]  # step ③
        )
        return out


class FluidPropsAsArraysFromCoolprop(FluidProps):
    """Fluid properties implementation using CoolProp with arrays."""

    def get_props(self, enthalpy: float, pressure: float | None = None) -> ndarray:
        """Get fluid properties as arrays using CoolProp.

        Args:
            enthalpy (float): Specific enthalpy of the fluid.
            pressure (float|None, optional): Pressure of the fluid. Defaults to None.

        Returns:
            ndarray: Array of fluid properties.
        """
        # Implementation using CoolProp would go here
        pass
