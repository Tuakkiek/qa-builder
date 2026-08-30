def save_request_count(count: int) -> None:
    REQUEST_COUNT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        REQUEST_COUNT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            {"request_count": count},
            file,
            ensure_ascii=False,
            indent=4
        )

