import os
import time
import logging
from osgeo import gdal
import glob

logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s', level=logging.INFO)

def main():
    start = time.time()

    env_input = os.getenv('INPUT_FILENAME')

    if env_input:
        logging.info(f"Input file: {env_input}")
        env_input_path = os.path.join('/data/input', env_input)
        if os.path.exists(env_input_path):
            input_path = env_input_path
        else:
            logging.error(f'No file named "{env_input}" found.')
            return
    else:       
        found_files = glob.glob('/data/input/*.tif')
        if found_files: 
            count = len(found_files)
            input_path = found_files[0]
            input_name = os.path.basename(input_path)
            if count > 1:
                logging.warning(f"Found {count} files. Processing the first one: {input_name}.")
            else:
                logging.info(f"Found input file: {input_name}.")
        else:
            logging.error("No files found.")
            return

    filename = os.path.basename(input_path)
    filename_without_extension = os.path.splitext(filename)[0]
    new_filename = f"{filename_without_extension}_resampled.tif"
    output_path = os.path.join('/data/output', new_filename)

    target_res = float(os.getenv('TARGET_RES', '100'))
    resample_alg = os.getenv('RESAMPLE_ALG', 'near')

    logging.info(f'Applied settings: Res={target_res}, Alg={resample_alg}')
    logging.info("Starting resampling...")

    try:
        gdal.Warp(output_path, input_path, xRes=target_res, yRes=target_res, resampleAlg=resample_alg)
    except Exception as e:
        logging.error(f"Error: {e}")

    end = time.time()
    elapsed = end - start
    logging.info(f'Resampling finished in {elapsed:.2f} seconds.')

if __name__ == "__main__":
    main()