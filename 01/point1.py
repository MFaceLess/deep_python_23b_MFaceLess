class SomeModel:
    def predict(self, message: str) -> float:
        message_len = len(message)
        if message_len > 10:
            return 1.0 / (message_len * 0.05 + 0.01)
        return 1.0 / (message_len + 0.01)


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    pred = model.predict(message)
    ans = ''
    if pred < bad_thresholds:
        ans = 'неуд'
    elif pred > good_thresholds:
        ans = 'отл'
    else:
        ans = 'норм'
    return ans


if __name__ == '__main__':
    models = SomeModel()

    assert predict_message_mood("Чапаев и пустота", models) == "отл"
    assert predict_message_mood("Вулкан", models) == "неуд"
