from src.operations.operations import Echo


def test_echo():
    echo = Echo()
    assert echo.execute("Hello world!", "Hello!", prev_output="Goodbye world!") == ("Hello world! Hello!", "")
    assert echo.execute(prev_output="Only prev_output") == ("", "")
