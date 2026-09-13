"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langchain.load import dumpd
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

REMOTE_PROMPT_NAME = "leonanluppi/bug_to_user_story_v1"
LOCAL_OUTPUT_PATH = "prompts/bug_to_user_story_v1.yml"

def _extract_prompts(prompt_template) -> dict:
    system_prompt = ""
    user_prompt = ""

    serialized = dumpd(prompt_template)
    messages = serialized["kwargs"]["messages"]

    for message in messages:
        msg_class = message["id"][-1]
        text = message["kwargs"]["prompt"]["kwargs"]["template"]

        if "System" in msg_class:
            system_prompt = text.strip()
        elif "Human" in msg_class:
            user_prompt = text.strip()

    return {"system_prompt": system_prompt, "user_prompt": user_prompt}


def pull_prompts_from_langsmith():

    """Faz pull dos prompts do LangSmith Prompt Hub e salva localmente."""
    print_section_header("Pulling prompts from LangSmith Prompt Hub")

    # Verifica se as variáveis de ambiente necessárias estão definidas
    check_env_vars(["LANGSMITH_API_KEY", "LANGSMITH_ENDPOINT"])

    # Conecta ao LangSmith e faz pull do prompt
    prompt = hub.pull(REMOTE_PROMPT_NAME)

    # Salva o prompt localmente em formato YAML
    extracted_prompts = _extract_prompts(prompt)
    save_yaml(extracted_prompts, LOCAL_OUTPUT_PATH)
    print(f"Prompt saved in: {LOCAL_OUTPUT_PATH}")


def main():
    """Função principal"""
    pull_prompts_from_langsmith()
    return 0


if __name__ == "__main__":
    sys.exit(main())
