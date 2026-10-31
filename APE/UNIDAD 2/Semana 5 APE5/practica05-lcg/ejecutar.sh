#!/bin/bash
# Compila y ejecuta Java y después Python (Python compara con lo que generó Java).
# Se corre desde cualquier carpeta: ./ejecutar.sh
# Para medir también el período completo en Java: ./ejecutar.sh periodo
cd "$(dirname "$0")"
mkdir -p java/build resultados graficas
javac -encoding UTF-8 -d java/build $(find java/src -name "*.java") \
  && java -Dstdout.encoding=UTF-8 -cp java/build Main "$@" \
  && python3 python/main.py
