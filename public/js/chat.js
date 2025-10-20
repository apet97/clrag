/**
 * Chat Interface Controller
 */

const chatState = {
    conversationId: null,
    isLoading: false
};

document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('chatInput');
    const chatSendBtn = document.getElementById('chatSendBtn');

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    chatSendBtn.addEventListener('click', sendMessage);
});

async function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();

    if (!message || chatState.isLoading) return;

    chatState.isLoading = true;
    addChatMessage(message, 'user');
    chatInput.value = '';

    // Show loading indicator
    const loadingMsg = document.createElement('div');
    loadingMsg.className = 'message assistant';
    loadingMsg.innerHTML = `<div class="message-content"><div class="message-loading"><div class="spinner"></div> Thinking...</div></div>`;
    document.getElementById('chatMessages').appendChild(loadingMsg);

    try {
        const response = await api.chat(message);

        // Remove loading message
        loadingMsg.remove();

        // Add assistant response
        const answer = response.answer || 'No response generated';
        addChatMessage(answer, 'assistant');

        // Display sources if available
        if (response.sources && response.sources.length > 0) {
            displaySources(response.sources);
        }

        chatState.conversationId = response.conversation_id;
    } catch (error) {
        loadingMsg.remove();
        addChatMessage(`Error: ${error.message}`, 'assistant');
    } finally {
        chatState.isLoading = false;
        document.getElementById('chatInput').focus();
    }
}

function addChatMessage(text, sender) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${sender}`;

    const content = document.createElement('div');
    content.className = 'message-content';

    // Simple markdown-like formatting
    let formattedText = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');

    content.innerHTML = formattedText;
    messageEl.appendChild(content);

    document.getElementById('chatMessages').appendChild(messageEl);
    document.getElementById('chatMessages').scrollTop = document.getElementById('chatMessages').scrollHeight;
}

function displaySources(sources) {
    const sourcesPanel = document.getElementById('sourcesPanel');
    const sourcesList = document.getElementById('sourcesList');

    sourcesList.innerHTML = '';

    sources.forEach((source, index) => {
        const sourceItem = document.createElement('div');
        sourceItem.className = 'source-item';
        sourceItem.innerHTML = `
            <strong>[${source.id}] ${source.title}</strong>
            <div style="font-size: 0.75rem; color: var(--text-light);">
                ${source.namespace} • <a href="${source.url}" target="_blank" rel="noopener">View article</a>
            </div>
        `;
        sourcesList.appendChild(sourceItem);
    });

    sourcesPanel.style.display = 'block';
}
