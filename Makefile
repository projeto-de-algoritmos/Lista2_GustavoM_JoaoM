BIN=env/bin/
help:
	@echo "Makefile para a execução do projeto"
	@echo ""
	@echo "Antes de rodar o projeto é recomendado a utilização da virtualenv rodando o comando: "
	@echo "$ source env/bin/activate"
	@echo ""
	@echo "Comandos:"
	@echo "install      Instala os requisitos para a execução do jogo"
	@echo "run          Executa o jogo"
	@echo ""

install:
	pip3 install -r requirements.txt

run:
	python3 main.py