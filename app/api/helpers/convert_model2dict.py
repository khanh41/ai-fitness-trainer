def exercise_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        "name": data["name"],
        "level": data["level"],
        "rating": data["rating"],
        "createAt": data["createAt"],
        "updateAt": data["updateAt"],
    }


def user_information_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        "name": data["timePredict"],
        "phoneNumber": data["phoneNumber"],
        "weight": data["weight"],
        "createAt": data["createAt"],
        "updateAt": data["updateAt"],
    }


def user_exercise_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        "exerciseId": data["exerciseId"],
        "process": data["process"],
        "numStreak": data["numStreak"],
        "createAt": data["createAt"],
        "updateAt": data["updateAt"],
    }


def user_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        "email": data["email"],
        "password": data["password"],
        "role": data["role"],
        "createAt": data["createAt"],
        "updateAt": data["updateAt"],
    }


def exercise_trainer_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        "modelUrl": data["modelUrl"],
        "angleConfig": data["angleConfig"],
        "createAt": data["createAt"],
        "updateAt": data["updateAt"],
    }
