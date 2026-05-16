# **Product conceptualizer with A2A Integration**

**Overview**  
This Product Conceptualizer project provides an AI-powered agent system for generating detailed, structured product concepts from simple business ideas. It leverages Google’s ADK (Agent Development Kit), A2A (Agent-to-Agent) protocol, and Microsoft Agent Framework to enable interactions.

**A2A Integration Workflow**  
<img src="https://github.com/cloudalchemy-ai/MAF/blob/main/Build_real_world_agents/Product_conceptualizer/fig1.jpg?raw=true" alt="Product conceptualizer" width="700"/>

>**Key Features**

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

→ product\_conceptualizer\_agent

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

| cd product\_conceptualizer\_agent |
| :---- |

   

5. Run the A2A remote server

| python \_\_main\_\_.py |
| :---- |

6. Now the A2A server is up and running. Make sure the Remote agent server URL is given in the environment variable. Then in another terminal, redirect to parent directory and run agent\_with\_a2a.py

cd ..  
python agent\_with\_a2a.py

7. Enter the product idea to the agent.

**Remote agent setup**  
<img src="https://github.com/cloudalchemy-ai/MAF/blob/main/Build_real_world_agents/Product_conceptualizer/fig2.jpg?raw=true" alt="Product conceptualizer" width="300"/>

1. **agent.py**
   Defines the remote agent and declares it as a root agent.
2. **agentexecutor.py**  
   Activates the agent, making it accessible to the host agent. Serves as a link between the host and remote agents.  
3. **main.py**
   Initializes and activates the remote agent.  
   

   
