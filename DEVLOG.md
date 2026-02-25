# Izstrādes žurnāls

### 2026.02.24
* **Paveiktais**: Uzsākts darbs pie projekta struktūras. Izveidoti pirmie moduļi: `storage.py` datu saglabāšanai, `logic.py` aprēķiniem un `app.py` bāzes GUI izveidei. Izveidots `export.py` skelets.
* **Problēmas**: Parādījās pirmās kļūdas ar failu importēšanu un neidentificētas kļūdas (unidentified errors) `storage.py` failā.

### 2026.02.25
* **Paveiktais**: Veikta koda revīzija un pielāgošana projekta tehniskajām prasībām. 
* **Labojumi**: Izlabotas atkāpju (indentation) kļūdas visos moduļos. Pabeigta datu ielādes un saglabāšanas loģika caur JSON.
* **Vizuālie uzlabojumi**: Pielāgoti loga izmēri un elementu izvietojums, lai tie nepārklātos.

### 2026.02.26
* **Paveiktais**: Pabeigta CSV eksporta funkcija modulī `export.py`, izmantojot `utf-8-sig` kodējumu Excel saderībai.
* **Funkcionalitāte**: Ieviests mēneša filtrs un automātiska kopsummas pārrēķināšana.
* **GUI uzlabojumi**: Vizuāli pielabotas pogas un sakārtoti tabulas kolonnu platumi, lai dati (īpaši apraksti) būtu pilnībā nolasāmi.
* **Dokumentācija**: Sagatavots README.md, izveidota docs/ mape ar ekrānuzņēmumiem un plūsmas diagrammu.