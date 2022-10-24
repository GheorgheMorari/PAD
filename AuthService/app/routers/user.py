from fastapi import APIRouter, Depends
from bson.objectid import ObjectId
from AuthService.app.serializers.userSerializers import userResponseEntity

from AuthService.app.database import User
from .. import schemas, oauth2

router = APIRouter()


@router.post('/me', response_model=schemas.UserResponse)
def get_me(user_id: str = Depends(oauth2.require_user)):
    print(User.find_one({'_id': ObjectId(str(user_id))}))
    user = userResponseEntity(User.find_one({'_id': ObjectId(str(user_id))}))
    return {"status": "success", "user": user}