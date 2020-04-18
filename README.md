# Dokumentacja
## O aplikacji
Aplikacją w projekcie jest translator napisów. Aplikacja pozwala użytkownikowi dodać własny plik srt i przetłumaczyć je z dowolnego języka (w jednym pliku może być nawet kilka różnych języków - aplikacja je rozpozna) na inny dowolny język.
![](0.png)
Działanie aplikacji opiera się na wrzuceniu przez użytkownika pliku z napisami i określeniu języka docelowego. Po wybraniu przycisku "Translate" plik trafia na dysk w App Service. Tam jest otwierany i odczytywany linijka po linijce.
![](1.png)

Pliki srt posiadają numer grupy i zakres czasu podczas którego napisy będą wyświetlane na ekranie. Następnie dodawana jest linijka odstępu i algorytm zapętlający cały proces. Algorytm odczytuje za pomocą generatora plik linijka po linijce, jeśli trafi na tekst, wtedy zapisuje do momentu aż nie trafi na pustą linię. Jeśli w kolejnych liniach znajduje się tekst, wtedy są one łączone i wysyłane do tłumaczenia (jeśli w następnej nie ma tekstu, wtedy wysyła tylko tę jedną, do pojawienia się linii bez tekstu. Linijkę bez tekstu zapisuje do nowego pliku).
#### Przykład:
![](2.png)

Linijki 26 i 27 zapisują się bez zmieniania do nowego pliku. Linijki 28 i 29 zostają przetłumaczone i zapisane do nowego pliku.
Po przetłumaczeniu na dysku w App Service tworzy się nowy plik. Następnie napisy są wysyłane do konta magazynu i usuwane z dysku w App Service. W bazie danych pojawiają się nazwy plików i ich lokalizacje w Storage. Przy pobieraniu przez użytkownika, nazwa pliku jest wyszukiwana w Storage, plik jest ładowany do pamięci komputera i wysyłany do użytkownika.

## Koszty
Do wdrożenia aplikacji wykorzystano następujące usługi chmurowe Azure: 
* Azure App Service
* Azure Database for PostgreSQL
* Cognitive Service (TextTranslation)
* Storage Account

#### Plan i koszty usługi Azure App Service
Przy wybranym planie usługi App Service w lokalizacji West Europe, System operacyjny Linux, plan standardowy S1 z automatycznym skalowaniem - koszty prezentują się nastęująco (69.35  USD).
![](4.png)

#### Plan i koszty usługi Azure Database for PostreSQL
Najwięcej miesięcznych kosztów generuje baza danych (208.63 USD) przy planie Memory Optimized uwzględniającym skalowanie w razie potrzeby. Lokalizacja West Europe, plan miesięczny "Pay as you go".
![](5.png)

#### Plan i koszty usługi Cognitive Service (TextTranslation)
Usługa w wersji free uwzględnia miesięcznie do 2.000.000 przetłumaczonych wyrazów.

#### Plan i koszty usługi Storage Account
Konta magazynu generują szacowane miesięczne koszty w wysokości 20.80 USD na miesięcznym planie "Pay as you go" w lokalizacji East US.
![](6.png)

#### Szacowany miesięczne koszty wszystkich wykorzystanych usług
Oszacowany miesięczny koszt utrzymania postawionej aplikacji (w wybranym planie z możliwością skalowania) - wszystkich usług wraz z dodatkami do poszczególnych z nich - dobre miesięczne koszty na przykład za SSL wynosi 301.10 USD.
![](7.png)

