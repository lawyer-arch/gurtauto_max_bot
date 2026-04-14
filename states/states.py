from maxapi.context import StatesGroup, State


class LeadForm(StatesGroup):
    phone = State()
    marka_model_color = State()
    engine = State()
    drive = State()
    fuel = State()
    mileage = State()
    year = State()
    budget = State()
    repairs = State()
    url = State()
    image = State()