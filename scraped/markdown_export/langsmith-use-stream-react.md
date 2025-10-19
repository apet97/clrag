# langsmith-use-stream-react

> Source: https://docs.langchain.com/langsmith/use-stream-react

The useStream() React hook provides a seamless way to integrate LangGraph into your React applications. It handles all the complexities of streaming, state management, and branching logic, letting you focus on building great chat experiences.Key features:
Messages streaming: Handle a stream of message chunks to form a complete message
Automatic state management for messages, interrupts, loading states, and errors
Conversation branching: Create alternate conversation paths from any point in the chat history
UI-agnostic design: bring your own components and styling
Let’s explore how to use useStream() in your React application.The useStream() provides a solid foundation for creating bespoke chat experiences. For pre-built chat components and interfaces, we also recommend checking out CopilotKit and assistant-ui.
The useStream() hook takes care of all the complex state management behind the scenes, providing you with simple interfaces to build your UI. Here’s what you get out of the box:
Thread state management
Loading and error states
Interrupts
Message handling and updates
Branching support
Here are some examples on how to use these features effectively:
The useStream() hook can automatically resume an ongoing run upon mounting by setting reconnectOnMount: true. This is useful for continuing a stream after a page refresh, ensuring no messages and events generated during the downtime are lost.
By default the ID of the created run is stored in window.sessionStorage, which can be swapped by passing a custom storage in reconnectOnMount instead. The storage is used to persist the in-flight run ID for a thread (under lg:stream:${threadId} key).
You can also manually manage the resuming process by using the run callbacks to persist the run metadata and the joinStream function to resume the stream. Make sure to pass streamResumable: true when creating the run; otherwise some events might be lost.
Copy
import type { Message } from "@langchain/langgraph-sdk";import { useStream } from "@langchain/langgraph-sdk/react";import { useCallback, useState, useEffect, useRef } from "react";export default function App() { const [threadId, onThreadId] = useSearchParam("threadId"); const thread = useStream<{ messages: Message[] }>({ apiUrl: "http://localhost:2024", assistantId: "agent", threadId, onThreadId, onCreated: (run) => { window.sessionStorage.setItem(`resume:${run.thread_id}`, run.run_id); }, onFinish: (_, run) => { window.sessionStorage.removeItem(`resume:${run?.thread_id}`); }, }); // Ensure that we only join the stream once per thread. const joinedThreadId = useRef<string | null>(null); useEffect(() => { if (!threadId) return; const resume = window.sessionStorage.getItem(`resume:${threadId}`); if (resume && joinedThreadId.current !== threadId) { thread.joinStream(resume); joinedThreadId.current = threadId; } }, [threadId]); return ( <form onSubmit={(e) => { e.preventDefault(); const form = e.target as HTMLFormElement; const message = new FormData(form).get("message") as string; thread.submit( { messages: [{ type: "human", content: message }] }, { streamResumable: true } ); }} > <div> {thread.messages.map((message) => ( <div key={message.id}>{message.content as string}</div> ))} </div> <input type="text" name="message" /> <button type="submit">Send</button> </form> );}// Utility method to retrieve and persist data in URL as search paramfunction useSearchParam(key: string) { const [value, setValue] = useState<string | null>(() => { const params = new URLSearchParams(window.location.search); return params.get(key) ?? null; }); const update = useCallback( (value: string | null) => { setValue(value); const url = new URL(window.location.href); if (value == null) { url.searchParams.delete(key); } else { url.searchParams.set(key, value); } window.history.pushState({}, "", url.toString()); }, [key] ); return [value, update] as const;}
The useStream() hook will keep track of the message chunks received from the server and concatenate them together to form a complete message. The completed message chunks can be retrieved via the messages property.By default, the messagesKey is set to messages, where it will append the new messages chunks to values["messages"]. If you store messages in a different key, you can change the value of messagesKey.
Copy
import type { Message } from "@langchain/langgraph-sdk";import { useStream } from "@langchain/langgraph-sdk/react";export default function HomePage() { const thread = useStream<{ messages: Message[] }>({ apiUrl: "http://localhost:2024", assistantId: "agent", messagesKey: "messages", }); return ( <div> {thread.messages.map((message) => ( <div key={message.id}>{message.content as string}</div> ))} </div> );}
Under the hood, the useStream() hook will use the streamMode: "messages-tuple" to receive a stream of messages (i.e. individual LLM tokens) from any LangChain chat model invocations inside your graph nodes. Learn more about messages streaming in the streaming guide.
For each message, you can use getMessagesMetadata() to get the first checkpoint from which the message has been first seen. You can then create a new run from the checkpoint preceding the first seen checkpoint to create a new branch in a thread.A branch can be created in following ways:
Edit a previous user message.
Request a regeneration of a previous assistant message.
For advanced use cases you can use the experimental_branchTree property to get the tree representation of the thread, which can be used to render branching controls for non-message based graphs.
You can optimistically update the client state before performing a network request to the agent, allowing you to provide immediate feedback to the user, such as showing the user message immediately before the agent has seen the request.
Use the initialValues option to display cached thread data immediately while the history is being loaded from the server. This improves user experience by showing cached data instantly when navigating to existing threads.
Copy
import { useStream } from "@langchain/langgraph-sdk/react";const CachedThreadExample = ({ threadId, cachedThreadData }) => { const stream = useStream({ apiUrl: "http://localhost:2024", assistantId: "agent", threadId, // Show cached data immediately while history loads initialValues: cachedThreadData?.values, messagesKey: "messages", }); return ( <div> {stream.messages.map((message) => ( <div key={message.id}>{message.content as string}</div> ))} </div> );};
Use the threadId option in submit function to enable optimistic UI patterns where you need to know the thread ID before the thread is actually created.
Copy
import { useState } from "react";import { useStream } from "@langchain/langgraph-sdk/react";const OptimisticThreadExample = () => { const [threadId, setThreadId] = useState<string | null>(null); const [optimisticThreadId] = useState(() => crypto.randomUUID()); const stream = useStream({ apiUrl: "http://localhost:2024", assistantId: "agent", threadId, onThreadId: setThreadId, // (3) Updated after thread has been created. messagesKey: "messages", }); const handleSubmit = (text: string) => { // (1) Perform a soft navigation to /threads/${optimisticThreadId} // without waiting for thread creation. window.history.pushState({}, "", `/threads/${optimisticThreadId}`); // (2) Submit message to create thread with the predetermined ID. stream.submit( { messages: [{ type: "human", content: text }] }, { threadId: optimisticThreadId } ); }; return ( <div> <p>Thread ID: {threadId ?? optimisticThreadId}</p> {/* Rest of component */} </div> );};
The useStream() hook is friendly for apps written in TypeScript and you can specify types for the state to get better type safety and IDE support.
Copy
// Define your typestype State = { messages: Message[]; context?: Record<string, unknown>;};// Use them with the hookconst thread = useStream<State>({ apiUrl: "http://localhost:2024", assistantId: "agent", messagesKey: "messages",});
You can also optionally specify types for different scenarios, such as:
ConfigurableType: Type for the config.configurable property (default: Record<string, unknown>)
InterruptType: Type for the interrupt value - i.e. contents of interrupt(...) function (default: unknown)
CustomEventType: Type for the custom events (default: unknown)
UpdateType: Type for the submit function (default: Partial<State>)
If you’re using LangGraph.js, you can also reuse your graph’s annotation types. However, make sure to only import the types of the annotation schema in order to avoid importing the entire LangGraph.js runtime (i.e. via import type { ... } directive).