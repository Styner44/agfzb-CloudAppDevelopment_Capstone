def main(dict):
    name = dict.get('name', 'World')
    greeting = f'Hello, {name}!'
    return {"greeting": greeting}