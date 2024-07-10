import os
import ray
from video2dataset import video2dataset
# Import placement group APIs.
from ray.util.placement_group import placement_group
from ray.util.scheduling_strategies import PlacementGroupSchedulingStrategy


ray.init()
ctx = ray.data.DataContext.get_current()
ctx.execution_options.resource_limits.cpu = 32


@ray.remote
def launch_job(
    url_list = "s3://mls.us-east-1.mum-data/open_source_data/panda70m_training_10m.csv",
    output_folder = "s3://mls.us-east-1.mum-data/open_source_data/panda10",
    output_format: str = "files",
    input_format: str = "csv",
    encode_formats = {"video": "best", "audio": "m4a"},
    stage: str = "download",
    url_col="url" ,
    caption_col="caption" ,
    clip_col="timestamp" ,
    save_additional_columns=["matching_score"] ,
    incremental_mode: str = "overwrite",
    max_shard_retry: int = 3,
    tmp_dir: str = "/tmp/download",
    config="src/video2dataset/video2dataset/configs/panda70m.yaml" ,
    **kwargs
):
    current_directory = os.getcwd()
    print(current_directory)
    video2dataset(
        url_list= url_list,
        output_folder= output_folder,
        output_format= output_format,
        input_format= input_format,
        encode_formats= encode_formats,
        stage= stage,
        url_col= url_col,
        caption_col= caption_col,
        clip_col= clip_col,
        save_additional_columns= save_additional_columns,
        incremental_mode= incremental_mode,
        max_shard_retry= max_shard_retry,
        tmp_dir= tmp_dir,
        config= config,
        )



if __name__ == '__main__':
    pg = placement_group([{"CPU": 32, "GPU": 0}], strategy="STRICT_PACK")
    ray.get(
        launch_job.options(
            scheduling_strategy=PlacementGroupSchedulingStrategy(
                placement_group=pg
            )
        ).remote()
    )