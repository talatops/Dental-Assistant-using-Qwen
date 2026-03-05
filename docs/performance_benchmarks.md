## Performance Benchmarks - Dental Clinic Assistant

This document is intended to capture latency and throughput measurements for the local Qwen model
and the end-to-end system. Update the table below after running the benchmark scripts.

### Model Inference Benchmarks

Script: `backend/scripts/benchmark_latency.py`


| Prompt ID | Description                                    | Time to First Token (s) | Total Time (s) | Tokens Generated (approx words) | Tokens/sec (approx) |
| --------- | ---------------------------------------------- | ----------------------- | -------------- | ------------------------------- | -------------------- |
| 1         | Assistant introduction                         | N/A                     | 3.840          | 35                              | 9.11                 |
| 2         | Appointment booking request                    | N/A                     | 5.382          | 127                             | 23.60                |
| 3         | Explanation of routine dental cleaning (short) | N/A                     | 7.732          | 231                             | 29.88                |


### WebSocket Stress Test

Script: `backend/scripts/stress_test_ws.py`


| Clients | Description                        | Observations (latency, errors, stability) |
| ------- | ---------------------------------- | ----------------------------------------- |
| 5       | Concurrent appointment requests    | Per-client total times ≈ 10.412, 11.933, 11.810, 11.725, 11.078s; average ≈ 11.392s; no errors observed. |
| 10      | (optional) heavier concurrent load |                                           |


