import helpers


def email_count(text, Module):
    Length = " [*] " + Module + \
        ": Gathered " + str(text) + " Email(s)!"
    print helpers.color(Length, status=True)