import beam

# The environment your code will run on
app = beam.App(
    name="fashion-clip-app",
    cpu=8,
    memory="32Gi",
    gpu="T4",
    python_version="python3.8",
    python_packages=[
        "fashion-clip",
        "gdown",
    ],
)

# Deploys function as async webhook
app.Trigger.Webhook(
    inputs={"query": beam.Types.String()},
    handler="run.py:search_image",
    loader="run.py:load_fclip",
)

# File to store image outputs
app.Output.File(path="output.png", name="myimage")

# Persistent volume to store data
app.Mount.PersistentVolume(path="./cache_data", name="cache_data")