"""Workflow utilities that do not depend on a particular LLM provider."""

from __future__ import annotations

from extraction_schema import (
    DocumentExtraction,
    HazardEvent,
    HazardTaskOutput,
    ImpactTaskOutput,
    LocationTaskOutput,
    TimeTaskOutput,
)


def _event_map(output) -> dict[str, object]:
    mapped = {event.event_id: event for event in output.events}
    if len(mapped) != len(output.events):
        raise ValueError(f"Duplicate event_id in {type(output).__name__}.")
    return mapped


def merge_decomposed_outputs(
    hazards: HazardTaskOutput,
    locations: LocationTaskOutput,
    times: TimeTaskOutput,
    impacts: ImpactTaskOutput,
) -> DocumentExtraction:
    """Merge four validated task outputs, rejecting silent event mismatches."""

    outputs = (locations, times, impacts)
    if any(output.document_id != hazards.document_id for output in outputs):
        raise ValueError("All task outputs must refer to the same document_id.")

    hazard_map = _event_map(hazards)
    location_map = _event_map(locations)
    time_map = _event_map(times)
    impact_map = _event_map(impacts)
    expected_ids = set(hazard_map)
    for name, mapping in (
        ("locations", location_map),
        ("times", time_map),
        ("impacts", impact_map),
    ):
        if set(mapping) != expected_ids:
            raise ValueError(f"{name} event IDs do not match the hazard task.")

    events = [
        HazardEvent(
            event_id=event_id,
            hazards=hazard_map[event_id].hazards,
            locations=location_map[event_id].locations,
            times=time_map[event_id].times,
            impacts=impact_map[event_id].impacts,
        )
        for event_id in (event.event_id for event in hazards.events)
    ]
    return DocumentExtraction(document_id=hazards.document_id, events=events)

