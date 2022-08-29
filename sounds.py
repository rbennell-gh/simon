import pygame as pg
from array import array

class Tone(pg.mixer.Sound):
    """This generates a 'Square wave' with a generator.

    Then creates an array of samples, and passes that into pygame.Sound.
    """

    def __init__(self, frequency, array_type, volume=.1):
        self.frequency = frequency
        if array_type == 'b':
            # we have to convert the 1 byte 'b' samples to 2 byte 'h'.
            samples = self.signed_char_to_signed_short(
                self.make_samples_b()
            )
        elif array_type == 'h':
            samples = self.make_samples_h()
        else:
            raise ValueError('array_type not supported')

        pg.mixer.Sound.__init__(self, buffer=samples)
        self.set_volume(volume)

    def make_samples_b(self):
        """ Builds samples array between -127 and 127.
            Array type 'h'.
        """
        mixer_frequency = pg.mixer.get_init()[0]
        mixer_format = pg.mixer.get_init()[1]
        period = int(round(mixer_frequency / self.frequency))
        max_amplitude = 2 ** (abs(mixer_format) - 1) - 1
        max_amplitude = int(max_amplitude / 256)
        # print(f'mixer_frequency:{mixer_frequency}, mixer_format:{mixer_format}')
        # print(f'period:{period}, max_amplitude:{max_amplitude}')

        # 'b' array is signed char, 1 byte
        # https://docs.python.org/3/library/array.html
        samples = array('b',
            (max_amplitude if time < period / 2 else -max_amplitude
                for time in range(period))
        )
        return samples

    def signed_char_to_signed_short(self, b_samples):
        """ Converts 1 byte signed char samples to 2 byte signed short.

            127 -> 32767
        """
        # just a simple linear conversion.
        factor = int(32767 / 127)
        return array('h', (sample * factor for sample in b_samples))

    def make_samples_h(self):
        """ Builds samples array between -32767 snd 32767.
            Array type 'h'.
        """
        mixer_frequency = pg.mixer.get_init()[0]
        mixer_format = pg.mixer.get_init()[1]
        period = int(round(mixer_frequency / self.frequency))
        max_amplitude = 2 ** (abs(mixer_format) - 1) - 1
        # print(f'mixer_frequency:{mixer_frequency}, mixer_format:{mixer_format}')
        # print(f'period:{period}, max_amplitude:{max_amplitude}')

        # 'h' array is signed short, 2 bytes
        # https://docs.python.org/3/library/array.html
        samples = array('h',
            (max_amplitude if time < period / 2 else -max_amplitude
                for time in range(period))
        )
        return samples