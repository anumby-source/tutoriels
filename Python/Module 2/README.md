# Module 2: Comprendre ce qu’est une boucle événementielle et une coroutine.

- Savoir créer et lancer plusieurs tâches concurrentes.
- Manipuler ```uasyncio.sleep()``` pour éviter de bloquer le programme.
- Appliquer l’asynchrone à des cas concrets : LED, bouton, capteur.

Documentation générale micropython https://docs.micropython.org/en/latest/library/asyncio.html

Documentation générale python https://docs.python.org/3/library/asyncio-task.html

## Pourquoi l’asynchrone sur ESP32 ?
L’ESP32 doit souvent :
- clignoter une LED,
- lire un capteur,
- gérer un bouton,
- servir une page web,
- communiquer en WiFi…

En fonctionnement **synchrone**, chaque tâche attend la précédente → 
le microcontrôleur devient lent ou non réactif.
En fonctionnement **asynchrone**, les tâches sont non bloquantes : 
elles avancent chacune à leur rythme tout en partageant le CPU.
l’asynchrone permet d’exécuter plusieurs tâches sans bloquer le programme .

## Le module uasyncio
MicroPython fournit une version légère d’asyncio :

```
import uasyncio as asyncio
```

Concepts clés :

- **coroutine** : fonction déclarée avec ```async def```
- **task** : coroutine lancée en parallèle
- **await** : pause non bloquante
- **event loop** : moteur qui exécute les tâches


- la tâche principale ```main``` est lancée par la fonction ```asyncio.run(main())``` et l'on attend qu'elle se termine
- les tâches sont lancées par une tâche **parente** par la fonction ```t = asyncio.create_task(f())``` sans attendre qu'elles se terminent
- lorsque la tâche parente s'arrête, toutes les tâche *filles* s'arrêtent
- on peut contrôler la durée d'une tâche par la fonction ```await asyncio.sleep(secondes)```
- on peut attendre qu'une tâche déjà lancée se temine par la fonction ```await t```
- on peut forcer l'arrêt d'une tâche déjà lancée par la fonction ```t.cancel()```

## Exemple 1 — Combiner pluseurs boucles de façon non bloquante

```
import uasyncio as asyncio

async def blink():
    # Ici on affiche alternativement 0 ou 1 toutes les demi-secondes
    while True:
        print("0")
        await asyncio.sleep(0.5)
        print("1")
        await asyncio.sleep(0.5)

async def main():
    # on lance la première boucle, tout en lançant une autre boucle plus rapide
    # puis on arrête l'application au bout de 5 secondes

    asyncio.create_task(blink())
    for i in range(10):
        print("aaa")
        await asyncio.sleep(0.1)

    await asyncio.sleep(5)   # laisse tourner 5s

asyncio.run(main())
```


## Exemple 2 — Clignoter une LED sans bloquer
```
import uasyncio as asyncio
from machine import Pin

led = Pin(2, Pin.OUT)

async def blink():
    # On allume et éteint la LED indéfiniment
    while True:
        led.value(1)
        await asyncio.sleep(0.5)
        led.value(0)
        await asyncio.sleep(0.5)

async def main():
    # On lance la tâche de clignottement qui peut continuer
    # sans gêner le reste du programme
    asyncio.create_task(blink())
    for i in range(10):
        print("aaa")
        await asyncio.sleep(0.1)
    await asyncio.sleep(10)   # laisse tourner 10s

asyncio.run(main())
```

- **await asyncio.sleep()** ne bloque pas le CPU.
- Pendant ce temps, d’autres tâches peuvent tourner.

## Exemple 3 — LED + lecture bouton en parallèle

![img.png](img.png)![img_1.png](img_1.png)


```
import uasyncio as asyncio
from machine import Pin

led = Pin(2, Pin.OUT)
button = Pin(0, Pin.IN, Pin.PULL_UP)

async def blink():
    while True:
        led.value(not led.value())
        await asyncio.sleep(0.3)

async def watch_button():
    while True:
        if button.value() == 0:
            print("Bouton pressé !")
        await asyncio.sleep(0.05)

async def main():
    asyncio.create_task(blink())
    asyncio.create_task(watch_button())
    await asyncio.sleep(60)

asyncio.run(main())
```
- Plusieurs tâches tournent réellement en parallèle (coopératif).
- Le bouton est lu sans bloquer le clignotement.

## Exemple 4 — Lire un capteur périodiquement (ex. température)

![img_2.png](img_2.png)![img_3.png](img_3.png)

```
import uasyncio as asyncio
from machine import ADC, Pin

adc = ADC(Pin(34))

async def read_sensor():
    while True:
        value = adc.read()
        print("Valeur :", value)
        await asyncio.sleep(1)

async def main():
    asyncio.create_task(read_sensor())
    await asyncio.sleep(30)

asyncio.run(main())
```

- Une tâche peut tourner à intervalle régulier.
- Le programme reste réactif.

## Exemple 5 — Serveur Web + LED (cas réel IoT)
Cet exemple illustre un cas typique décrit dans les tutoriels MicroPython : gérer un serveur web tout en restant réactif aux entrées/sorties .

```
import uasyncio as asyncio
from machine import Pin

led = Pin(2, Pin.OUT)

async def web_server(reader, writer):
    request = await reader.read(1024)
    led.value(not led.value())
    response = "HTTP/1.0 200 OK\r\n\r\nLED toggled!"
    await writer.awrite(response)
    await writer.aclose()

async def main():
    server = await asyncio.start_server(web_server, "0.0.0.0", 80)
    print("Serveur lancé")
    await server.wait_closed()

asyncio.run(main())
```

## Exercices pour les élèves
### Niveau 1
- Modifier la fréquence de clignotement.
- Ajouter une deuxième LED avec une fréquence différente.

### Niveau 2
- Faire un compteur qui s’incrémente toutes les secondes.
- Afficher le compteur sans bloquer le clignotement.

### Niveau 3
- Lire un capteur et envoyer les données via un serveur web.
- Ajouter un bouton qui active/désactive la lecture du capteur.

