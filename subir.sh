VERSAO="0.0.2"
DATA_HORA=$(date +"%d-%m-%Y - %H:%M")
MENSAGEM_COMMIT="Versao: $VERSAO - $DATA_HORA"

git add .
git commit -m "$MENSAGEM_COMMIT"
git push origin main
