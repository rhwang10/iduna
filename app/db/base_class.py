import typing as t

from sqlalchemy.ext.declarative import as_declarative, declared_attr

class_registry: t.Dict = {}

@as_declarative(class_registry=class_registry)
class Base:
    id: t.Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__
        tokens = []
        start = 0
        for idx in range(len(name)):
            if idx == 0 or (name[idx].islower() and idx != len(name) - 1):
                pass
            elif idx == len(name) - 1 or (name[idx].isupper() and idx != 0):
                if idx == len(name) - 1:
                    tokens.append(name[start:idx + 1].lower())
                else:
                    tokens.append(name[start:idx].lower())
                    start = idx
        return '_'.join(tokens)
