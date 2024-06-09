import os, shutil


def copy_contents(from_directory, to_directory):
    print(f"Copying files...\nfrom --> {from_directory}\ninto --> {to_directory}")
    if os.path.exists(from_directory):
        if not os.path.exists(to_directory):
            print(f"Directory does not exist, creating directory...")
            try:
                os.mkdir(to_directory)
            except:
                raise Exception(f"Error: failed to create directory {to_directory}")
            else:
                print(f"Success: created directory {to_directory}")
        else:
            print(f"Directory already exists: deleting directory {to_directory}")
            try:
                shutil.rmtree(to_directory)
                os.mkdir(to_directory)
            except:
                raise Exception(f"Error: failed to delete and re-create directory {to_directory}")
            else:
                print(f"Success: deleted and re-created directory {to_directory}")
        for item in os.listdir(from_directory):
            from_item_path = os.path.join(from_directory, item)
            to_item_path = os.path.join(to_directory, item)
            if os.path.isfile(from_item_path):
                print(f"Copying file........\n{from_item_path}\n{to_item_path}")
                try:
                    shutil.copy(from_item_path, to_item_path)
                except:
                    raise Exception(f"Error: failed to copy file...\n{from_item_path}\n-->{to_item_path}")
                else:
                    print(f"Success: copied file")
            if os.path.isdir(from_item_path):
                print(f"Copying directory...\n{from_item_path}\n{to_item_path}")
                try:
                    os.mkdir(to_item_path)
                except:
                    raise Exception(f"Error: failed to copy directory {from_item_path} --> {to_item_path}")
                else:
                    print(f"Success: copied directory")
                copy_contents(from_item_path, to_item_path)
    else:
        raise Exception(f"Error: {from_directory} does not exist")
