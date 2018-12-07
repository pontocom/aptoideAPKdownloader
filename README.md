# aptoideAPKdownloader

Tool that can be used to download APKs from the [Aptoide](www.aptoide.com) app store. The tool downloads a list of APKs from the store that are recorded on a file.

On the Aptoide store select the application id (**app_id**) of the APK that you wish to download, that can be found on the "**Download**" button link:
```
https://en.aptoide.com/thank-you?app_id=41563327&store_name=sommydany
```

You can build an file with a list of app_ids to be downloaded in order for our tool to use!

## Tool usage

In order to use the tool the following command and options can be used:

```
python3 aptoideAPKdownloader.py [-h, --help] [-v, --version] [-i, --input] FILE 
```

**-h, --help**: Displays the usage of the tool (**optional**).
**-v, --version**: Displays the version of the tool (**optional**).
**-i, --input**: This parameter is mandatory and is used to pass the file that contains the list of application ids that will be downloaded by the tool (mandatory). The file will have an app_id per line.

**Example**:

```
python3 aptoideAPKdownloader.py -i apks.txt
```
This will download all the APKs, corresponding to the app ids contained in the apks.txt file.
