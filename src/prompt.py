#!/usr/bin/env python3
"""RAG prompt templates with inline citations."""

from typing import List, Dict, Any
import re


class RAGPrompt:
    """Build RAG prompts with citations."""

    SYSTEM_PROMPT = """You are an internal technical assistant for Clockify Help and LangChain documentation.
Your role: answer only from provided context. Be accurate and concise.
Citations: use inline bracketed format [1], [2] tied to Sources section.
If info is missing: say so and suggest related topics.
Format: answer first, then numbered Sources."""

    @staticmethod
    def build_context_block(chunks: List[Dict[str, Any]]) -> tuple[str, List[Dict]]:
        """Format chunks as numbered context blocks."""
        sources = []
        context_lines = []

        for idx, chunk in enumerate(chunks, 1):
            url = chunk.get("url", "")
            title = chunk.get("title", "Untitled")
            namespace = chunk.get("namespace", "")
            text = chunk.get("text", "")[:300]  # First 300 chars

            source = {
                "number": idx,
                "title": title,
                "url": url,
                "namespace": namespace,
            }
            sources.append(source)

            context_lines.append(f"[{idx}] {title} ({namespace})\nURL: {url}\n\n{text}...\n")

        context = "\n".join(context_lines)
        return context, sources

    @staticmethod
    def build_user_prompt(question: str, context: str) -> str:
        """Build final user prompt."""
        return f"""Based on the following context, answer the user's question.
Use inline citations [1], [2] when relevant.

CONTEXT:
{context}

QUESTION: {question}

Please provide a clear, accurate answer with inline citations."""

    @staticmethod
    def build_messages(question: str, chunks: List[Dict[str, Any]]) -> tuple[List[Dict[str, str]], List[Dict]]:
        """Build messages for LLM + track sources."""
        context, sources = RAGPrompt.build_context_block(chunks)
        user_msg = RAGPrompt.build_user_prompt(question, context)

        messages = [
            {"role": "system", "content": RAGPrompt.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]

        return messages, sources

    @staticmethod
    def format_response(answer: str, sources: List[Dict], use_citations: bool = True) -> Dict[str, Any]:
        """Format final response with sources."""
        response_text = answer

        if use_citations:
            # Add Sources section
            sources_section = "\n\n## Sources\n\n"
            for src in sources:
                sources_section += f"[{src['number']}] **{src['title']}** ({src['namespace']})\n"
                sources_section += f"    URL: {src['url']}\n\n"

            response_text += sources_section

        return {
            "answer": response_text,
            "sources": sources,
            "sources_count": len(sources),
        }
