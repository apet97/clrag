---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-integrations-chat-google-generative-ai",
  "h1": "oss-javascript-integrations-chat-google-generative-ai",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.446158",
  "sha256_raw": "f52fa4c1a538cd5db2c906988254fa1e2cc28357ea6f3bf69dddbe3fc6c25780"
}
---

# oss-javascript-integrations-chat-google-generative-ai

> Source: https://docs.langchain.com/oss/javascript/integrations/chat/google_generative_ai

Google AI offers a number of different chat models, including the powerful Gemini series. For information on the latest models, their features, context windows, etc. head to the Google AI docs.This will help you getting started with ChatGoogleGenerativeAIchat models. For detailed documentation of all ChatGoogleGenerativeAI features and configurations head to the API reference.
You can access Google’s gemini and gemini-vision models, as well as other
generative models in LangChain through ChatGoogleGenerativeAI class in the
@langchain/google-genai integration package.
Copy
<Tip>**You can also access Google's `gemini` family of models via the LangChain VertexAI and VertexAI-web integrations.**Click [here](/oss/javascript/integrations/chat/google_vertex_ai) to read the docs.</Tip>
const aiMsg = await llm.invoke([ [ "system", "You are a helpful assistant that translates English to French. Translate the user sentence.", ], ["human", "I love programming."],])aiMsg
Gemini models have default safety settings that can be overridden. If you are receiving lots of “Safety Warnings” from your models, you can try tweaking the safety_settings attribute of the model. For example, to turn off safety blocking for dangerous content, you can import enums from the @google/generative-ai package, then construct your LLM as follows:
Copy
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";import { HarmBlockThreshold, HarmCategory } from "@google/generative-ai";const llmWithSafetySettings = new ChatGoogleGenerativeAI({ model: "gemini-1.5-pro", temperature: 0, safetySettings: [ { category: HarmCategory.HARM_CATEGORY_HARASSMENT, threshold: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, }, ], // other params...});
Tool calling with Google AI is mostly the same as tool calling with other models, but has a few restrictions on schema.The Google AI API does not allow tool schemas to contain an object with unknown properties. For example, the following Zod schemas will throw an error:const invalidSchema = z.object({ properties: z.record(z.unknown()) });andconst invalidSchema2 = z.record(z.unknown());Instead, you should explicitly define the properties of the object field. Here’s an example:
Copy
import { tool } from "@langchain/core/tools";import { ChatGoogleGenerativeAI } from "@langchain/google-genai";import * as z from "zod";// Define your toolconst fakeBrowserTool = tool((_) => { return "The search result is xyz..."}, { name: "browser_tool", description: "Useful for when you need to find something on the web or summarize a webpage.", schema: z.object({ url: z.string().describe("The URL of the webpage to search."), query: z.string().optional().describe("An optional search query to use."), }),})const llmWithTool = new ChatGoogleGenerativeAI({ model: "gemini-pro",}).bindTools([fakeBrowserTool]) // Bind your tools to the modelconst toolRes = await llmWithTool.invoke([ [ "human", "Search the web and tell me what the weather will be like tonight in new york. use a popular weather website", ],]);console.log(toolRes.tool_calls);
Copy
[ { name: 'browser_tool', args: { url: 'https://www.weather.com', query: 'weather tonight in new york' }, type: 'tool_call' }]
Google also offers a built in search tool which you can use to ground content generation in real-world information. Here’s an example of how to use it:
Copy
import { DynamicRetrievalMode, GoogleSearchRetrievalTool } from "@google/generative-ai";import { ChatGoogleGenerativeAI } from "@langchain/google-genai";const searchRetrievalTool: GoogleSearchRetrievalTool = { googleSearchRetrieval: { dynamicRetrievalConfig: { mode: DynamicRetrievalMode.MODE_DYNAMIC, dynamicThreshold: 0.7, // default is 0.7 } }};const searchRetrievalModel = new ChatGoogleGenerativeAI({ model: "gemini-1.5-pro", temperature: 0, maxRetries: 0,}).bindTools([searchRetrievalTool]);const searchRetrievalResult = await searchRetrievalModel.invoke("Who won the 2024 MLB World Series?");console.log(searchRetrievalResult.content);
Copy
The Los Angeles Dodgers won the 2024 World Series, defeating the New York Yankees in Game 5 on October 30, 2024, by a score of 7-6. This victory marks the Dodgers' eighth World Series title and their first in a full season since 1988. They achieved this win by overcoming a 5-0 deficit, making them the first team in World Series history to win a clinching game after being behind by such a margin. The Dodgers also became the first team in MLB postseason history to overcome a five-run deficit, fall behind again, and still win. Walker Buehler earned the save in the final game, securing the championship for the Dodgers.
The response also includes metadata about the search result:
Google Generative AI also supports code execution. Using the built in CodeExecutionTool, you can make the model generate code, execute it, and use the results in a final completion:
Copy
import { CodeExecutionTool } from "@google/generative-ai";import { ChatGoogleGenerativeAI } from "@langchain/google-genai";const codeExecutionTool: CodeExecutionTool = { codeExecution: {}, // Simply pass an empty object to enable it.};const codeExecutionModel = new ChatGoogleGenerativeAI({ model: "gemini-1.5-pro", temperature: 0, maxRetries: 0,}).bindTools([codeExecutionTool]);const codeExecutionResult = await codeExecutionModel.invoke("Use code execution to find the sum of the first and last 3 numbers in the following list: [1, 2, 3, 72638, 8, 727, 4, 5, 6]");console.dir(codeExecutionResult.content, { depth: null });
Copy
[ { type: 'text', text: "Here's how to find the sum of the first and last three numbers in the given list using Python:\n" + '\n' }, { type: 'executableCode', executableCode: { language: 'PYTHON', code: '\n' + 'my_list = [1, 2, 3, 72638, 8, 727, 4, 5, 6]\n' + '\n' + 'first_three_sum = sum(my_list[:3])\n' + 'last_three_sum = sum(my_list[-3:])\n' + 'total_sum = first_three_sum + last_three_sum\n' + '\n' + 'print(f"{first_three_sum=}")\n' + 'print(f"{last_three_sum=}")\n' + 'print(f"{total_sum=}")\n' + '\n' } }, { type: 'codeExecutionResult', codeExecutionResult: { outcome: 'OUTCOME_OK', output: 'first_three_sum=6\nlast_three_sum=15\ntotal_sum=21\n' } }, { type: 'text', text: 'Therefore, the sum of the first three numbers (1, 2, 3) is 6, the sum of the last three numbers (4, 5, 6) is 15, and their total sum is 21.\n' }]
You can also pass this generation back to the model as chat history:
Copy
const codeExecutionExplanation = await codeExecutionModel.invoke([ codeExecutionResult, { role: "user", content: "Please explain the question I asked, the code you wrote, and the answer you got.", }])console.log(codeExecutionExplanation.content);
Copy
You asked for the sum of the first three and the last three numbers in the list `[1, 2, 3, 72638, 8, 727, 4, 5, 6]`.Here's a breakdown of the code:1. **`my_list = [1, 2, 3, 72638, 8, 727, 4, 5, 6]`**: This line defines the list of numbers you provided.2. **`first_three_sum = sum(my_list[:3])`**: This calculates the sum of the first three numbers. `my_list[:3]` is a slice of the list that takes elements from the beginning up to (but not including) the index 3. So, it takes elements at indices 0, 1, and 2, which are 1, 2, and 3. The `sum()` function then adds these numbers together.3. **`last_three_sum = sum(my_list[-3:])`**: This calculates the sum of the last three numbers. `my_list[-3:]` is a slice that takes elements starting from the third element from the end and goes to the end of the list. So it takes elements at indices -3, -2, and -1 which correspond to 4, 5, and 6. The `sum()` function adds these numbers.4. **`total_sum = first_three_sum + last_three_sum`**: This adds the sum of the first three numbers and the sum of the last three numbers to get the final result.5. **`print(f"{first_three_sum=}")`**, **`print(f"{last_three_sum=}")`**, and **`print(f"{total_sum=}")`**: These lines print the calculated sums in a clear and readable format.The output of the code was:* `first_three_sum=6`* `last_three_sum=15`* `total_sum=21`Therefore, the answer to your question is 21.
Context caching allows you to pass some content to the model once, cache the input tokens, and then refer to the cached tokens for subsequent requests to reduce cost. You can create a CachedContent object using GoogleAICacheManager class and then pass the CachedContent object to your ChatGoogleGenerativeAIModel with enableCachedContent() method.
Copy
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";import { GoogleAICacheManager, GoogleAIFileManager,} from "@google/generative-ai/server";const fileManager = new GoogleAIFileManager(process.env.GOOGLE_API_KEY);const cacheManager = new GoogleAICacheManager(process.env.GOOGLE_API_KEY);// uploads file for cachingconst pathToVideoFile = "/path/to/video/file";const displayName = "example-video";const fileResult = await fileManager.uploadFile(pathToVideoFile, { displayName, mimeType: "video/mp4",});// creates cached content AFTER uploading is finishedconst cachedContent = await cacheManager.create({ model: "models/gemini-1.5-flash-001", displayName: displayName, systemInstruction: "You are an expert video analyzer, and your job is to answer " + "the user's query based on the video file you have access to.", contents: [ { role: "user", parts: [ { fileData: { mimeType: fileResult.file.mimeType, fileUri: fileResult.file.uri, }, }, ], }, ], ttlSeconds: 300,});// passes cached video to modelconst model = new ChatGoogleGenerativeAI({});model.useCachedContent(cachedContent);// invokes model with cached videoawait model.invoke("Summarize the video");
Note
Context caching supports both Gemini 1.5 Pro and Gemini 1.5 Flash. Context caching is only available for stable models with fixed versions (for example, gemini-1.5-pro-001). You must include the version postfix (for example, the -001 in gemini-1.5-pro-001).
The minimum input token count for context caching is 32,768, and the maximum is the same as the maximum for the given model.
As of the time this doc was written (2023/12/12), Gemini has some restrictions on the types and structure of prompts it accepts. Specifically:
When providing multimodal (image) inputs, you are restricted to at most 1 message of “human” (user) type. You cannot pass multiple messages (though the single human message may have multiple content entries)
System messages are not natively supported, and will be merged with the first human message if present.
For regular chat conversations, messages must follow the human/ai/human/ai alternating pattern. You may not provide 2 AI or human messages in sequence.
Message may be blocked if they violate the safety checks of the LLM. In this case, the model will return an empty response.