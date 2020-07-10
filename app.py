"""
Testing 
"""

from programs import ComputerController, Computer, Program


if __name__ == "__main__":

    computer = Computer()

    computer.add_program(ComputerController(keyword='computer.umdl'))
    #computer.add_program(Program(keyword='computer_music.pmdl',callback=lambda x: print("MUSIC")))
    # computer.add_program(Program(keyword='computer_email.pmdl',callback=lambda x: print("EMAIL")))
    # computer.add_program(Program(keyword='youtube.pmdl',callback=lambda x: print("YT")))
    computer.add_program(
        Program('hey_fucker.pmdl', lambda x: print("Eres un deus")))
    computer.start_programs()
