# Projeto BDD - Arquitetura Limpa (Robótica)

Esta é a versão refatorada utilizando Clean Architecture, Padrão Strategy/Adapter e Princípios SOLID.
Pronto para suportar PyBullet, CoppeliaSim e diferentes braços robóticos (Niryo, Kinova).

## Como rodar:
1. Extraia o ZIP e abra a pasta no VS Code.
2. Crie e ative um ambiente virtual (opcional, mas recomendado).
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute o PyBullet por padrão: `behave`
5. Teste a arquitetura chamando o CoppeliaSim (Mock):
   - PowerShell: `$env:SIMULATOR="coppeliasim"; behave`
   - Linux/Mac: `SIMULATOR=coppeliasim behave`
