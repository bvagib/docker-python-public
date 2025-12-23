import os
import time
import logging
from osgeo import gdal

logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s', level=logging.INFO)

def main():
    start = time.time()
    logging.info("Starting resampling...")

    input_filename = os.getenv('INPUT_FILENAME', 'input.tif')
    output_filename = os.getenv('OUTPUT_FILENAME', 'resampled.tif')
    target_res = float(os.getenv('TARGET_RES', '100'))
    resample_alg = os.getenv('RESAMPLE_ALG', 'near')

    input_path = os.path.join('/data/input', input_filename)
    output_path = os.path.join('/data/output', output_filename)
    logging.info(f'Applied settings: Res={target_res}, Alg={resample_alg}')

    try:
        gdal.Warp(output_path, input_path, xRes=target_res, yRes=target_res, resampleAlg=resample_alg)
    except Exception as e:
        logging.error(f"Error: {e}")

    end = time.time()
    elapsed = end - start
    logging.info(f'Resampling finished in {elapsed:.2f} seconds.')

if __name__ == "__main__":
    main()