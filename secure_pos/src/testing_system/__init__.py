from testing_system.tester_development import DevelopmentTester
from testing_system.tester_execution import ExecutionTester


def development_testing():
    test_system = DevelopmentTester()
    # num_sessions = [1, 1, 1]
    num_sessions = [50, 100, 200, 300, 400, 500]
    test_system.start_development_testing(num_sessions)


def execution_testing():
    test_system = ExecutionTester()
    execution_len = 1000
    monitoring_len = 10

    # num_sessions = [5]
    num_sessions = [i * (execution_len + monitoring_len) for i in range(1, 5)]
    
    test_system.start_execution_testing(num_sessions, execution_len, monitoring_len)


if __name__ == "__main__":
    development_testing()
    # execution_testing()
    print("FINE TESTING")
