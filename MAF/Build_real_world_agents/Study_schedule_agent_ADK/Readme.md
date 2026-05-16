# **Study Scheduler agent using A2A**

**Overview**  
The calendar is generated using the Microsoft Agent Framework (MAF). When requested, the study-schedule agent creates a customized schedule based on user requirements while considering the calendar,  through the Google ADK. In this setup, the A2A agent is integrated as an MAF agent.

**A2A Integration Workflow**  
<img src="https://github.com/cloudalchemy-ai/MAF/blob/main/Orchestration_workflows/Concurrent_orchestration/Image.jpg?raw=true" alt="Study schedule agent" width="700"/>

**Key Features**

1. Google ADK  
2. Gemini API Key  
3. Agent framework  
4. A2A

**Prerequisites**

Before starting, make sure you have:

* Remote agent URL and Google API key set in environment variable.  
  * A2A\_AGENT\_HOST\="http://localhost:10001"  
  * GOOGLE\_API\_KEY\="Your API Key"


* Agent-framework installed.  
  * pip install agent-framework

**Project Structure**

Your project should look like this : 	

→ A2A\_remote\_agent

→ agent.py

→ init.py

→ agent\_executor.py

→ \_\_main\_\_.py

		→ agent\_with\_a2a.py

→ .env

**Agent framework setup and execution**

1. Setup and activate the virtual environment.  
2. In the terminal run “ pip install \-r requirements.txt” to install the requirements.  
3. Make sure necessary environment variables are set in the .env file.  
4. From the parent directory, run 

| cd A2A\_remote\_agent |
| :---- |

   

5. Run the A2A remote server

| python \_\_main\_\_.py |
| :---- |

6. Now the A2A server is up and running. Make sure the Remote agent server URL is given in the environment variable. Then redirect to parent directory and run agent\_with\_a2a.py

python agent\_with\_a2a.py

7. Enter the input.  

I want to learn Python and I would like to spend 3 hours a day. Also, I am a visual learner.
