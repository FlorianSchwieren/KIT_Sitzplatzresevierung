Erklärung zur JSON:
Vorname
"name" : "Max",

Emailadresse an die, die update Email geschickt wird
"mail" : "max@musterman.de",

login username von https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung
"username" : "ABCDE",

login password von https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung
"password" : "12345",

Wenn man auf der Website auf den jeweiligen Platz geht, sieht man in der url einmal die area und den room. area=area id=room.
Der erste Eintrag in der Liste wird am höchsten priorisiert. Unten ein Beispiel von den Plätzen Empore A2 139/140/141.
"seat" : [
    {
        "area" : 35, 
        "id" : 1280
    },
    {
        "area" : 35, 
        "id" : 1281
        },
    {
    "area" : 35, 
    "id" : 1282
    }
],

Wochentage beginnend mit Montag=0, ..., Sontag = 6. An den Tagen wird versucht zu buchen. Alle möglich. 
"day" : [0, 1, 2, 3, 4, 5, 6],

Zeitperioden beginnend mit vormittags=0, ..., nachts=3. Am besten nur 2 angeben.
"period" : [0, 1]