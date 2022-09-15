from ossem_parsing import load_ossem_cdm, load_ossem_dm, load_ossem_dd
import subprocess
import json
import os
import argparse


def save_json(file_path, ossem_definition):
    with open(file_path, 'w') as dump_file:
        dump_file.write(json.dumps(ossem_definition, default=str, indent=4))


def grouped(iterable, n):
    # https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return zip(*[iter(iterable)]*n)


def main():
    """
    Parse OSSEM modules and dump them as json versioned
    """

    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-o", "--output", help="Output path",
                        default=os.path.join("pages", "src", "ossem_build"))

    # Read arguments from command line
    args = parser.parse_args()

    ##################
    ### LOAD OSSEM ###
    ##################

    load_ossem = {'OSSEM-CDM': load_ossem_cdm,
                  'OSSEM-DM': load_ossem_dm, 'OSSEM-DD': load_ossem_dd}

    path = args.output

    output = subprocess.check_output(['git', 'submodule', '--quiet', 'foreach',
                                      "echo $name; git tag --list --sort=-v:refname | head -n 1"]).decode('ascii')

    print(f"OUTPUT = {output}")

    result = output.splitlines()

    for module_name, version in grouped(result, 2):

        if not module_name.startswith('OSSEM-'):
            continue

        assert version.startswith('v')

        file_path = os.path.join(path, f"{module_name}{version}.json")
        if not os.path.isfile(file_path):
            ossem_definition = load_ossem[module_name](from_cache=False)
            save_json(file_path, ossem_definition)

            version_file_path = os.path.join(path, f"{module_name}.version")
            print(version, file=open(version_file_path, mode='w'), end='')


if __name__ == "__main__":
    print("[+] Start OSSEM build to JSON")
    main()
