'''Check spelling and basic grammar.

Use gingerit, a wrapper around the gingersoftware.com API
See https://github.com/Azd325/gingerit

@pnry 28 Dec 2021
'''
from gingerit.gingerit import GingerIt


def write_checker(show_dict=False):
    Parser = GingerIt()
    text = input('Please enter text: ')
    try:
        print(text)
        results = Parser.parse(text.strip())
        if results:
            print_results(results, show_dict)
    except Exception as e:
        print(e)


def print_results(results, show_dict):
    n = 0

    edits = ''
    if not results:
        return
    for info in reversed(results['corrections']):
        if info:
            if info['text'] and info['correct']:
                n = n + 1
                # short dictionary
                if info['definition'] and show_dict:
                    edits += f"{n}. {info['text']} -> {info['correct']} : {info['definition']}\n"
                else:
                    edits += f"{n}. {info['text']} -> {info['correct']}\n"
    if n > 0:
        print('\nSuggested =>', results['result'], '\n')
        print('\nCorrections:', n, '\n')
        print(edits)
    else:
        print('No errors detected!')
    print(results)


if __name__ == '__main__':
    write_checker(False)
