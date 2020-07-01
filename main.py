import micropip

# globals
nodes = []
edges = []


def build_graph(config):
    import ceci
    import txpipe
    stages = [ceci.PipelineStage.get_stage(stage['name']) for stage in config['stages']]

    edges = []
    nodes = []

    # Nodes we have already added
    seen = set()

    # Add overall pipeline inputs
    inputs = config['inputs']
    for inp in inputs.keys():
        if inp not in seen:
            nodes.append([inp, 'gold'])
            seen.add(inp)

    for stage in stages:
        # add the stage itself
        nodes.append([stage.name, 'orangered'])
        # connect that stage to its inputs
        for inp, _ in stage.inputs:
            if inp not in seen:
                nodes.append([inp, 'skyblue'])
                seen.add(inp)
            edges.append([inp, stage.name])
        # and to its outputs
        for out, _ in stage.outputs:
            if out not in seen:
                nodes.append([out, 'skyblue'])
                seen.add(out)
            edges.append([stage.name, out])
    return nodes, edges


def download_file(url, path):
    import pyodide
    print(f"Downloading {url}")
    sio = pyodide.open_url(url)
    sio.seek(0)
    open(path, 'w').write(sio.read())


def main(*args):
    import ceci
    import txpipe
    import yaml
    from js import document
    import os
    print("imports complete")

    pipeline_file = "laptop_pipeline.yml"
    # Download the yaml files
    download_file("/laptop_pipeline.yml", pipeline_file)

    # read the yaml files into a ceci pipeline
    config = yaml.safe_load(open(pipeline_file))

    # Make a pipeline image
    global nodes
    global edges
    nodes, edges = build_graph(config)



def entry_point(base_url):
    imports = [
        "numpy",
        "scipy",
        # "networkx",
        "setuptools-scm",
        # need a pure-python version
        base_url + "/PyYAML-5.3.1-cp37-cp37m-macosx_10_13_x86_64.whl",
        # modified to remove some dependencies:
        base_url + "/ceci-1.0.5-py3-none-any.whl",
        base_url + "/txpipe-0.3-py3-none-any.whl",
    ]
    return micropip.install(imports).then(main)

