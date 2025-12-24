# Containerized Raster Resampler
A Python-based app that can be used to resample raster (`.tif`) files using GDAL. It is containerized with Docker.
## Features
- Resample single file: option given to process a specific file by name.
- Resample multiple files at once: automatically detects and processes all `.tif` files when no input file is specified.
- Dynamic output naming: automatically generates output filenames (e.g., `inputfile_resampled.tif`).

## Dependencies
- Docker and Docker Compose installed.
## Get started
1. Place your `.tif` files into the `raster-resampling-app/input` folder.
2. Open a terminal.
3. Run the app:
    ```bash
    docker compose up --build raster-resampling-app
    ```
4. Results are in `raster-resampling-app/output`.
## Configuration
You can configure the app by editing the `environment` section in the `compose.yml` file.
| Variable | Default | Description |
| :--- | :--- | :--- |
| `INPUT_FILENAME` | *(Empty)* | Empty: Batch process all files.<br>Filename: Process only this specific file (e.g., `input.tif`). |
| `TARGET_RES` | `100` | The target resolution (pixel size) in map units. Must be a positive number. |
| `RESAMPLE_ALG` | `near` | Resampling algorithm.<br>Valid options: `near`, `bilinear`, `cubic`, `cubicspline`, `lanczos`, `average`, `rms`, `mode`, `max`, `min`, `med`, `q1`, `q3`, `sum` |
## Credits
Technologies used in this app:
- GDAL (Geospatial Data Abstraction Library, `gdal.org`)
- Docker (`docker.com`)
- Python (`python.org`)