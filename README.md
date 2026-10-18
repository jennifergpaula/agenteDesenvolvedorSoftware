# Agente Desenvolvedor de Software

Exemplo de validação de transações para pipelines de automação e dados, com um
limite determinístico de processamento automatizado e encaminhamento para
aprovação humana quando esse limite é excedido.

## Requisitos

- Python 3.11 ou superior

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Uso

O módulo [`transaction.py`](transaction.py) fornece `TransactionRecord`,
`process_transaction` e `HumanApprovalRequiredError`.

```python
from transaction import process_transaction

record = process_transaction(
    {
        "transaction_id": "tx_001",
        "amount": 1500.50,
        "risk_score": 0.1,
    }
)
```

Transações com valor até `10.000,00`, inclusive, são aceitas pela automação.
Valores acima desse teto levantam `HumanApprovalRequiredError`. Dados que não
atendem ao modelo levantam `pydantic.ValidationError`.

## Testes

Execute a suíte com:

```bash
pytest -q
```

Os testes cobrem uma transação normal, o teto exato, a exigência de aprovação
humana acima do teto e um valor inválido.

## Prompt do agente

O prompt utilizado como especificação deste exemplo está em
[`PROMPT.md`](PROMPT.md).
