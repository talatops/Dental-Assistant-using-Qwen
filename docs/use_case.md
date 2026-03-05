## Dental Clinic Appointment Assistant - Use Case

### Overview
The system is a conversational assistant for a dental clinic that helps patients get information about the clinic and request appointments. It runs on a local, CPU-only LLM and is exposed via a web chat interface and FastAPI backend.

### Primary Goals
- Answer frequently asked questions about the clinic (timings, services, dentists, payment options, insurance policy).
- Help patients request, confirm, or cancel appointments at the clinic.
- Collect all the relevant information needed for staff to finalize bookings offline (the bot does not directly access any scheduling tools).

### In-Scope Capabilities
- Provide information about:
  - Clinic working hours and days.
  - Types of treatments available (check-ups, cleanings, braces consultations, whitening, etc.).
  - Approximate visit durations and typical preparation instructions.
  - High-level pricing ranges or “starting from” pricing if configured.
  - Supported insurance policies and how claims usually work.
- Assist with appointment-related conversations:
  - New appointment requests (collecting name, contact details, preferred date/time, doctor preference, and reason for visit).
  - Rescheduling appointments (collecting old and new preferred slots).
  - Cancellations (confirming details and reason, if provided).
- Handle general conversational questions while staying within domain:
  - Directions to the clinic.
  - What to bring to the appointment.
  - Follow-up questions about what to expect after common procedures (only high-level information, no medical diagnosis).

### Out-of-Scope / Restrictions
- No real-time integration with clinic management software or calendars.
- No access to patient records, EMR, or personal health data beyond what the user types into the chat.
- No prescribing medication, diagnosing diseases, or providing treatment plans.
- No emergency triage: emergencies must always be directed to phone/ER instructions.
- No use of external tools, retrieval-augmented generation, or third-party LLM APIs.

### Target Users
- New or existing patients of the dental clinic.
- Administrative staff may optionally use the chat logs to process appointment requests.

### Environment & Constraints
- Runs on CPU-only infrastructure using a local, quantized Qwen model.
- Accessible through a ChatGPT-style web UI and a documented WebSocket API.
- Must support multiple concurrent user sessions.

### Success Criteria
- Patients can easily obtain answers to common clinic questions.
- Patients can submit appointment requests with all necessary information captured.
- The system maintains coherent, multi-turn conversations that respect the clinic’s policies and tone.

