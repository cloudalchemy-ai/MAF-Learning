# Idea Generator and Validator

**Overview**  
This project integrates **CrewAI** agents, tasks, and processes to generate and validate business ideas using an external **N8N workflow** for idea generation. The system is designed to be invoked via **Microsoft Agent framework** and follows a structured workflow.

**Idea Generator and Validator workflow**

<img src="https://github.com/cloudalchemy-ai/MAF/blob/main/Build_real_world_agents/Idea_generator_and_validator/Image.jpg?raw=true" alt="Idea generator" width="700"/>
**Key Features**

1. Automated Idea Generation : Uses an N8N webhook to generate business ideas from user prompts.  
2. Structured Validation : Evaluates ideas based on market demand, uniqueness, scalability, revenue potential, and risks.  
3. CrewAI Integration : Leverages CrewAI agents, tasks, and sequential process orchestration for smooth execution.  
4. Modular Design : Separates idea generation, validation, and workflow execution for maintainability and scalability.  
5. Runs via Agent Framework : Fully integrated with Microsoft Agent Framework for effortless Agentic communication.

**Prerequisites**

Before starting, make sure you have:

* Python 3.8 or higher.  
* Pip for installing packages.  
* Google API key for N8N setup.  
* OpenAI model name and API key set in an environment variable.

**Project Structure**

Your project should look like this : 	

→ A2a inspector

→ remote\_agent

→ \_\_init\_\_.py

→ agent.py

→ agent\_executor.py

→ \_\_main\_\_.py

→ utils.py

→ .env

**N8N Webhook Setup**


1. Visit [https://n8n.io/](https://n8n.io/) and login or start a new trial(14 days).  
2. Start the workspace.  
3. Click the “start from scratch” option.  
4. Click on “ Add first step” and select “Webhook” from the dropdown. Setup the parameters as follows : 


5. Copy the Test URL from the parameters and add it in the .env file.  
   Eg : N8N\_WEBHOOK\_URL=https://sreevidya.app.n8n.cloud/webhook-test/ideagen  
     
6. Click on the \+ button on the right side of the webhook.  Select AI → Google Gemini → Message a model. Set the parameters as follows :     
   Prompt :   
   ‘ ‘ ‘  
   Generate one well-structured and innovative business idea based on the user's input: {{ $json.body.prompt }}.    
   Ensure the idea is:  
   \- Relevant to the user's requirements    
   \- Feasible and realistic    
   \- Includes a short name, description, target audience, potential revenue model, and unique selling point (USP)    
   ‘ ‘ ‘  
   In settings, turn on Always output data option.   
7. Click on the \+ to add another node on the message a model node to add Respond to webhook node with the following parameters :  
   Response body : {{ $json.candidates\[0\].content.parts\[0\].text }}  
    ![][image6]  
8. Click “Execute workflow” to get the app up and running.


**Remote agent (N8N \+ CrewAI) setup**

1. Business idea generator tool :   
   1. Acts as an external tool for AI agents.   
   2. Calls an N8N workflow to generate business ideas and returns the raw response from the webhook.  
2. BusinessIdeaAgent Class :  
   1. Encapsulates the idea validation workflow.  
   2. It combines agent logic, task definition and execution flow.  
3. Validator agent :  
   1. Act as a business idea validator agent.  
   2. Call a business idea generator tool and validate the idea and return the validation results. 

**Running the system**

1. Setup and activate the virtual environment.  
2. In the terminal run “ pip install \-r requirements.txt” to install the requirements.  
3. Make sure the N8N workflow is executed (mandatory for each prompt).   
4. Make sure  the .env file has the necessary values.  
   Eg : 

| MODEL=gpt-4o-miniOPENAI\_API\_KEY=your\_api\_key N8N\_WEBHOOK\_URL=[https://yourapp.app.n8n.cloud/webhook-test/appname](https://yourapp.app.n8n.cloud/webhook-test/appname) A2A\_AGENT\_HOST=[http://localhost:10011/](http://localhost:10011/)  \#URL of the remote agent |
| :---- |

   

5. From the parent directory, run 

| python \-m remote\_agent |
| :---- |

   

6. Now that the server is up and running, make sure N8N is Executing Workflow, and run agent\_with\_a2a.py in a new terminal.

| \#Execute the agent framework python agent\_with\_a2a.py |
| :---- |

7. Now we can enter our prompt to the Agent framework. 
