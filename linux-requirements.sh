echo
echo "Oi, aqui fala o professor Alexandre pelo Linux"
echo "Nao se sinta sozinho(a), eu estou no computador com voce"
echo
echo
echo
echo "vou CRIAR o ambiente virtual na pasta de nivel anterior"
python3 -m venv ../venv &&
echo "PRONTO!"
echo
echo
echo
echo "agora vou ATIVAR o ambiente virtual"
source ../venv/bin/activate &&
echo "PRONTO!"
echo
echo
echo
echo "finalmente, eu vou INSTALAR a biblioteca pdf2image"
echo
pip3 install pdf2image &&
echo
echo "PRONTO!"
echo
echo
echo
echo "vou dar um git config --list para vc conferir seu user.email, user.name, se está no seu repositório mesmo e o credential.helper"
echo
git config --list
echo
echo
echo
echo "==> CONFIRA <== se está tudo certo no seu user.email, user.name, remote.origin.url e o credential.helper"
echo "se estiver tudo certo, pode codar. Boa sorte!"
echo
echo
echo
