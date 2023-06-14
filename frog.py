from OpenWeather import _download_url
import random
class Frog:
    def __init__(self):
        self.l = ['https://media.discordapp.net/attachments/883217364085260362/890035959037579284/pexels-photo-236600.png?width=710&height=473',
                    'https://cdn.discordapp.com/attachments/890037241471205397/890037253307510824/frog-butterfly-pond-mirroring-45863.png',
                    'https://cdn.discordapp.com/attachments/890037241471205397/890037287545626634/pexels-photo-6713437.png',
                    'https://cdn.discordapp.com/attachments/890037241471205397/890037317501341736/pexels-photo-4524669.png',
                    'https://cdn.discordapp.com/attachments/890037241471205397/890037370022400040/tree-frog-frog-red-eyed-amphibian-76957.png',
                    'https://cdn.discordapp.com/attachments/890037241471205397/890037409184645162/frog-macro-amphibian-green-70083.png',
                    'https://cdn.discordapp.com/attachments/890037241471205397/890037965504520202/pexels-photo-674318.png',
                    'https://images.pexels.com/photos/2092041/pexels-photo-2092041.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                    'https://images.pexels.com/photos/73798/frog-marbled-reed-frog-amphibian-animal-73798.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                    'https://images.pexels.com/photos/2170198/pexels-photo-2170198.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                    'https://images.pexels.com/photos/638689/pexels-photo-638689.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                    'https://images.pexels.com/photos/35669/hyla-meridionalis-the-frog-amphibians.jpg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                    'https://images.pexels.com/photos/1046494/pexels-photo-1046494.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                    'https://images.pexels.com/photos/1370740/pexels-photo-1370740.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                    'https://images.pexels.com/photos/1101196/pexels-photo-1101196.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
                    'https://images.pexels.com/photos/3180755/pexels-photo-3180755.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                    'https://images.pexels.com/photos/9408389/pexels-photo-9408389.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940,'
                    'https://images.pexels.com/photos/1136104/pexels-photo-1136104.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                    'https://images.pexels.com/photos/753250/pexels-photo-753250.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                    'https://images.pexels.com/potos/2631482/pexels-photo-2631482.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                  'https://images.pexels.com/photos/57400/tree-frog-anuran-frog-amphibians-57400.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500']

    def ree(self):
        return self.l[random.randint(0, len(self.l) - 1)]




if __name__ == '__main__':
    print(_download_url('https://www.pexels.com/photo/amphibians-animals-frogs-grass-236600/'))
