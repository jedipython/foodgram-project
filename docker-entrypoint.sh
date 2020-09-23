fixtures = (
    "ingredients.json",
)

for fixture in fixtures:
    try:
        call_command("loaddata", fixture)
    except Exception:
        print("Can't load fixtures from: ", fixture)  # noqa