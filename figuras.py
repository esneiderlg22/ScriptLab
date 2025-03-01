import cowsay
import pyfiglet

characters = ['beavis', 'cheese', 'cow', 'daemon', 'dragon', 'fox', 'ghostbusters', 
              'kitty', 'meow', 'miki', 'milk', 'octopus', 'pig', 'stegosaurus', 
              'stimpy', 'trex', 'turkey', 'turtle', 'tux']

for character in characters:
    print(f"\n{character.upper()}:\n")
    try:
        print(getattr(cowsay, character)("¡Hola desde Python!"))
    except AttributeError:
        print(f"{character} no está disponible en tu versión de cowsay.")

ascii_text = pyfiglet.figlet_format("successful")
print(ascii_text)