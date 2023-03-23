from experience_recorder.recorder import Recorder

def test_along():
    import yaml

    from experience_recorder.configuration import Configuration
    from experience_recorder.recorder import Recorder
    import os

    if __name__ == "__main__":
        with open("conf/global.yaml", 'r', encoding='utf-8') as global_configuration:
            global_configuration = yaml.safe_load(global_configuration)
            task_configuration = Configuration(global_configuration)
            task_configuration.save_configuration()
            recorder = Recorder(global_configuration, task_configuration.conf)



