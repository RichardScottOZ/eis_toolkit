from numbers import Number
from typing import Optional, Tuple

import numpy as np
import rasterio
from beartype import beartype
from scipy.ndimage import distance_transform_edt

# !! WIP !!


@beartype
def _distance_computation_raster(
    raster: rasterio.io.DatasetReader, threshold: Optional[Number]
) -> Tuple[np.ndarray, dict]:

    raster_array = raster.read()
    out_meta = raster.meta.copy()

    if threshold is not None:
        binary_mask = raster_array >= threshold

    # Step 3: Calculate the Euclidean distance for each cell to the nearest 'true' cell in the binary mask
    out_image = distance_transform_edt(~binary_mask)

    return out_image, out_meta


@beartype
def distance_computation_raster(
    raster: rasterio.io.DatasetReader, threshold: Optional[Number]
) -> Tuple[np.ndarray, dict]:
    """TBD.

    Args:
        raster: The raster to be reprojected.
        threshold: Threshold binary value. Optional.

    Returns:
        The distance computation output raster data.
        The updated metadata.

    Raises:
        NonMatchinCrsException: Raster is already in the target CRS.
    """

    raster_array = raster.read()

    if threshold is None:
        unique_values = np.unique(raster_array)
        if len(unique_values) == 2:
            pass

    out_image, out_meta = _distance_computation_raster(raster, threshold)
    return out_image, out_meta
