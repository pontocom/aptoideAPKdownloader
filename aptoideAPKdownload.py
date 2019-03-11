import requests
from tqdm import tqdm
import math
from urllib.parse import urlparse
import os
import argparse

if __name__=="__main__":
    VERSION = '0.1'
    banner = """
             __         _     __      ___    ___   __ __    __                    __               __         
 ___ _ ___  / /_ ___   (_)___/ /___  / _ |  / _ \ / //_/___/ /___  _    __ ___   / /___  ___ _ ___/ /___  ____
/ _ `// _ \/ __// _ \ / // _  // -_)/ __ | / ___// ,<  / _  // _ \| |/|/ // _ \ / // _ \/ _ `// _  // -_)/ __/
\_,_// .__/\__/ \___//_/ \_,_/ \__//_/ |_|/_/   /_/|_| \_,_/ \___/|__,__//_//_//_/ \___/\_,_/ \_,_/ \__//_/   
    /_/                                                                                                           """

    print(str(banner))

    text = "Tool that downloads APKs from the Aptoide app store"
    parser = argparse.ArgumentParser(description = text)
    parser.add_argument('-v','--version', action='version', version='Aptoide APK Downloader ' + VERSION)
    parser.add_argument('-i', '--input', help='Input file that contains the identifiers of the Aptoide apps to search and download (default filename is ./apks.txt).', action='store', dest='file', nargs=1, default='teste123')
    parser.add_argument('-m', '--md5', help='The MD5 id of the app to download!', action='store', dest='md5', nargs=1, default='')
    args = parser.parse_args()

    # aptoide_API_endpoint = "http://ws2.aptoide.com/api/7/app/get/app_id="
    aptoide_API_endpoint = "http://ws2.aptoide.com/api/7/app/get/apk_md5sum="

    print(args)

    if args.md5:
        response = requests.get(aptoide_API_endpoint + args.md5[0])

        jsondata = response.json()

        applicationName = jsondata["nodes"]["meta"]["data"]["name"]
        applicationPackage = jsondata["nodes"]["meta"]["data"]["package"]
        appVersion = jsondata["nodes"]["meta"]["data"]["file"]["vername"]
        appMD5 = jsondata["nodes"]["meta"]["data"]["file"]["md5sum"]
        appPath = jsondata["nodes"]["meta"]["data"]["file"]["path"]

        print("Getting the following APK => " + applicationName)
        print(applicationPackage + " (" + appVersion + ") -> " + appMD5)
        print(appPath)

        # write the file to the filesystem
        a = urlparse(appPath)
        filename = os.path.basename(a.path)

        # Streaming, so we can iterate over the response.
        r = requests.get(appPath, stream=True)

        # Total size in bytes.
        total_size = int(r.headers.get('content-length', 0));
        block_size = 1024
        wrote = 0
        with open(filename, 'wb') as f:
            for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size // block_size), unit='KB',
                             unit_scale=True):
                wrote = wrote + len(data)
                f.write(data)
        if total_size != 0 and wrote != total_size:
            print("ERROR, something went wrong")

    elif args.file:
        filename = format(args.file[0])

        print("Reading APK info from: " + filename)

        with open('apks.txt') as f:
            for line in f:
                id_app = line

                response = requests.get(aptoide_API_endpoint + id_app)

                jsondata = response.json()

                applicationName = jsondata["nodes"]["meta"]["data"]["name"]
                applicationPackage = jsondata["nodes"]["meta"]["data"]["package"]
                appVersion = jsondata["nodes"]["meta"]["data"]["file"]["vername"]
                appMD5 = jsondata["nodes"]["meta"]["data"]["file"]["md5sum"]
                appPath = jsondata["nodes"]["meta"]["data"]["file"]["path"]

                print("Getting the following APK => " + applicationName)
                print(applicationPackage + " (" + appVersion + ") -> " + appMD5)
                print(appPath)

                # write the file to the filesystem
                a = urlparse(appPath)
                filename = os.path.basename(a.path)

                # Streaming, so we can iterate over the response.
                r = requests.get(appPath, stream=True)

                # Total size in bytes.
                total_size = int(r.headers.get('content-length', 0));
                block_size = 1024
                wrote = 0
                with open( filename, 'wb') as f:
                    for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
                        wrote = wrote  + len(data)
                        f.write(data)
                if total_size != 0 and wrote != total_size:
                    print("ERROR, something went wrong")
