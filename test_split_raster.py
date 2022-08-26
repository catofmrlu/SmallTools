from osgeo import ogr, gdal
import numpy as np


def split_raster(sourcetif, x_count, y_count):
    # sourcetif:源影像数据
    # x_count：横向切割数量
    # y_count：纵向切割数量

    ds = gdal.Open(sourcetif, 0)
    proj = ds.GetProjection()
    gtf = ds.GetGeoTransform()
    band = ds.GetRasterBand(1)
    # array_list = band.ReadAsArray()
    chunk_px_count_x = int(ds.RasterXSize / x_count)
    chunk_px_count_y = int(ds.RasterYSize / y_count)

    x_max = y_min = None
    x_min = gtf[0]

    for x in range(x_count):

        if x == x_count - 1:
            x_max = gtf[0] + ds.RasterXSize * gtf[1]
        else:
            x_max = x_min + chunk_px_count_x * gtf[1]
        y_max = gtf[3]
        for y in range(y_count):

            if y == y_count - 1:
                y_min = gtf[3] + ds.RasterXSize * gtf[5]
            else:
                y_min = y_max + chunk_px_count_y * gtf[5]

            gdal.Warp(f"D:/{x}-{y}.tif", ds, outputBounds=[x_min, y_min, x_max, y_max], dstNodata=-9999)
            y_max = y_min
        x_min = x_max


if __name__ == '__main__':
    sourceds = r"D:\LS8_C_20170912_025912_000000_123046_GEOTIFF_SNC_L4\LC81230462017255SNC00_B1.tif"
    split_raster(sourceds, 4, 4)
