import os
import shutil
import sys

if __name__ == '__main__':
    dir_to_migrate = sys.argv[1]

    response_files = []
    for root, dirs, files in os.walk(dir_to_migrate):
        response_files += [os.path.join(root, f) for f in files if f.endswith('.json')]
    
    for response_file in response_files:
        filename = os.path.basename(response_file)
        method, endpoint = filename.split('_')
        new_endpoint_dir = os.path.join(os.path.dirname(response_file), os.path.splitext(endpoint)[0])

        if not os.path.exists(new_endpoint_dir):
            os.mkdir(new_endpoint_dir)
        
        shutil.copyfile(response_file, os.path.join(new_endpoint_dir, method + ".json"))
        os.remove(response_file)
