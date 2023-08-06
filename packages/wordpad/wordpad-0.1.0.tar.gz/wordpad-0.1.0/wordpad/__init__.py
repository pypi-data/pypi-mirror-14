
def pad(value, width, char='0', direction='left'):

    value = str(value)

    while len(value) < width:
        if direction == 'left':
            value = '{0}{1}'.format(char, value)
        else:
            value = '{1}{0}'.format(char, value)

    return value
