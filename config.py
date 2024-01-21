import os

from Melodie import Config, MysqlDBConfig

config = Config(
    project_name="CovidContagion",
    project_root=os.path.dirname(__file__),
    input_folder="data/input",
    output_folder="data/output",
    data_output_type="csv"
    # database_config=MysqlDBConfig("covid_contagion", "localhost", "root", "123456")
)
