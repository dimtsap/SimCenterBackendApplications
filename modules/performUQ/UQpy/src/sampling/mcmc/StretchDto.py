from __future__ import annotations

from typing import Literal, Annotated, Union

from pydantic import Field

from src.UQpyDTO import UQpyDTO
from src.sampling.mcmc.ModifiedMetropolisHastingsDto import ModifiedMetropolisHastingsDto


class StretchDto(UQpyDTO):
    method: Literal['Stretch'] = 'Stretch'
    burn_length: int = Field(default=0, alias='burn-in', ge=0)
    jump: int = Field(default=1, ge=0)
    dimension: int = Field(..., gt=0)
    n_chains: int = Field(default=2, alias='numChains', ge=2)
    random_state: int = Field(..., alias='randomState')
    scale: float = Field(..., gt=0)

    def init_to_text(self):
        from UQpy.sampling.mcmc.Stretch import Stretch
        c = Stretch

        class_name = c.__module__.split(".")[-1]
        import_statement = "from " + c.__module__ + " import " + class_name + "\n"

        stretch_parameters = self.dict()
        stretch_parameters.pop("method")
        stretch_parameters["log_pdf_target"] = f"marginals.log_pdf"
        stretch_parameters["seed"] = f"list(marginals.rvs({self.n_chains},))"
        str_parameters = str()
        for key in stretch_parameters:
            if stretch_parameters[key] is None: continue
            str_parameters += key + "=" + str(stretch_parameters[key]) + ","

        # prerequisite_str = import_statement + import_likehood_statement
        prerequisite_str = import_statement
        prerequisite_str += "sampling = " + class_name + "(" + str_parameters + ")\n"
        sampling_str = "sampling"

        return (prerequisite_str, sampling_str)


SamplingMethod = Annotated[Union[StretchDto, ModifiedMetropolisHastingsDto], Field(discriminator='method')]