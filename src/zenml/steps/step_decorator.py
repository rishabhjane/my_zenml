#  Copyright (c) ZenML GmbH 2021. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

import types
from typing import Callable, Type, Union

from zenml.steps.base_step import STEP_INNER_FUNC_NAME, BaseStep


def step(
    _func: types.FunctionType = None, *, name: str = None
) -> Union[BaseStep, Callable[..., BaseStep]]:
    """Outer decorator function for the creation of a ZenML step

    In order to be able work with parameters such as `name`, it features a
    nested decorator structure.

    Args:
        _func: Optional func from outside.
        name (required) the given name for the step.

    Returns:
        the inner decorator which creates the step class based on the
        ZenML BaseStep
    """

    def inner_decorator(func: types.FunctionType) -> Type:
        """Inner decorator function for the creation of a ZenML Step

        Args:
          func: types.FunctionType, this function will be used as the
            "process" method of the generated Step

        Returns:
            The class of a newly generated ZenML Step.
        """
        return type(
            name if name else func.__name__,
            (BaseStep,),
            {STEP_INNER_FUNC_NAME: staticmethod(func)},
        )

    if _func is None:
        return inner_decorator
    else:
        return inner_decorator(_func)
