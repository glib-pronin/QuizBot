from .command_handler import router_command
from .start_test_handler import router_start_test
from .join_test_handler import router_join
from .testing_handler import router_testing

all_routers = [
    router_command,
    router_start_test,
    router_join,
    router_testing,
]