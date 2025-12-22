import os
import time
import logging
from osgeo import gdal

logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s', level=logging.INFO)

def main():
    start = time.time()
    logging.info("Starting resampling...")

    input_path='/data/input/input.tif'
    output_path='/data/output/resampled.tif'

    try:
        gdal.Warp(output_path, input_path, xRes=100, yRes=100, resampleAlg='near')
        logging.info("Kész")
    except Exception as e:
        logging.error(f"Hiba: {e}")

    end = time.time()
    elapsed = end - start
    logging.info(f'Resampling finished in {elapsed:.2f} seconds')

if __name__ == "__main__":
    main()