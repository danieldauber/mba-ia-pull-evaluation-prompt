"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure


PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_prompt():
    """Retorna a definição do prompt otimizado."""
    prompts = load_prompts(PROMPT_PATH)
    return prompts["bug_to_user_story_v2"]


class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt = get_prompt()

        assert "system_prompt" in prompt
        assert prompt["system_prompt"].strip()

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = get_prompt()["system_prompt"]

        assert "Você é" in system_prompt
        assert "especialista" in system_prompt.lower()

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = get_prompt()["system_prompt"].lower()

        assert "user stor" in system_prompt
        assert "como um" in system_prompt

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = get_prompt()["system_prompt"]

        assert system_prompt.count("Bug Report:") >= 2
        assert system_prompt.count("Output:") >= 2

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt_text = yaml.safe_dump(get_prompt(), allow_unicode=True)

        assert "[TODO]" not in prompt_text

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = get_prompt().get("techniques_applied", [])

        assert isinstance(techniques, list)
        assert len(techniques) >= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])