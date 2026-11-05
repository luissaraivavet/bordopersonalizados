# Instalação local do Scrapling para o projeto Bordô, sem privilégios de administrador.
# Uso: powershell -ExecutionPolicy Bypass -File .\scripts\instalar_scrapling.ps1
# Opcional: -ComNavegador para baixar o navegador controlado pelo Scrapling.
param([switch]$ComNavegador)
$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$venv = Join-Path $root ".venv-scrapling"
$python = Join-Path $venv "Scripts\python.exe"
$requirements = Join-Path $PSScriptRoot "requirements-scrapling.txt"

if (-not (Test-Path $python)) {
    Write-Host "Criando ambiente isolado do Scrapling..." -ForegroundColor Cyan
    $launcher = Get-Command py -ErrorAction SilentlyContinue
    if ($launcher) {
        & py -3 -m venv $venv
    } else {
        $command = Get-Command python -ErrorAction SilentlyContinue
        if (-not $command) {
            throw "Python 3.10+ não encontrado. Instale o Python e execute este arquivo novamente."
        }
        & python -m venv $venv
    }
    if ($LASTEXITCODE -ne 0) { throw "Não foi possível criar o ambiente Python." }
}
if (-not (Test-Path $python)) { throw "Python do ambiente virtual não localizado." }

Write-Host "Instalando Scrapling com os recursos de leitura HTTP..." -ForegroundColor Cyan
& $python -m pip install --disable-pip-version-check -r $requirements
if ($LASTEXITCODE -ne 0) { throw "Falha ao baixar dependências. Confira a conexão com a internet." }

& $python -c 'from scrapling import Selector; from scrapling.fetchers import Fetcher; print("OK: Scrapling e Fetcher importados.")'
if ($LASTEXITCODE -ne 0) { throw "Scrapling instalado, mas uma importação falhou." }

if ($ComNavegador) {
    $executable = Join-Path $venv "Scripts\scrapling.exe"
    Write-Host "Instalando dependências de navegador..." -ForegroundColor Cyan
    & $executable install
    if ($LASTEXITCODE -ne 0) { throw "Falha na instalação opcional do navegador." }
}

Write-Host "Validando o importador offline com fixture, sem acessar o Mercado Livre..." -ForegroundColor Cyan
Push-Location $root
try {
    & $python -m unittest discover -s tests -p test_importar_afiliados.py -v
    if ($LASTEXITCODE -ne 0) { throw "Falha nos testes locais do importador." }
} finally {
    Pop-Location
}
Write-Host ""
Write-Host "Scrapling pronto no ambiente local: $venv" -ForegroundColor Green
Write-Host "Arquivo de links: content\afiliados-links.json"
Write-Host "Para analisar HTML autorizado: .\.venv-scrapling\Scripts\python.exe scripts\importar_afiliados.py --fixture caminho-do-arquivo.html"
Write-Host "O programa não publicou produtos e não capturou páginas do Mercado Livre."
