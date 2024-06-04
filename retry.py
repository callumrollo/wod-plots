from pathlib import Path
import datetime
import download_wod


if __name__ == '__main__':
    logf = Path(download_wod.logfile)
    mtime = datetime.datetime.fromtimestamp(logf.lstat().st_mtime)
    time_elapsed = datetime.datetime.now() - mtime
    # customize delay time here
    if time_elapsed > datetime.timedelta(minutes=60):
        download_wod.main()


