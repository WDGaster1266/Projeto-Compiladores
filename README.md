[README.md](https://github.com/user-attachments/files/25051406/README.md)
# Projeto Compilador C

## 📖 Descrição
Este projeto implementa um **compilador simples** para uma linguagem estilo C.  
Ele realiza as etapas clássicas de compilação:

- **Análise léxica** → converte o código em tokens.  
- **Análise sintática** → constrói a árvore sintática abstrata (AST).  
- **Análise semântica** → valida declarações e tipos.  
- **Geração de código intermediário (TAC)** → produz código de três endereços.  
- **Execução de testes** → valida o funcionamento do lexer e da análise.  

---

## 📂 Estrutura do Projeto

```text
Projeto Compilador C/
└── textorodavel/
    ├── ast_printer.py
    ├── lexer.py
    ├── main.py
    ├── parser.py
    ├── program.py
    ├── semantic.py
    ├── tac_generator.py
    ├── test_lexer.py
    └── __pycache__/   # arquivos gerados automaticamente pelo Python (ignorar)
