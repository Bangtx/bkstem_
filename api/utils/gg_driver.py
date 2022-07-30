from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)


def upload(file_name):
    # for upload_file in upload_file_list:
    gfile = drive.CreateFile({'parents': [{'id': '1ov1ZC3cHOGaS91AOhKNIeTdeIKkRg-C-'}]})
    # Read file and set it as the content of this instance.
    gfile.SetContentFile(file_name)
    gfile.Upload()  # Upload the file
    gfile.InsertPermission({'role': 'reader', 'type': 'anyone'})
    id_file = gfile.__dict__['attr']['metadata']['parents'][0]['id']
    return drive.ListFile(
        {'q': "'{}' in parents and trashed=false".format(id_file)}
    ).GetList()


def get_list(id):
    # 1ov1ZC3cHOGaS91AOhKNIeTdeIKkRg-C-
    return drive.ListFile(
        {'q': "'{}' in parents and trashed=false".format('1ov1ZC3cHOGaS91AOhKNIeTdeIKkRg-C-')}
    ).GetList()

