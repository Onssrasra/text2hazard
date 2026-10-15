"""Validated output schema shared by both Text2Hazard workflows.

The schema deliberately keeps extracted wording and normalized values separate.
Every predicted fact must carry a verbatim evidence quote so unsupported output
can be measured during evaluation.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    """Base model that rejects unexpected fields from model output."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Evidence(StrictModel):
    quote: str = Field(min_length=1, description="Verbatim supporting text from the document.")


class HazardCategory(str, Enum):
    FLOOD = "flood"
    STORM = "storm"
    EXTREME_HEAT = "extreme_heat"
    DROUGHT_LOW_WATER = "drought_low_water"
    WILDFIRE = "wildfire"
    COLD_SNOW = "cold_snow"
    OTHER = "other"


class HazardMention(StrictModel):
    category: HazardCategory
    source_text: str = Field(min_length=1, description="Hazard wording used in the source.")
    evidence: Evidence


class LocationMention(StrictModel):
    source_text: str = Field(min_length=1, description="Location wording used in the source.")
    normalized_name: str | None = None
    country_code: str | None = Field(
        default=None,
        pattern=r"^[A-Z]{2}$",
        description="ISO 3166-1 alpha-2 code when explicitly known; otherwise null.",
    )
    evidence: Evidence


class TimeMention(StrictModel):
    source_text: str = Field(min_length=1, description="Temporal wording used in the source.")
    normalized_start: str | None = Field(
        default=None,
        description="ISO date or datetime when supported by the text; otherwise null.",
    )
    normalized_end: str | None = Field(
        default=None,
        description="ISO end date or datetime for an interval; otherwise null.",
    )
    evidence: Evidence


class ImpactCategory(str, Enum):
    HUMAN_HEALTH = "human_health"
    INFRASTRUCTURE = "infrastructure"
    TRANSPORT = "transport"
    UTILITIES = "utilities"
    ECONOMIC = "economic"
    ENVIRONMENTAL = "environmental"
    OTHER = "other"


class ImpactMention(StrictModel):
    category: ImpactCategory
    description: str = Field(min_length=1)
    evidence: Evidence


class HazardEvent(StrictModel):
    event_id: str = Field(min_length=1, description="Document-local stable ID such as event_01.")
    hazards: list[HazardMention] = Field(default_factory=list)
    locations: list[LocationMention] = Field(default_factory=list)
    times: list[TimeMention] = Field(default_factory=list)
    impacts: list[ImpactMention] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_hazard(self) -> "HazardEvent":
        if not self.hazards:
            raise ValueError("Each event must contain at least one supported hazard mention.")
        return self


class DocumentExtraction(StrictModel):
    document_id: str = Field(min_length=1)
    events: list[HazardEvent] = Field(default_factory=list)
    notes: list[str] = Field(
        default_factory=list,
        description="Annotation or parsing notes; never a substitute for extracted facts.",
    )


class HazardTaskEvent(StrictModel):
    event_id: str = Field(min_length=1)
    hazards: list[HazardMention] = Field(min_length=1)


class HazardTaskOutput(StrictModel):
    document_id: str = Field(min_length=1)
    events: list[HazardTaskEvent] = Field(default_factory=list)


class LocationTaskEvent(StrictModel):
    event_id: str = Field(min_length=1)
    locations: list[LocationMention] = Field(default_factory=list)


class LocationTaskOutput(StrictModel):
    document_id: str = Field(min_length=1)
    events: list[LocationTaskEvent] = Field(default_factory=list)


class TimeTaskEvent(StrictModel):
    event_id: str = Field(min_length=1)
    times: list[TimeMention] = Field(default_factory=list)


class TimeTaskOutput(StrictModel):
    document_id: str = Field(min_length=1)
    events: list[TimeTaskEvent] = Field(default_factory=list)


class ImpactTaskEvent(StrictModel):
    event_id: str = Field(min_length=1)
    impacts: list[ImpactMention] = Field(default_factory=list)


class ImpactTaskOutput(StrictModel):
    document_id: str = Field(min_length=1)
    events: list[ImpactTaskEvent] = Field(default_factory=list)


