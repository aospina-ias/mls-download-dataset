import os
import configparser
import yaml
import os
import importlib


def generate_runtime_saml(profile="saml", inference_runtime=False, to_yaml=False, workdir=False, path_workdir=None, **kwargs):
    # aws
    config = configparser.RawConfigParser()
    credentials_file = '/.aws/credentials'
    home = os.path.expanduser("~")
    credentials_file = home + credentials_file
    config.read(credentials_file)

    # databricks
    config_dbs = configparser.RawConfigParser()
    databricks_credentials_file = '/.databrickscfg'
    databricks_credentials_file = home + databricks_credentials_file
    config_dbs.read(databricks_credentials_file)


    # Environment Variables
    env_vars = {}
    # Get the credentials from the file
    env_vars["AWS_ACCESS_KEY_ID"] = config.get(profile, 'aws_access_key_id')
    env_vars["AWS_SECRET_ACCESS_KEY"] = config.get(profile, 'aws_secret_access_key')
    if "aws_session_token" in config[profile]:
        env_vars["AWS_SESSION_TOKEN"] = config.get(profile, 'aws_session_token')

    env_vars["DATABRICKS_HOST"] = "https://ias-datascience-dev.cloud.databricks.com"

    try: 
        # wandb
        config_wandb = configparser.RawConfigParser()
        wandb_credentials_file = '/.wandb'
        wandb_credentials_file = home + wandb_credentials_file
        config_wandb.read(wandb_credentials_file)
        try:
            profile_wandb = config_wandb.sections()[0]
        except:
            profile_wandb = "DEFAULT"
        env_vars["WANDB_API_KEY"] = config_wandb.get(profile_wandb, 'api_key')
    except:
        print("No wandb config file")

    try:
        profile_dbs = config_dbs.sections()[0]
    except:
        profile_dbs = "DEFAULT"

    env_vars["DATABRICKS_TOKEN"] = config_dbs.get(profile_dbs, 'token')
    env_vars["USER"] = os.environ.get('LOGNAME') or os.environ.get('USER')

    # Python libraries
    pip = [
        "boto3",
        "s3fs==2024.6.1",
        "fire",
        "wandb",
        "mteb",
        "omegaconf",
        "yt_dlp",
        "pyarrow",
        "fsspec",
        "webdataset",
        "webvtt-py",
        "timeout-decorator",
        "decord",
        "scenedetect[opencv]==0.6",
        "accelerate",
        "bitsandbytes",
        "scipy",
        "portalocker",
        "ffmpeg-python",
        "einops",
        "langdetect",
        "torch==2.0.0",
        "torchdata==0.6.0",
        "torchaudio==2.0.0",
        "transformers==4.30.0",
    ]






    # Python modules
    py_modules = []

    spec = importlib.util.find_spec("video2dataset")
    video2dataset_path = os.path.dirname(spec.origin)
    py_modules.append(video2dataset_path)


    runtime_env = {
        "env_vars": env_vars,
        "py_modules": py_modules,
        "pip": pip,
    }

    if workdir:
        if path_workdir is not None:
            runtime_env["working_dir"]= path_workdir
        else:
            runtime_env["working_dir"]= os.getcwd()

    if to_yaml:
        with open('runtime-env-saml.yaml', 'w') as file:
            yaml.dump(runtime_env, file)

    return runtime_env

