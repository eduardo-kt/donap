# Caso de Uso 1: Realizar Doação (R01)

## Cenário Principal de Sucesso (CPS)
1. O Agente autentica o uso do sistema.
2. O Agente escolhe consultar donatário.
3. O sistema verifica se o donatário está cadastrado.
4. O sistema retorna as doações que se enquadram no perfil do donatário.
5. O Agente seleciona donativos.
6. O Agente autentica a doação.
7. O sistema atualiza a base de dados dos donativos disponíveis.
8. O sistema atualiza o cadastro do donatário.

## Extensões
- **Passo 3:** O sistema verifica se o donatário está cadastrado.
  - 3.1 Se o donatário não estiver cadastrado, sistema transfere para cadastro.
  - 3.2 Agente cadastra donatário (R02).
  - 3.3 Ao finalizar o cadastro, retoma o CPS no passo 4.

# Caso de Uso 2: Cadastrar Donativo (R03)

## Cenário Principal de Sucesso (CPS)

1. O Agente autentica o uso do sistema.  
2. O Agente escolhe cadastrar doação.  
3. O Agente cadastra a doação.  
4. O Agente autentica o registro.  
5. O sistema atualiza a base de dados dos donativos disponíveis.  

# Caso de Uso 3: Cadastrar Agente (R04)

## Cenário Principal de Sucesso (CPS)

1. O Agente_1 autentica o uso do sistema.  
2. O Agente_1 escolhe cadastrar Agente_2.  
3. O Agente_1 cadastra o Agente_2.  
4. O Agente_1 autentica o registro.  
5. O sistema atualiza a base de Agentes cadastrados.  
