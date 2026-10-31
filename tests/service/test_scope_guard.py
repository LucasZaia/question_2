from agent_app.service.scope_guard import is_in_scope


def test_scope_guard_allows_linux_programming_and_infrastructure_topics() -> None:
    assert is_in_scope("Como uso chmod no Linux?")
    assert is_in_scope("Mostre um exemplo de uma função Python.")
    assert is_in_scope("Como faço deploy com Docker?")


def test_scope_guard_rejects_unrelated_topics() -> None:
    assert not is_in_scope("Qual é a previsão do tempo para amanhã?")
    assert not is_in_scope("Me conte uma receita de bolo.")

