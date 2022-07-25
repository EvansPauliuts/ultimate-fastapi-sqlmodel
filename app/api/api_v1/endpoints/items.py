from typing import Any
from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def test() -> Any:
    return {'message': 'Hello World'}
