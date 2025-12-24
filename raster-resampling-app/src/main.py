import os
import time
import logging
from osgeo import gdal
import glob

logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s', level=logging.INFO)

def main():
    start = time.time()

    env_input = os.getenv('INPUT_FILENAME')
    files_to_process = []

    if env_input:
        logging.info(f"Input file: {env_input}")
        env_input_path = os.path.join('/data/input', env_input)
        if os.path.exists(env_input_path):
            files_to_process = [env_input_path]
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
                logging.warning(f"Found {count} files. Batch processing all found files.")
                files_to_process = found_files
            else:
                input_name = os.path.basename(found_files[0])
                logging.info(f"Found input file: {input_name}.")
                files_to_process = [found_files[0]]
        else:
            logging.error("No files found.")
            return
    
    user_defined_res = os.getenv('TARGET_RES')
    default_res = 100.0

    if user_defined_res:
        try:
            val = float(user_defined_res)
            if val > 0:
                default_res = val
            else:
                logging.warning(f"Invalid TARGET_RES: {val} (must be positive). Using default value: {default_res}")
        except ValueError:
            logging.warning(f"Invalid TARGET_RES value: {user_defined_res} (NaN). Using default value: {default_res}")

    user_defined_alg = os.getenv('RESAMPLE_ALG')
    valid_algs = ['near', 'bilinear', 'cubic', 'cubicspline', 'lanczos', 'average', 'rms', 'mode', 'max', 'min', 'med', 'q1', 'q3', 'sum']
    default_alg = 'near'
    if user_defined_alg: 
        if user_defined_alg.lower() in valid_algs:
            default_alg = user_defined_alg.lower()
        else:
            logging.warning(f"Unknown algorithm: {user_defined_alg}. Using default: {default_alg}.\nValid options are: {valid_algs}.")

    logging.info(f'Applied settings: Res={default_res}, Alg={default_alg}')
    logging.info("Starting resampling...")

    success_count = 0
    error_count = 0
    
    for input_path in files_to_process:
        filename = os.path.basename(input_path)
        filename_without_extension = os.path.splitext(filename)[0]
        new_filename = f"{filename_without_extension}_resampled.tif"
        output_path = os.path.join('/data/output', new_filename)
        try:
            gdal.Warp(output_path, input_path, xRes=default_res, yRes=default_res, resampleAlg=default_alg)
            success_count += 1
        except Exception as e:
            logging.error(f"Error: {e}")
            error_count += 1

    end = time.time()
    elapsed = end - start
    logging.info(f'Resampling finished in {elapsed:.2f} seconds. Files resampled: {success_count}. Errors: {error_count}.')

if __name__ == "__main__":
    main()