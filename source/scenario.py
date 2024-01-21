from typing import Any, Dict
from Melodie import Scenario
import numpy as np
import pandas as pd
from source import data_info


class CovidScenario(Scenario):

    def load(self):
        self.transition_probs_df = self.load_dataframe(
            "Parameter_AgeGroup_TransitionProb.xlsx")

        self.id_health_state = self.load_dataframe(
            "ID_HealthState.xlsx"
        )
        self.id_age_group = self.load_dataframe(
            "ID_AgeGroup.xlsx"
        )

    def setup(self):
        self.period_num: int = 0
        self.agent_num: int = 0
        self.initial_infected_percentage: float = 0.0
        self.young_percentage: float = 0.0
        self.infection_prob: float = 0.0
        self.setup_transition_probs()

    def setup_data(self):
        self.generate_agent_dataframe()

    def setup_transition_probs(self):
        df = self.transition_probs_df
        self.transition_probs = {
            0: {
                "s1_s1": df.at[0, "prob_s1_s1"],
                "s1_s2": df.at[0, "prob_s1_s2"],
                "s1_s3": df.at[0, "prob_s1_s3"],
            },
            1: {
                "s1_s1": df.at[1, "prob_s1_s1"],
                "s1_s2": df.at[1, "prob_s1_s2"],
                "s1_s3": df.at[1, "prob_s1_s3"],
            }
        }

    def get_transition_probs(self, id_age_group: int):
        return self.transition_probs[id_age_group]

    @staticmethod
    def init_health_state(scenario: "CovidScenario"):
        state = 0
        if np.random.uniform(0, 1) <= scenario.initial_infected_percentage:
            state = 1
        return state

    @staticmethod
    def init_age_group(scenario: "CovidScenario"):
        age_group = 0
        if np.random.uniform(0, 1) > scenario.young_percentage:
            age_group = 1
        return age_group

    def generate_agent_dataframe(self):
        assert self.manager is not None
        assert self.manager.data_loader is not None

        def generate_row(id: int, scenario: "CovidScenario") -> Dict[str, Any]:
            return {
                "id": id,
                "health_state": self.init_health_state(scenario),
                "age_group": self.init_age_group(scenario),
            }
        data = []
        for agent_id in range(self.agent_num):
            data.append(generate_row(agent_id, self))
        self.agent_params = pd.DataFrame(data)
