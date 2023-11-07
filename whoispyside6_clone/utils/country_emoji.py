import flag


def get_flag(country_code):
    return flag.flag(country_code)


if __name__ == '__main__':
    print(get_flag("KR"))
