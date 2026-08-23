# Project Ideas

Just some first ideas for the project so we can discuss the direction.

Nothing here is fixed yet.

## Given topic

**Text2Data: extracting hazard types, geolocation, time and impacts**

The general idea is to take text from e.g. newspaper articles or research papers about natural hazards and convert the information into structured data.

Things we could try to extract:

* hazard type
* location
* date/time
* impacts / damages

## Pipeline idea (Ons)

One possible pipeline could be:

**Documents**

→ some preprocessing

→ LLM extracts the information

→ validate the output with Pydantic

→ save it as structured data

→ later use/query/analyse the data

This is just a first idea and we should discuss if it makes sense.

## Pydantic

Pydantic is a Python library where we can define what kind of output we expect.

For example, instead of letting the LLM return random text, we could define something like:

```python
class HazardEvent(BaseModel):
    hazard_type: str | None
    locations: list[str]
    event_date: str | None
    impacts: list[str]
```

So the LLM should return the same kind of structure every time.

Possible types could be:

* `hazard_type`: text, maybe later fixed categories
* `locations`: list of locations
* `event_date`: text at first, maybe later a real `date`
* `impacts`: list of impacts/damages

Later we could make this more detailed, for example with country, city, coordinates, impact type, evidence from the source text, etc.

## LLM architecture ideas

### Option 1: one LLM

One LLM gets the document and extracts everything at once:

* hazard
* location
* date
* impact

### Option 2: split it into several parts

For example:

* one step for hazard type
* one step for locations
* one step for dates
* one step for impacts

Then combine everything into the same Pydantic output.

Could be interesting to compare if splitting the task helps or if one LLM call is already enough.

Not sure yet if we really need "agents" or if a normal pipeline with several LLM calls is better/simpler.

## How to store the result

After extraction we need to decide how to save the information.

Ideas:

* normal table / dataframe / database
* knowledge graph

Knowledge graph could be interesting because we could have relations like:

`Flood -> occurred in -> Valencia`

`Flood -> happened on -> 2024-10-29`

`Flood -> caused -> transport disruption`

Not sure yet if this should be part of the main research question or just something we show at the end.

## Evaluation ideas

We probably need some manually labelled examples so we know if the extraction is actually correct.

Could compare things like:

* hazard extraction
* location extraction
* date extraction
* impact extraction
* hallucinated information
* runtime / number of LLM calls

Possible metrics could be precision, recall and F1, depending on what exactly we decide to extract.

## Things we still need to discuss

* final research question
* which fields we actually want to extract
* which LLM/model(s) to use
* one LLM vs split pipeline
* whether agents are needed
* whether to compare zero-shot and few-shot prompting
* how much data to label manually
* if impacts/damages should be included
* if we want to use a knowledge graph
* how to split the work between us
