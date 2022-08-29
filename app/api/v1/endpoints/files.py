import os

from fastapi import APIRouter
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate

router = APIRouter(prefix='/files', tags=['Files'])


@router.get('/{filename}')
def qwe(filename,
        name: str = '',
        surname: str = '',
        patronymic: str = '',
        phone: str = '',
        passport: str = '',
        seria: str = '',
        nomer: str = '',
        address: str = '',
        familyComposition: str = '',
        birthday: str = '',
        gender: str = ''):
    doc = DocxTemplate('files/templates/' + filename + '.docx')
    context = {'name': name,
               'surname': surname,
               'patronymic': patronymic,
               'phone': phone,
               'passport': passport,
               'seria': seria,
               'nomer': nomer,
               'address': address,
               'familyComposition': familyComposition,
               'birthday': birthday,
               'gender': gender}
    doc.render(context)
    doc.save('files/generated/' + filename + '.docx')

    return FileResponse('files/generated/' + filename + '.docx', media_type='application/msword')
