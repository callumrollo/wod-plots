import xarray as xr
import pandas as pd
import requests
from pathlib import Path
import logging
_log = logging.getLogger(__name__)

base = "https://www.ncei.noaa.gov/data/oceans/ncei/wod"
logfile = 'wod-download.log'


def extract_year(year, save_nc=False):
    """
    Downloads files from the world ocean database for the specified year.
    :param year: Year to download
    :param save_nc: boolean to save the source nc file. Defaults to False
    :return: None
    """
    downloads_dir = Path("downloaded_files")
    if not downloads_dir.exists():
        downloads_dir.mkdir()

    for ds_type in ("osd", "mbt", "xbt", "ctd", "mrb","apb", "gld", "pfl", "drb", "uor"):
        ds_name = f"wod_{ds_type}_{year}"
        fn = downloads_dir / f"{ds_name}.csv"
        if save_nc:
            dfn = downloads_dir / f"{ds_name}.nc"
        else:
            dfn = downloads_dir / "dataset.nc"
        if Path(fn).exists():
            _log.info(f"Already got {ds_name}")
            continue
        url = f"{base}/{year}/{ds_name}.nc"
        response = requests.get(url)
        if response.status_code != 200:
            _log.info(f"No result for {ds_name}")
            continue
        with open(dfn, 'wb') as f:
            f.write(response.content)
        ds = xr.open_dataset(dfn)
        df = pd.DataFrame({"ds_name": ds_name, "lon": ds.lon.values, "lat": ds.lat.values, "time": ds.time.values})
        df.to_csv(fn, index=False)
        _log.info(f"Downloaded {ds_name}")


def main():
    logging.basicConfig(filename=logfile,
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    _log.info("START")
    for year in range(2000, 2024):
        extract_year(year)
    _log.info("COMPLETE")


if __name__ == '__main__':
    main()

