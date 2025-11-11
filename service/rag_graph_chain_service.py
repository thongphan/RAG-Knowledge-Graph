from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableBranch, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Tuple, Optional


class RAGPipelineService:
    """Main orchestrator combining structured & unstructured retrievers with LLM, supports chat history."""

    def __init__(self, structured_retriever, unstructured_retriever, chat_model):
        self.structured = structured_retriever
        self.unstructured = unstructured_retriever
        self.chat = chat_model

        self.prompt = PromptTemplate.from_template("""
        Answer the question based only on the following context:
        {context}

        Question: {question}
        Answer concisely:
        """)

        # Prompt to condense follow-up question with chat history
        self.condense_prompt = PromptTemplate.from_template("""
        Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question,
        in its original language.
        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:
        """)

    @staticmethod
    def format_chat_history(chat_history: List[Tuple[str, str]]) -> List:
        """Convert tuples to HumanMessage/AIMessage list for LLM input."""
        buffer = []
        for human, ai in chat_history:
            buffer.append(HumanMessage(content=human))
            buffer.append(AIMessage(content=ai))
        return buffer

    def run(self, question: str, chat_history: Optional[List[Tuple[str, str]]] = None):
        """
        Run the RAG pipeline.
        :param question: The question to answer.
        :param chat_history: Optional previous conversation.
        """

        # Step 1: Condense question if chat history exists
        if chat_history:
            formatted_history = self.format_chat_history(chat_history)
            standalone_question = (
                RunnablePassthrough.assign(chat_history=lambda _: formatted_history)
                | self.condense_prompt
                | self.chat
                | StrOutputParser()
            ).invoke({"question": question})
        else:
            standalone_question = question

        # Step 2: Retrieve structured and unstructured context
        structured_context = self.structured.retrieve([standalone_question])
        unstructured_context = self.unstructured.retrieve(standalone_question)
        context = f"Structured: {structured_context}\nUnstructured: {' '.join(unstructured_context)}"

        # Step 3: Run final LLM chain
        chain = (
            RunnableParallel({"context": RunnablePassthrough(), "question": RunnablePassthrough()})
            | self.prompt
            | self.chat
            | StrOutputParser()
        )
        return chain.invoke({"context": context, "question": standalone_question})
