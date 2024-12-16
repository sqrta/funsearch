from funsearch import _extract_function_names, main
from config import Config, ProgramsDatabaseConfig

with open("skeleton.py", "r") as f:
    content = f.read()
    res = _extract_function_names(content)

    databaseConf = ProgramsDatabaseConfig(num_islands=1)
    conf = Config(
        programs_database=databaseConf,
        num_samplers=1,
        num_evaluators=1,
        samples_per_prompt=1,
        iterations=5,
    )
    inputs = [5]
    print(res)
    checkpoint = "bigcode/starcoder"
    cache_dir = "your path to save llm checkpoint"
    main(content, inputs, conf)
