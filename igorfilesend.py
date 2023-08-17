import argparse
from datafed.CommandLib import API
from util import *
import os
import glob
import getpass

# Initialize the API object
df_api = API()
# def delete_datafed_key_files(directory):
#     priv_key_file = os.path.join(directory, 'datafed-user-key.priv')
#     pub_key_file = os.path.join(directory, 'datafed-user-key.pub')

#     if os.path.exists(priv_key_file):
#         os.remove(priv_key_file)
#         print("Deleted datafed-user-key.priv")

#     if os.path.exists(pub_key_file):
#         os.remove(pub_key_file)
#         print("Deleted datafed-user-key.pub")

# directory_path = r'C:\Users\Asylum User\.datafed'

def DataFed_Log_In():

    # if df_api.getAuthUser() is not None:
    #     delete_datafed_key_files(directory_path)
    # else:

    uid = input("User ID: ")
    password = getpass.getpass(prompt="Password: ")

    try:
        # Attempt to log in using provided credentials
        df_api.loginByPassword(uid, password)
        success = f"Successfully logged in to Data as {df_api.getAuthUser()}"
        if df_api.getAuthUser() is not None:
            df_api.setupCredentials()
    except:
        success = "Could not log into DataFed. Check your internet connection, username, and password"

    return success

def _send_ibw_to_datafed(file_name, collection_id):

    json_output = get_metadata(file_name)

    print(file_name)
    print(collection_id)

    # This removes flattening information and fixes inf values in metadata
    try:
        del json_output['Flatten Offsets 0']
    except:
        pass

    try:
        del json_output['Flatten Slopes 0']
    except:
        pass

    try:
        del json_output['Flatten Slopes 4']
    except:
        pass

    try:
        del json_output['Flatten Offsets 4']
    except:
        pass

    try:
        del json_output['Flatten Offsets 1']
    except:
        pass

    try:
        del json_output['Flatten Slopes 1']
    except:
        pass

    for i, (key, value) in enumerate(json_output.items()):
        if value == np.NINF:
            json_output[key] = '-Inf'

    for i, (key, value) in enumerate(json_output.items()):
        if value == np.Inf:
            json_output[key] = 'Inf'

    try:
        # creates a new data record
        dc_resp = df_api.dataCreate(file_name, # file name
                                metadata=json.dumps(json_output), # metadata
                                parent_id=collection_id, # parent collection
                            )
    except Exception as e:
        print('There was an error creating the DataRecord', e)

    try:
        # extracts the record ID
        rec_id = dc_resp[0].data[0].id
    except ValueError:
        print('Could not find record ID')

    try:
        # sends the put command
        put_resp = df_api.dataPut(rec_id,
                                    file_name,
                                    wait = True)
    except Exception:
        print('Could not intiate globus transfer')


if __name__ == "__main__":

    # parser = argparse.ArgumentParser()
    # parser.add_argument("square", help="display a square of a given number",
    #                     type=int)
    # args = parser.parse_args()
    # print(args.square**2)

    parser = argparse.ArgumentParser(description="Send IBW data to DataFed")

    parser.add_argument("file_name", help="Path to the IBW file")
    parser.add_argument("collection_id", help="ID of the parent collection")

    args = parser.parse_args()

    login_result = DataFed_Log_In()
    print(login_result)

    _send_ibw_to_datafed(file_name=args.file_name, collection_id=args.collection_id)