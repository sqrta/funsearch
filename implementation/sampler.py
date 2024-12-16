# Copyright 2023 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Class for sampling new programs."""
from collections.abc import Collection, Sequence

import numpy as np

import evaluator
import programs_database


class LLM:
    """Language model that predicts continuation of provided source code."""

    def __init__(self, samples_per_prompt: int) -> None:
        self._samples_per_prompt = samples_per_prompt

    def _draw_sample(self, prompt: str) -> str:
        """Returns a predicted continuation of `prompt`."""
        # Make sure your LLM only produce a pure python function without discription at the start.

        raise NotImplementedError("Must provide a language model.")

    def draw_samples(self, prompt: str) -> Collection[str]:
        """Returns multiple predicted continuations of `prompt`."""
        return [self._draw_sample(prompt) for _ in range(self._samples_per_prompt)]


class Sampler:
    """Node that samples program continuations and sends them for analysis."""

    def __init__(
        self,
        database: programs_database.ProgramsDatabase,
        evaluators: Sequence[evaluator.Evaluator],
        samples_per_prompt: int,
        prompt_manipulate,
    ) -> None:
        self._database = database
        self._evaluators = evaluators
        self._llm = LLM(samples_per_prompt)
        self._prompt_manipulate = prompt_manipulate

    def sample(self, iterations):
        """Continuously gets prompts, samples programs, sends them for analysis."""
        iter = 0

        while iter < iterations:

            iter += 1
            prompt = self._database.get_prompt()
            samples = self._llm.draw_samples(self._prompt_manipulate(prompt.code))
            Island_index = 0
            # best = self._database._best_program_per_island[0]
            score = self._database._best_score_per_island[Island_index]
            print(
                f"iteration {iter}: the best score in Island {Island_index} is {score}"
            )
            # This loop can be executed in parallel on remote evaluator machines.
            for sample in samples:
                chosen_evaluator = np.random.choice(self._evaluators)
                # remove the head of the function
                # the input to chosen_evaluator.analyse should only be the body
                """
                e.g.
                def foo():
                    return True
                =>
                return True
                """

                sample_body = "\n".join(sample.split("\n")[1:])
                chosen_evaluator.analyse(
                    sample_body, prompt.island_id, prompt.version_generated
                )
