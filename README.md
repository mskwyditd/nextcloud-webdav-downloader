# nextcloud-webdav-downloader

A simple python tool, which lists Nextcloud root folder resources and allows downloading a chosen file or folder through WebDAV.

## Install dependencies

    pip install -r requirements.txt

## Download file or folder

    python3 nc_downloader.py [-l, --login login] [-p, --password password] [-d, --dst-path /destnation/path] [-s, --src-path file/folder to download]

Default destination path (download path) is folder from which the code is executed.

### Example execution

    $ python .\nc_downloader.py -l *username*
    Password: *password*
    user.name/
    Documents/
    ...
    *items listed from root folder*
    ...
    Templates/
    What should be downloaded? (/ or name of folder/file): *file or folder name*
    65.5kB [00:17, 3.75kB/s]
