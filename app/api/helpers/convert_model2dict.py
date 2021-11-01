def exercise_helper(data) -> dict:
    return {
        "exerciseId": data["exerciseId"],
        "name": data["name"],
        "level": data["level"],
        "rating": data["rating"],
        "creatAt": data["creatAt"],
        "updateAt": data["updateAt"],
    }


def user_information_helper(data) -> dict:
    return {
        "userId": data["userId"],
        "name": data["timePredict"],
        "phoneNumber": data["phoneNumber"],
        "weight": data["weight"],
        "creatAt": data["creatAt"],
        "updateAt": data["updateAt"],
    }


def user_exercise_helper(data) -> dict:
    return {
        "userId": data["userId"],
        "exerciseId": data["exerciseId"],
        "process": data["process"],
        "numStreak": data["numStreak"],
        "creatAt": data["creatAt"],
        "updateAt": data["updateAt"],
    }


def user_helper(data) -> dict:
    return {
        "userId": data["userId"],
        "email": data["email"],
        "password": data["password"],
        "role": data["role"],
        "creatAt": data["creatAt"],
        "updateAt": data["updateAt"],
    }


def exercise_trainer_helper(data) -> dict:
    return {
        "exerciseId": data["exerciseId"],
        "modelUrl": data["modelUrl"],
        "angleConfig": data["angleConfig"],
        "creatAt": data["creatAt"],
        "updateAt": data["updateAt"],
    }
