CS 4063 - Natural Language Processing
Due Date: Friday, March 6th by 11:55pm.
Assignments are to be done in groups of two or three. No late assignments will be accepted.
Submissions that do not comply with the specifications given in this document will not be marked
and a zero grade will be assigned.
You are allowed to use all the generative tools that you have access to. But you should generate the minimal
possible code to implement the reqired functionality. You should also be able to explain the code and produce
the prompts when asked. Be careful, this is not a one shot assignment and requires multiple pieces
to be executed separately before it all come together. Learn!
Each group must submit a single GitHub repository link on Google Classroom, containing all code, docu-
mentation, models, deployment scripts, and test cases. Also submit the vercel link that you have deployed your
app on. Do not submit your code, models, docker files on Google Classroom. A short loom video to
demo your system is optional but recommended.
Conversational AI System
Large Language Models (LLMs) have enabled powerful conversational agents capable of performing natural
dialogue, reasoning, and task execution. However, deploying such systems in production environments requires
careful system design, orchestration, concurrency handling, and optimization for latency and resource constraints.
In this assignment, you will design and implement a fully functional conversational AI system that
runs entirely locally on CPU, exposes a real-time conversational API, and provides a minimal web-based
chat interface. The focus of this assignment is on system engineering, orchestration, deployment, and
performance rather than model training.
Important Constraint: For this assignment, Tools and Retrieval-Augmented Generation (RAG)
are strictly disallowed. The system must rely purely on prompt orchestration and conversational
memory/state.
1 Overall Objective
The objective is to build a low-latency, production-style conversational AI system that:
 Runs on a laptop using quantized open-weight LLMs,
 Supports real-time streaming interaction,
 Maintains conversation state,
 Handles concurrent users,
 Exposes a clean API,
 Provides a ChatGPT-style web interface.
1
2 System Architecture Overview
Your system must follow the general architecture below. However, you should design and properly split the
conversation manager into the required microservices:
Web UI ↔ FastAPI + WebSocket ↔ Conversation Manager ↔ Local LLM Engine
The system should consist of the following components:
 Frontend: Web-based chat interface
 Backend API: FastAPI server with REST + WebSocket endpoints
 Conversation Manager: Session handling, history management, prompt orchestration
 LLM Engine: Locally running inference using quantized models
Tools and RAG modules must not be included in the system design.
3 Phase-wise Assignment Tasks
3.1 Phase I: Business Case Selection
Each group must select a realistic conversational business use-case. For example:
 Dental clinic appointment scheduling assistant
 University admissions inquiry chatbot
 Airline booking assistant (information only)
 Hotel front-desk virtual assistant
 Customer support chatbot for a small business
Your chatbot must strictly follow the conversational tone, policies, and constraints of the selected business
domain.
Deliverables:
 Use-case description
 Example dialogues
 Conversation flow design
3.2 Phase II: Local LLM Selection and Optimization
Select a small, CPU-friendly instruction-tuned model, such as:
 Qwen 0.6B – 4B (quantized GGUF)
 Phi series
 LiquidAI 1.2B
You can:
 Run inference using llama.cpp, vLLM, or Ollama.
 Use quantized models.
 Optimize for latency and memory footprint.
Deliverables:
 Context memory management scheme (filtering signal from the noise)
 Inference latency benchmarks
2
3.3 Phase III: Conversation Manager and Prompt Orchestration
Implement a conversation manager that:
 Maintains dialogue history
 Enforces conversation policies
 Handles turn-taking logic
 Builds structured system prompts
 Supports multi-turn reasoning with fidelity to previous context
Important: You may not use tools, agents, plugins, or RAG. All intelligence must come from:
 Prompt design
 Context window management
Deliverables:
 Prompt templates
 Conversation orchestration logic
 Multi-turn dialogue tests
3.4 Phase IV: Microservice API Implementation
Develop a containerized backend microservice with:
 WebSocket endpoint: /ws/chat
 JSON-based request and response format
Functional requirements:
 Asynchronous request handling
 Concurrent user support
 Streaming token output (preferred)
 Robust error handling
Deliverables:
 FastAPI service
 WebSocket streaming
 Dockerized deployment
 Postman test collection
3
3.5 Phase V: Web-Based Chat Interface
Develop a simple ChatGPT-style web interface that supports:
 Real-time messaging
 Streaming responses
 Conversation history
 Reset / new session functionality
Deliverables:
 HTML/JS or React frontend
 WebSocket integration
 Clean UI/UX
3.6 Phase VI: Production Readiness and Evaluation
Prepare your system for production-like conditions:
 Latency benchmarking
 Stress testing
 Failure handling
Submit a detailed README.md to describe the architecture of your system and the evaluations that you
have run to test the correctness of your system
4 System Features
Your conversational system must support:
 Fully local inference (no cloud APIs)
 Instruction-tuned conversational responses
 Context tracking across turns
 CPU-optimized inference
 Streaming output
 Stateless backend
5 Submission Guidelines
Each group must submit:
1. GitHub repository (source code)
2. dockerfile + deployment scripts
3. Postman API collection
4. Web UI frontend
5. README.md should include:
4
 Setup instructions
 Architecture diagram
 Model selection
 Performance benchmarks
 Known limitations
Honor Policy
Cheating in code, datasets, or reports will result in an immediate zero grade and reporting to the academic
disciplinary committee. All work must be original to the group