## Conversation Flow - Dental Clinic Assistant

This document describes the high-level conversation flow for the dental clinic assistant.

```mermaid
flowchart TD
  start[Start] --> greetUser["Greet user and introduce clinic assistant"]
  greetUser --> getIntent["Ask how you can help"]

  getIntent -->|Appointment request| apptFlow["Appointment request flow"]
  getIntent -->|Reschedule/cancel| changeFlow["Reschedule/cancel flow"]
  getIntent -->|General question| faqFlow["FAQ / information flow"]
  getIntent -->|Out of scope / emergency| safetyFlow["Safety and escalation flow"]

  subgraph apptFlowSub [Appointment Request]
    apptFlow --> collectName["Collect name"]
    collectName --> collectContact["Collect contact number"]
    collectContact --> collectDateTime["Ask preferred date/time"]
    collectDateTime --> collectDoctorPref["Ask for doctor preference (optional)"]
    collectDoctorPref --> collectReason["Ask reason for visit"]
    collectReason --> confirmSummary["Summarize request and confirm details"]
    confirmSummary --> submitAppt["Mark request as pending for staff"]
  end

  subgraph changeFlowSub [Reschedule / Cancel]
    changeFlow --> confirmIdentity["Collect name and basic appointment details"]
    confirmIdentity --> askNewSlot["Ask for new preferred slot or confirm cancellation"]
    askNewSlot --> summarizeChange["Summarize change/cancellation for staff"]
  end

  subgraph faqFlowSub [FAQ / Info]
    faqFlow --> classifyQuestion["Classify question (timings, services, insurance, etc.)"]
    classifyQuestion --> answerFAQ["Answer using clinic policies and generic information"]
    answerFAQ --> offerMoreHelp["Ask if anything else is needed"]
  end

  subgraph safetyFlowSub [Safety / Out-of-Scope]
    safetyFlow --> identifyEmergency["Detect emergencies, diagnosis, or prescriptions"]
    identifyEmergency --> adviseContact["Advise to call clinic or seek medical help"]
  end

  submitAppt --> endNode[End]
  summarizeChange --> endNode
  offerMoreHelp -->|User done| endNode
  adviseContact --> endNode
```

### Key Policy Points
- The assistant always:
  - Avoids diagnosis and medication recommendations.
  - Redirects emergencies to phone/ER.
  - Confirms details before treating an appointment request as final.
- The assistant uses previous turns to remember the patient’s details and reason for visit within the current conversation.

