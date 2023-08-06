# Usage

from internet_sabotage import no_connection

with no_connection():
    response = requests.get('http://httpbin.org/ip')


or

@no_connection
def test_something():
    pass
