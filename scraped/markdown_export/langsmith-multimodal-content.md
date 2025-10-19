# langsmith-multimodal-content

> Source: https://docs.langchain.com/langsmith/multimodal-content

- Inline content: Embed static files (images, PDFs, audio) directly in your prompt. This is ideal when you want to consistently include the same multimodal content across all uses of the prompt. For example, you might include a reference image that helps ground the model’s responses.
-
Template variables: Create dynamic placeholders for attachments that can be populated with different content each time. This approach offers more flexibility, allowing you to:
- Test how the model handles different inputs
- Create reusable prompts that work with varying content
Not all models support multimodal content. Before using multimodal features in the playground, make sure your selected model supports the file types you want to use.
Inline content
Click the file icon in the message where you want to add multimodal content. Under theUpload content
tab, you can upload a file and include it inline in the prompt.
Template variables
Click the file icon in the message where you want to add multimodal content. Under theTemplate variables
tab, you can create a template variable for a specific attachment type. Currently, only images, PDFs, and audio files (.wav, .mp3) are supported.
Populate the template variable
Once you’ve added a template variable, you can provide content for it using the panel on the right side of the screen. Simply click the+
button to upload or select content that will be used to populate the template variable.