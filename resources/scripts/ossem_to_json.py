from ossem_parsing import load_ossem_cdm, load_ossem_dm, load_ossem_dd
import subprocess
import json
import os
import argparse
import pathlib


def save_json(file_path, ossem_definition):
    with open(file_path, 'w') as dump_file:
        dump_file.write(json.dumps(ossem_definition, default=str, indent=4))


def grouped(iterable, n):
    # https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return zip(*[iter(iterable)]*n)


def dump_to_md(ossem_definition, hugo_path):
    full_path = os.path.join("pages", "src", "content", "docs", hugo_path)

    for (name, definition) in ossem_definition.items():
        filename = name.replace(" ", "_").replace("OSSEM-DD", "") + ".md"
        file_path = os.path.join(full_path, filename)
        pathlib.Path(os.path.dirname(file_path)).mkdir(
            parents=True, exist_ok=True)

        with open(os.path.join(full_path, filename), mode='w') as hugo_file:
            print(f"---\ntitle: {os.path.basename(name)}\n---", file=hugo_file)
            for (title, content) in definition.items():
                print(f"# {title}", file=hugo_file)
                if isinstance(content, str):
                    print(content, file=hugo_file)
                elif isinstance(content, list) and len(content) > 0:
                    if isinstance(content[0], dict):
                        keys = content[0].keys()
                        print("|" + "|".join(keys) + "|", file=hugo_file)
                        print("|" + " :---|" * len(keys), file=hugo_file)
                        for item in content:
                            print("|" + "|".join([str(v) for v in item.values()]) +
                                  "|", file=hugo_file)
                    else:
                        for item in content:
                            print(f"- {item}", file=hugo_file)


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

    load_ossem = {
        'OSSEM-CDM': (load_ossem_cdm, os.path.join('ossem-cdm', 'entities')),
        'OSSEM-DM': (load_ossem_dm, os.path.join('ossem-dm', 'relationships')),
        'OSSEM-DD': (load_ossem_dd, os.path.join('ossem-dd', 'dictionaries'))
    }

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
        (parsing_ossem, hugo_path) = load_ossem[module_name]

        if not os.path.isfile(file_path):
            ossem_definition = parsing_ossem(from_cache=False)
            save_json(file_path, ossem_definition)

            version_file_path = os.path.join(path, f"{module_name}.version")
            print(version, file=open(version_file_path, mode='w'), end='')


if __name__ == "__main__":
    print("[+] Start OSSEM build to JSON")
    main()

    ossem_definition = load_ossem_cdm(
        ossem_name="OSSEM-CDMv0.0.2", from_cache=True)
    dump_to_md(ossem_definition, os.path.join('ossem-cdm', 'entities'))

    ossem_definition = load_ossem_dm(
        ossem_name="OSSEM-DMv0.0.1", from_cache=True)
    dump_to_md(ossem_definition, os.path.join('ossem-dm', 'relationships'))

    # ossem_definition = load_ossem_dd(
    #     ossem_name="OSSEM-DDv0.0.1", from_cache=True)
    # dump_to_md(ossem_definition, os.path.join('ossem-dd', 'dictionaries'))
