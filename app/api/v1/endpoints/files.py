from fastapi import APIRouter
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate
from app.schemas.user import ChangeUser

router = APIRouter(prefix='/files', tags=['Files'])


@router.get('/{filename}')
def files(filename):
    context = {'name': '',
               'surname': '',
               'patronymic': '',
               'phone': '',
               'passport': '',
               'seria': '',
               'nomer': '',
               'address': '',
               'familyComposition': '',
               'birthday': '',
               'gender': ''}
    doc = DocxTemplate('app/files/templates/' + filename + '.docx')
    doc.render(context)
    doc.save('app/files/generated/' + filename + '.docx')

    return FileResponse('app/files/generated/' + filename + '.docx',
                        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')


@router.post('/{filename}')
def files(filename, user: ChangeUser):
    # seria =
    # nomer =
    context = {'name': user.name,
               'surname': user.surname,
               'patronymic': user.patronymic,
               'phone': user.phone,
               'passport': user.passport,
               'seria': '',
               'nomer': '',
               'address': user.address,
               'familyComposition': user.familyComposition,
               'birthday': user.birthday,
               'gender': user.gender}
    doc = DocxTemplate('app/files/templates/' + filename + '.docx')
    doc.render(context)
    doc.save('app/files/generated/' + filename + '.docx')

    return FileResponse('app/files/generated/' + filename + '.docx',
                        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        filename=filename + 'docx')
