import os
import toml
import subprocess
import hashlib
import sys
import time

# TODO: Run rsync across entire directory for less moving parts
# TODO: Multithreading
# TODO: Convert to Go

def run_command(cmd):
    try:
        subprocess.run(cmd)
    except:
        print("unable to run command:"  + ''.join(cmd))

def run_rsync(file_name):
    run_command(["rsync", "-vr", "--rsh=ssh", file_name, str(configs["remote_server"]) + ":" + str(configs["remote_files"])])

def delete(file_name):
    run_command(["rm", "-rv", file_name])

def get_file_list(local_files):
    files_to_ingest = []
    for root, dirs, files in os.walk(local_files):
        for name in files:
            files_to_ingest.append(os.path.join(root,name))
    return files_to_ingest

def get_transfer_file_list(local_files):
    files_to_ingest = []
    for files in os.listdir(local_files):
        files_to_ingest.append(os.path.join(configs["local_files"],files))
    return files_to_ingest

def sha256_load_local(file_name, local_sha_map):
    sha256 = hashlib.sha256()
    with open(file_name, "rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256.update(byte_block)
    local_sha_map[sha256.hexdigest()] = file_name
    return local_sha_map

def sha256_load_remote():
    remote_sha_map = {}
    keypair = subprocess.check_output(["ssh", configs["remote_server"], 'find', configs["remote_files"], '-type f -exec sha256sum {} \;']).split()

    timing = 0
    for index in range(len(keypair)//2):
        remote_sha_map[str(keypair[timing])[2:-1]] = str(keypair[timing+1])[2:-1]
        timing += 2

    return remote_sha_map

def sha256_check(local_checksum_map, remote_checksum_map):
    bad_list = []
    for key in local_checksum_map:
        if key not in remote_checksum_map:
            print("Bad file: " + local_checksum_map[key])
            bad_list.append(local_checksum_map[key])
        else:
            print(local_checksum_map[key] + " passed sha256 check!")
    return bad_list

def get_args():
    try:
        return sys.argv[1]
    except:
        print("invalid sys.argv[1], running default: /root/config.toml")
        return "/root/config.toml"

if __name__ == '__main__':
    try:
        configs = toml.loads(open(get_args(),"r").read())
    except:
        print("error while reading toml")

    while(True):
        for file in get_transfer_file_list(configs["local_files"]):
            run_rsync(file)

        local_sha_map = {}

        for file in get_file_list(configs["local_files"]):
            local_sha_map = sha256_load_local(file,local_sha_map)

        remote_sha_map = sha256_load_remote()

        bad_list = sha256_check(local_sha_map, remote_sha_map)
        while(len(bad_list) != 0):
            for file in bad_list:
                run_rsync(file)
            remote_sha_map = sha256_load_remote()
            bad_list = (sha256_check(local_sha_map, remote_sha_map))
            
        for file in get_transfer_file_list(configs["local_files"]):
            delete(file)

        time.sleep(600)