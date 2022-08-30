from fastapi import APIRouter
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate

router = APIRouter(prefix='/files', tags=['Files'])


@router.get('/{filename}')
def files(filename,
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
    doc = DocxTemplate('app/files/templates/' + filename + '.docx')
    doc.render(context)
    doc.save('app/files/generated/' + filename + '.docx')

    return FileResponse('app/files/generated/' + filename + '.docx',
                        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
