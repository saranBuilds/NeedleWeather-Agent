# Agent Interaction Log: Weather Query

This document tracks an instance of the agent-tool execution flow, capturing the chain of logic from a user's prompt to an external API call and the final natural language answer.

## 🔄 Interaction Diagram

```text
User
  │
  │ "What is the temperature in Madurai?"
  ▼
Needle (Agent)
  │
  │ decides → get_temperature(city="Madurai")
  ▼
Weather Tool
  │
  │ calls external weather API
  ▼
Temperature Result
  │
  │ returns raw data (e.g., 31°C)
  ▼
Needle / Agent
  │
  ▼
"Madurai is currently 31°C"
```

---

## 📑 Trace Context & Execution Logs

| Trace Step | Actor | Action / Output | Meaning |
| :--- | :--- | :--- | :--- |
| **01** | `User` | Input: `"What is the temperature in Madurai?"` | Request for real-time external information. |
| **02** | `Needle / Agent` | Intent Parsed → Tool Call: `get_temperature(city="Madurai")` | The LLM core identifies it cannot answer natively and routes to a registered tool. |
| **03** | `Weather Tool` | Request Payload: `GET /v1/current?q=Madurai` | Execution layer communicates with a downstream environment or service. |
| **04** | `External API` | Response Body: `{"location": "Madurai", "temp_c": 31}` | Raw metrics fetched successfully. |
| **05** | `Needle / Agent` | Synthesis Generation | Combines raw context back into user-friendly interface language. |
| **06** | `System Output` | Final Text: `"Madurai is currently 31°C"` | Goal completed. |

---

## 🛠️ Associated Tool Definition

```json
{
  "name": "get_temperature",
  "description": "Fetches the current temperature in Celsius for a given city.",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "The name of the target city (e.g., Madurai)."
      }
    },
    "required": ["city"]
  }
}
```