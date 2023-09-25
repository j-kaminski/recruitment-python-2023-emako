#### Autor: Jakub Kamiński 

- `example_currency_rates.json` - lokalne źródło danych z kursami walut
- `database.json` - baza danych z zapisanymi kursami walut


## Konfiguracja środowiska i uruchomienie 

Instalacja zależności
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


Uruchomienie programu (ARG1 - dev, prod)
```bash
python -m task ARG1
```

Uruchomienie testów
```bash
./tests.sh
```

