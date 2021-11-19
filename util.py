import shutil
import requests
import os
import urllib.request as request
import sqlite3

SPLITTER='/'
RESOURCES_FOLDER = os.getcwd()

def download_file_http(url, file_path, c,ctx):
    if c > 5:
        download_file_http_failsafe(url, file_path,ctx)
    else:
        if ctx:
            with requests.get(url, stream=True,verify=False) as r:
                with open(file_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
        else:
            with requests.get(url, stream=True) as r:
                with open(file_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)


# slower but safer
def download_file_http_failsafe(url, file_path,ctx):
    with requests.Session() as session:
        if ctx: session.verify = False
        get = session.get(url, stream=True)
        if get.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in get.iter_content(chunk_size=1024):
                    f.write(chunk)


def download_file_ftp(url, file_path,ctx):
    with closing(request.urlopen(url,context=ctx)) as r:
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(r, f)


def download_file(url, output_folder='', stdout_file=None, retry_limit=10):
    file_path = output_folder + url.split('/')[-1]
    ctx=None
    try:
        target_file = request.urlopen(url)
    except:
        try:
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            target_file = request.urlopen(url,context=ctx)
        except:
            print('Cannot download target url', url)
            return
    target_size = target_file.info()['Content-Length']
    transfer_encoding = target_file.info()['Transfer-Encoding']
    if target_size: target_size = int(target_size)
    if file_exists(file_path):
        if transfer_encoding == 'chunked':
            return
        elif os.stat(file_path).st_size == target_size:
            print('Not downloading from ' + url + ' since file was already found!', flush=True, file=stdout_file)
            return
        else:
            os.remove(file_path)
    print('Downloading from ' + url + '. The file will be kept in ' + output_folder, flush=True, file=stdout_file)
    c = 0
    while c <= retry_limit:
        if 'ftp' in url:
            try:
                download_file_ftp(url, file_path,ctx)
            except:
                try:
                    download_file_http(url, file_path, c,ctx)
                except: pass
        else:
            try:
                download_file_http(url, file_path, c,ctx)
            except:
                pass
        if transfer_encoding == 'chunked': return
        if file_exists(file_path):
            if os.stat(file_path).st_size == target_size: return
        c += 1
    print('Did not manage to download the following url correctly:\n' + url)
    raise Exception

def uncompress_archive(source_filepath, extract_path=None, block_size=65536, remove_source=False, stdout_file=None):
    file_name = source_filepath.split(SPLITTER)[-1]
    dir_path = SPLITTER.join(source_filepath.split(SPLITTER)[0:-1])
    if not extract_path: extract_path = dir_path
    if '.tar' in file_name:
        unpack_archive(source_file=source_filepath, extract_dir=extract_path, remove_source=remove_source,
                       stdout_file=None)
    # only for files
    elif '.gz' in file_name:
        gunzip(source_filepath=source_filepath, dest_filepath=extract_path, block_size=block_size,
               remove_source=remove_source, stdout_file=stdout_file)
    elif '.zip' in file_name:
        unzip_archive(source_file=source_filepath, extract_dir=extract_path, remove_source=remove_source,
                      stdout_file=None)
    else:
        print('Incorrect format! ', source_filepath, flush=True, file=stdout_file)


# this unzips to the same directory!
def gunzip(source_filepath, dest_filepath=None, block_size=65536, remove_source=False, stdout_file=None):
    if not dest_filepath:
        dest_filepath = source_filepath.strip('.gz')
    if os.path.isdir(dest_filepath):
        file_name = source_filepath.split(SPLITTER)[-1].replace('.gz', '')
        dest_filepath = add_slash(dest_filepath) + file_name
    print('Gunzipping ', source_filepath, 'to', dest_filepath, flush=True, file=stdout_file)
    with gzip_open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        while True:
            block = s_file.read(block_size)
            if not block:
                break
            else:
                d_file.write(block)
        d_file.write(block)
    if remove_source: os.remove(source_filepath)


def unpack_archive(source_file, extract_dir, remove_source=False, stdout_file=None):
    print('Unpacking', source_file, 'to', extract_dir, flush=True, file=stdout_file)
    shutil.unpack_archive(source_file, extract_dir=extract_dir)
    if remove_source: os.remove(source_file)


def unzip_archive(source_file, extract_dir, remove_source=False, stdout_file=None):
    print('Unzipping', source_file, 'to', extract_dir, flush=True, file=stdout_file)
    with ZipFile(source_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    if remove_source: os.remove(source_file)

def file_exists(target_file, force_download=False):
    if not target_file: return False
    if os.path.exists(target_file) and not force_download:
        return True
    return False

print(RESOURCES_FOLDER)