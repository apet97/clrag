---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-use-studio",
  "h1": "langsmith-use-studio",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.447047",
  "sha256_raw": "f57cf5567e748c54b895724e4a3f77732fff349e326f81d1e011a6552d30b872"
}
---

# langsmith-use-studio

> Source: https://docs.langchain.com/langsmith/use-studio

- Run application: Execute your application or agent and observe its behavior.
- Manage assistants: Create, edit, and select the assistant configuration used by your application.
- Manage threads: View and organize the threads, including forking or editing past runs for debugging.
Run application
- Graph
- Chat
Specify input
- Define the input to your graph in the Input section on the left side of the page, below the graph interface. Studio will attempt to render a form for your input based on the graph’s defined state schema. To disable this, click the View Raw button, which will present you with a JSON editor.
- Click the up or down arrows at the top of the Input section to toggle through and use previously submitted inputs.
Run settings
Assistant
To specify the assistant that is used for the run:- Click the Settings button in the bottom left corner. If an assistant is currently selected the button will also list the assistant name. If no assistant is selected it will say Manage Assistants.
- Select the assistant to run.
- Click the Active toggle at the top of the modal to activate it.
Streaming
Click the dropdown next to Submit and click the toggle to enable or disable streaming.Breakpoints
To run your graph with breakpoints:- Click Interrupt.
- Select a node and whether to pause before or after that node has executed.
- Click Continue in the thread log to resume execution.
Submit run
To submit the run with the specified input and run settings:Manage assistants
Studio lets you view, edit, and update your assistants, and allows you to run your graph using these assistant configurations. For more conceptual details, refer to the Assistants overview.- Graph
- Chat
To view your assistants:
- Click Manage Assistants in the bottom left corner. This opens a modal for you to view all the assistants for the selected graph.
- Specify the assistant and its version you would like to mark as Active. LangSmith will use this assistant when runs are submitted.
Manage threads
Studio provides tools to view all threads saved on the server and edit their state. You can create new threads, switch between threads, and modify past states both in graph mode and chat mode.- Graph
- Chat
View threads
- In the top of the right-hand pane, select the dropdown menu to view existing threads.
- Select the desired thread, and the thread history will populate in the right-hand side of the page.
- To create a new thread, click + New Thread and submit a run.
- To view more granular information in the thread, drag the slider at the top of the page to the right. To view less information, drag the slider to the left. Additionally, collapse or expand individual turns, nodes, and keys of the state.
- Switch between
Pretty
andJSON
mode for different rendering formats.
Edit thread history
To edit the state of the thread:- Select Edit node state next to the desired node.
- Edit the node’s output as desired and click Fork to confirm. This will create a new forked run from the checkpoint of the selected node.