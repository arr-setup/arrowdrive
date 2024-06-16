def parse(data: str, keys: list, mode: int = 1) -> list | dict | list[dict]:
    if type(data) == bytes:
        data = data.decode()

    if mode == 1:
        return dict(zip(keys, data.split('\n')))
    elif mode == 2:
        return dict([ item.split('=', 1) for item in data.split('\n') ])
    elif mode == 3:
        if len(keys) == 0:
            return [ item.split('::') for item in data.split('\n') ]
        else:
            return [ dict(zip(keys, item.split('::'))) for item in data.split('\n') ]
    elif mode == 4:
        return data.split('\n')
    else:
        raise ValueError("The mode given must be 1~4")
    
def unparse(data, mode: int = 1) -> str:
    if mode == 1:
        return '\n'.join(data[key] for key in data)
    elif mode == 2:
        return '\n'.join(f"{key}={value}" for key, value in data.items())
    elif mode == 3:
        return '\n'.join([ '::'.join(item.values()) for item in data ])
    elif mode == 4:
        return '\n'.join(data)
    else:
        raise ValueError("The mode given must be 1~4")
