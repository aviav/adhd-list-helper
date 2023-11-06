from anki.template import TemplateRenderContext
from anki import hooks
import random


def count_correct_answers(
    text: str, field: str, filter: str, ctx: TemplateRenderContext
) -> str:
    if filter != "count_correct_answers":
        return text

    fields = dict(ctx.note().items())

    return str(len(extract_values_before_blank(fields)))

hooks.field_filter.append(count_correct_answers)


def count_correct_answers_string(
    text: str, field: str, filter: str, ctx: TemplateRenderContext
) -> str:
    if filter != "count_correct_answers_string":
        return text

    number_correct = count_correct_answers(text, field, 'count_correct_answers', ctx)

    return n2w(int(number_correct))

hooks.field_filter.append(count_correct_answers_string)


def shuffle_all(
    text: str, field: str, filter: str, ctx: TemplateRenderContext
) -> str:
    if filter != "shuffle_all":
        return text

    fields = dict(ctx.note().items())
    non_blank_values = extract_values_before_blank(fields)
    random.shuffle(non_blank_values)
    list = ("<ul>"
    f"{''.join(['<li>' + value + '</li>' for value in non_blank_values])}"
    "</ul>")

    return list

hooks.field_filter.append(shuffle_all)


def shuffle_all_except(
    text: str, field: str, filter: str, ctx: TemplateRenderContext
) -> str:
    if filter != "shuffle_all_except":
        return text

    fields = dict(ctx.note().items())
    fields.pop(field)
    non_blank_values = extract_values_before_blank(fields)
    random.shuffle(non_blank_values)
    list = ("<ul>"
    f"{''.join(['<li>' + value + '</li>' for value in non_blank_values])}"
    "</ul>")

    return list

hooks.field_filter.append(shuffle_all_except)


# Inspired by https://stackoverflow.com/a/19506803
num2words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', \
             6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', \
            11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', \
            15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', \
            19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', \
            50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', \
            90: 'Ninety', 0: 'Zero'}

def n2w(n):
    try:
        return num2words[n].lower()
    except KeyError:
        try:
            return num2words[n-n%10].lower() + num2words[n%10].lower()
        except KeyError:
            return 'Number out of range'


def extract_values_before_blank(data):
    extracted_values = []
    for i in range(1, 11):  # Assuming keys range from 1 to 10
        key = f'Correct Answer {i}'
        if key not in data.keys():
            continue
        if data.get(key) == '':
            break
        extracted_values.append(data[key])
    return extracted_values
