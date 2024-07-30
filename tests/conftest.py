import pytest
import pandas as pd


@pytest.fixture
def sample_data():
    """Создает фикстуру с образцом данных для тестов."""
    data = {
        'Категория': ['Food', 'Transport', 'Food', 'Entertainment'],
        'Дата платежа': ['01.09.2023', '15.09.2023', '20.09.2023', '30.09.2023'],
        'Сумма операции': [300, 150, 450, 200]
    }
    return pd.DataFrame(data)