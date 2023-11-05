from string import Formatter

class ExtendedFormatter(Formatter):
    """An extended format string formatter

    Formatter with extended conversion symbol
    """
    def convert_field(self, value, conversion):
        """ Extend conversion symbol
        Following additional symbol has been added
        * l: convert to string and low case
        * u: convert to string and up case
        * t: convert to title

        default are:
        * s: convert with str()
        * r: convert with repr()
        * a: convert with ascii()
        """
        
        match conversion:
            case 'u':
                return str(value).upper()
            case 'l':
                return str(value).lower()
            case 't':
                return str(value).title()
            case _:
                return super(ExtendedFormatter, self).convert_field(value, conversion)


FORMATTER = ExtendedFormatter()