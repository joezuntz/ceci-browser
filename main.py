import micropip
global img_str
img_str = ""

imports = [
    "numpy",
    "scipy",
    "networkx",
    # "setuptools-scm",
    # need a pure-python version
    "http://127.0.0.1:8000/PyYAML-5.3.1-cp37-cp37m-macosx_10_13_x86_64.whl",
    # modified to remove som dependencies:
    "http://127.0.0.1:8000/ceci-1.0.5-py3-none-any.whl",
    "http://127.0.0.1:8000/txpipe-0.3-py3-none-any.whl"
]

def draw_pipeline(config):
    import networkx as nx
    import ceci
    import io
    import base64
    import matplotlib
    matplotlib.use('agg')
    import matplotlib.pyplot as plt
    graph = nx.Graph()
    stages = [ceci.PipelineStage.get_stage(stage['name']) for stage in config['stages']]

    # Nodes we have already added
    seen = set()

    # Add overall pipeline inputs
    inputs = config['inputs']
    for inp in inputs.keys():
        graph.add_node(inp)
        seen.add(inp)

    for stage in stages:
        # add the stage itself
        graph.add_node(stage.name)
        # connect that stage to its inputs
        for inp, _ in stage.inputs:
            if inp not in seen:
                graph.add_node(inp)
                seen.add(inp)
            graph.add_edge(inp, stage.name)
        # and to its outputs
        for out, _ in stage.outputs:
            if out not in seen:
                graph.add_node(out)
                seen.add(out)
            graph.add_edge(stage.name, out)

    # finally, output the stage to file
    fig = plt.figure()
    nx.draw(graph)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    print("Image draw_pipeline")
    return base64.b64encode(buf.read()).decode('UTF-8')
          # document.getElementById("pyplotfigure").src=pyodide.globals.img_str

def download_file(url, path):
    import pyodide
    print(f"Downloading {url}")
    sio = pyodide.open_url("http://127.0.0.1:8000/laptop_pipeline.yml")
    sio.seek(0)
    open(path, 'w').write(sio.read())


def main(*args):
    import ceci
    from js import document
    import txpipe
    import os
    import yaml
    print("imports complete")

    pipeline_file = "laptop_pipeline.yml"
    # Download the yaml files
    download_file("http://127.0.0.1:8000/laptop_pipeline.yml", pipeline_file)
    download_file("http://127.0.0.1:8000/laptop_config.yml", "laptop_config.yml")


    # read the yaml files into a ceci pipeline
    config = yaml.safe_load(open(pipeline_file))

    # Make a pipeline image
    img_data = draw_pipeline(config)

    set_image("pyplotfigure", img_data)

def set_image(div_id, img_data):
    from js import document
    global img_str
    img_str = 'data:image/png;base64,' + img_data
    div = document.getElementById(div_id)
    div.src = img_str


def entry_point():
    return micropip.install(imports).then(main)

entry_point()