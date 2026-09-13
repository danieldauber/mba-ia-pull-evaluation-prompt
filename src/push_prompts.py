"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()

def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    try:
        system_prompt = prompt_data["system_prompt"]
        user_template = prompt_data.get('user_prompt_template', '{bug_report}')

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_template)
        ])

        hub.push(
            prompt_name,
            prompt
        )

        print(f"Prompt '{prompt_name}' publicado com sucesso!")
        return True

    except Exception as e:
        print(f"Erro ao publicar prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    return validate_prompt_structure(prompt_data)


def main():
    prompt_name = "bug_to_user_story_v2"
    print_section_header("PUSH DE PROMPT PARA LANGSMITH")

    required_envs = [
        "LANGSMITH_API_KEY",
        "LANGSMITH_PROJECT"
    ]

    if not check_env_vars(required_envs):
        return 1

    prompt_path = "prompts/bug_to_user_story_v2.yml"
    data = load_yaml(prompt_path)
    prompt_data = data["bug_to_user_story_v2"]

    if not prompt_data:
        return 1

    is_valid, errors = validate_prompt(prompt_data)

    if not is_valid:
        print("Prompt inválido:")
        for err in errors:
            print(f"  - {err}")
        return 1

    prompt_name = f"bug_to_user_story_v{prompt_data['version']}"

    success = push_prompt_to_langsmith(prompt_name, prompt_data)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
    