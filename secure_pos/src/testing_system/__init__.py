from testing_system.tester import TestingSystem


def development_testing():
    test_system = TestingSystem()
    num_sessions = [50, 100, 200, 300, 400, 500, 1000]
    test_system.start_development_testing(num_sessions)


def execution_testing():
    test_system = TestingSystem()
    execution_len = 1000
    monitoring_len = 10
    num_sessions = [i * (execution_len + monitoring_len) for i in range(1, 5)]
    test_system.start_execution_testing(num_sessions, execution_len, monitoring_len)


if __name__ == "__main__":
    # development_testing()
    execution_testing()
    print("FINE TESTING")
