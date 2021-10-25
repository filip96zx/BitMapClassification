# BitMapClassification

Rozwiązanie zadania z pliku zadanie.odt

algorytm 1
to implementacja algorytmu zachłannego opisanego w zadaniu.

algorytm 2
to moja zoptymalizowana wersja algorytmu który wybiera punkty do obliczenia długości z równania okręgu. Okrąg rozszerza się z każdą iteracją, algorytm po znalezeniu punktu do obliczenia odległości kończy pętle dla danego punktu ponieważ znaleziona odległość jest najmniejsza. Ponadto algorytm umożliwia przyspieszenie działania kosztem dokładności poprzez zwiększanie skoku promienia w każdej iteracji.

Polecam porównać wyniki oraz czas pracy dla obu algorytmów oraz różnych ustawień skoku promienia.

Intrukcja:
- stwórz bitmapy klasowe do których algorytm będzie porównywał bitmapę testową.
  - bitmapy muszą nazywać się class1.bpm, class2.bpm... itd. z kolejnymi numerami aby program je wczytał, wszystkie bitmapy włącznie z testową powinny być kwadratowe       oraz tego samego rozmiaru.
- stwórz bitmapte testową o nazwie test1.bpm lub narysuj ją po włączeniu programu.
- po stworzeniu bitmap należy uruchomić program, wybrać algorym i nacisnąć przycisk "test". Program wykonuje dużo iteracji zwłaszcza przy pierwszym algorytmie więc oczekiwanie na wynik może chwilę potrwać zwłaszcza przy większych bitmapach. 
