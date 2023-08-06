from __future__ import print_function
import json
import os
import random
import re


__all__ = ['generate_random_string', 'bofh_excuse']


token_regex = re.compile('{(\w+)}')


def generate_random_string(template_dict, key='start'):
    """Generates a random excuse from a simple template dict.

    Based off of drow's generator.js (public domain).
    Grok it here: http://donjon.bin.sh/code/random/generator.js

    Args:
        template_dict: Dict with template strings.
        key: String with the starting index for the dict. (Default: 'start')

    Returns:
        Generated string.
    """

    data = template_dict.get(key)

    #if isinstance(data, list):
    result = random.choice(data)
    #else:
        #result = random.choice(data.values())

    for match in token_regex.findall(result):
        word = generate_random_string(template_dict, match) or match
        result = result.replace('{{{0}}}'.format(match), word)

    return result


def bofh_excuse(how_many=1):
    """Generate random BOFH themed technical excuses!

    Args:
        how_many: Number of excuses to generate. (Default: 1)

    Returns:
        A list of BOFH excuses.
    """

    excuse_path = os.path.join(os.path.dirname(__file__), 'bofh_excuses.json')
    with open(excuse_path, 'r') as _f:
        excuse_dict = json.load(_f)

    return [generate_random_string(excuse_dict) for _ in range(int(how_many))]


def main():
    for excuse in bofh_excuse():
        print(excuse)


if __name__ == '__main__':
    main()
