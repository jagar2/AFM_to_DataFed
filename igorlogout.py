from datafed.CommandLib import API
import os

df_api = API()
def delete_datafed_key_files(directory):
    priv_key_file = os.path.join(directory, 'datafed-user-key.priv')
    pub_key_file = os.path.join(directory, 'datafed-user-key.pub')

    if os.path.exists(priv_key_file):
        os.remove(priv_key_file)
        print("Deleted datafed-user-key.priv")

    if os.path.exists(pub_key_file):
        os.remove(pub_key_file)
        print("Deleted datafed-user-key.pub")


if __name__ == "__main__":
    directory_path = r'C:\Users\Asylum User\.datafed'
    delete_datafed_key_files(directory_path)