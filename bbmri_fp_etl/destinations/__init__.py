def transform_id(id_):
    transformation = {
        "/": "-",
        "_": "-",
        "(": "",
        ")": "",
        ' ': '-',
        '+': '',
        ':': '-'
    }
    return id_.translate(str.maketrans(transformation))