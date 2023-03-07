from googletrans import Translator
from httpcore._exceptions import ConnectError

translator = Translator()


def capitalize_text(text):
    text_arr = list(text)
    for index in range(len(text_arr)):
        if text_arr[index] in ['.', ';', '?', '!']:
            for next_index in range(index, len(text_arr)):
                if text_arr[next_index] not in ['.', ';', '?', '!', ' ', '\n', '\r']:
                    text_arr[next_index] = str(text_arr[next_index]).upper()
                    break
    return f''.join(text_arr)


def translate_text(obj, fr, to,  field_name, capitalize):
    try:
        text = str(translator.translate(getattr(obj, f'{field_name}'), src=f'{fr}', dest=f'{to}').text).capitalize()
        if capitalize:
            text = capitalize_text(text)
        return text
        #  return getattr(obj, f'{field_name}')
    except ConnectError:
        return getattr(obj, f'{field_name}')
    except ValueError:
        return getattr(obj, f'{field_name}')
